#!/usr/bin/env python
#PBS -N S1_Nanopore_canu
#PBS -l nodes=2:ppn=8
#PBS -l walltime=999999:00:00
import multiprocessing
import argparse, operator, os, random, sys, time
import random, subprocess
import pandas as pd

# dataset = sys.argv[1]
# workdir = "/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/{}/merge".format(dataset)
bin_annotation_script = "/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/pipeline/06MAG_checkm_GTDBtk.sh"
GTDB_tk_fastani = "/home1/jialh/tools/miniconda3/envs/gtdbtk-1.4.1/share/gtdbtk-1.4.1/db/fastani/database"
genome_tRNA_rRNA = "/home3/ZXMGroup/VIROME/G3compare/pipeline/04rRNA/00genome_tRNA_rRNA.py"

def get_fastani(inbac, fastani_set):
    df = pd.read_table(inbac, header=0)
    for index, row in df.iterrows():
        fastani = row['fastani_reference']
        if fastani != 'nan':
            fastani_set.add(fastani)

def prepare_fastani(GTDB_tk_dir, fastani_dir, pipelinelist, binmethods):
    if os.path.exists(fastani_dir):
        os.system("rm -rf {}".format(fastani_dir))
    else:
        os.system("mkdir -p {}".format(fastani_dir))
    fastani_set = set()
    with open(pipelinelist) as pipelines:
        for pipeline in pipelines:
            pipeline = pipeline.strip().split('+')[0]
            for binmethod in binmethods:
                print("begin to deal with {}+{}".format(pipeline, binmethod))
                inbac = os.path.join(GTDB_tk_dir, binmethod, pipeline, '02gtdbtk', 'classify',
                                     'gtdbtk.bac120.summary.tsv')
                inarc = os.path.join(GTDB_tk_dir, binmethod, pipeline, '02gtdbtk', 'classify',
                                     'gtdbtk.arc122.summary.tsv')
                get_fastani(inbac, fastani_set)
                if os.path.exists(inarc):
                    get_fastani(inarc, fastani_set)
    print("{} genomes in fastani".format(len(fastani_set)))
    for fastani in fastani_set:
        infasta = os.path.join(GTDB_tk_fastani, '{}_genomic.fna.gz'.format(fastani))
        os.system("cp {} {}".format(infasta, fastani_dir))
    GTDB_tk_RNAdir = os.path.join(workdir, "04GTDB_tk+RNA")
    os.system("cd {} || exit ".format(GTDB_tk_RNAdir))
    os.system("gunzip {}/*_genomic.fna.gz".format(fastani_dir))
    os.system("rename _genomic.fna .fa {}/*_genomic.fna".format(fastani_dir))
    os.system("python {} {} {}".format(genome_tRNA_rRNA, GTDB_tk_RNAdir, fastani_dir))

def GTDB_tk_add_RNA(inbac, tRNA_rRNA, pipeline, binmethod):
    GTDB_df = pd.read_table(inbac, header=0)
    RNA_df = pd.read_csv(tRNA_rRNA, header=0)
    GTDB_df_filter = GTDB_df.loc[GTDB_df['fastani_reference'].notnull(), ['user_genome','classification','fastani_reference']].copy()
    GTDB_RNA = pd.merge(GTDB_df_filter, RNA_df, left_on='fastani_reference', right_on='Bin')
    GTDB_RNA['pipeline'] = pipeline
    GTDB_RNA['binmethod'] = binmethod
    return GTDB_RNA

def GTDB_RNA_concat(GTDB_tk_dir, tRNA_rRNA, pipelinelist, binmethods):
    GTDB_RNA_bac_concat = pd.DataFrame()
    GTDB_RNA_arc_concat = pd.DataFrame()
    with open(pipelinelist) as pipelines:
        for pipeline in pipelines:
            pipeline = pipeline.strip().split('+')[0]
            for binmethod in binmethods:
                print("begin to deal with {}+{}".format(pipeline, binmethod))
                ##细菌
                inbac = os.path.join(GTDB_tk_dir, binmethod, pipeline, '02gtdbtk', 'classify',
                                     'gtdbtk.bac120.summary.tsv')
                GTDB_RNA_bac = GTDB_tk_add_RNA(inbac, tRNA_rRNA, pipeline, binmethod)
                if GTDB_RNA_bac_concat.shape[0] == 0:
                    GTDB_RNA_bac_concat = GTDB_RNA_bac
                else:
                    GTDB_RNA_bac_concat = pd.concat([GTDB_RNA_bac_concat, GTDB_RNA_bac])

                ##古细菌
                inarc = os.path.join(GTDB_tk_dir, binmethod, pipeline, '02gtdbtk', 'classify',
                                     'gtdbtk.ar122.summary.tsv')
                if os.path.exists(inarc):
                    GTDB_RNA_arc = GTDB_tk_add_RNA(inarc, tRNA_rRNA, pipeline, binmethod)
                    if GTDB_RNA_arc_concat.shape[0] == 0:
                        GTDB_RNA_arc_concat = GTDB_RNA_arc
                    else:
                        GTDB_RNA_arc_concat = pd.concat([GTDB_RNA_arc_concat,GTDB_RNA_arc])
    GTDB_tk_RNAdir = os.path.join(workdir, "04GTDB_tk+RNA")
    GTDB_RNA_bac_concat.to_csv(os.path.join(GTDB_tk_RNAdir, 'GTDB_RNA_bac.tsv'), sep='\t', index=False)
    GTDB_RNA_arc_concat.to_csv(os.path.join(GTDB_tk_RNAdir, 'GTDB_RNA_arc.tsv'), sep='\t', index=False)

def compare_MAG_to_fastani(Metabat2_bin3C_GTDB_RNA, Metabat2_bin3C_GTDB_RNA_compare_file):
    Metabat2_bin3C_GTDB_RNA_compare =  Metabat2_bin3C_GTDB_RNA.copy()
    for index, row in Metabat2_bin3C_GTDB_RNA.iterrows():
        if row['tRNA_y'] == 0:
            Metabat2_bin3C_GTDB_RNA_compare.loc[index, 'tRNA_compare'] = 1
        else:
            Metabat2_bin3C_GTDB_RNA_compare.loc[index, 'tRNA_compare'] = float(row['tRNA_x']) / float(row['tRNA_y'])

        if row['rna.16S_y'] == 0:
            Metabat2_bin3C_GTDB_RNA_compare.loc[index, 'rna.16S_compare'] = 1
        else:
            Metabat2_bin3C_GTDB_RNA_compare.loc[index, 'rna.16S_compare'] = float(row['rna.16S_x']) / float(row['rna.16S_y'])

        if row['rna.5S_y'] == 0:
            Metabat2_bin3C_GTDB_RNA_compare.loc[index, 'rna.5S_compare'] = 1
        else:
            Metabat2_bin3C_GTDB_RNA_compare.loc[index, 'rna.5S_compare'] = float(row['rna.5S_x']) / float(row['rna.5S_y'])

        if row['rna.23S_y'] == 0:
            Metabat2_bin3C_GTDB_RNA_compare.loc[index, 'rna.23S_compare'] = 1
        else:
            Metabat2_bin3C_GTDB_RNA_compare.loc[index, 'rna.23S_compare'] = float(row['rna.23S_x']) / float(row['rna.23S_y'])

        Metabat2_bin3C_GTDB_RNA_compare.to_csv(Metabat2_bin3C_GTDB_RNA_compare_file, sep='\t', index=False)

def run(outdir, bindir):
    os.system("sh {} {} {} 2>&1".format(bin_annotation_script,outdir, bindir))

def main():
    outdir = "/home3/ZXMGroup/VIROME/G3compare/pipeline/GTDB"
    for dataset in ['GIS20', 'CAMISIM', 'RealData']:
        workdir = "/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/{}/merge".format(dataset)
        pipelinelist = os.path.join(workdir, "pipeline.list")
        binmethods = ['Metabat2', 'bin3C']
        os.system("mkdir -p {}/03phylogenetic".format(workdir))
        GTDB_tk_dir = os.path.join(workdir, "03phylogenetic")

        ##<------------------------------------------------------------------>##
        # fastani_dir = os.path.join(workdir, "04GTDB_tk+RNA", "fastani")
        # prepare_fastani(GTDB_tk_dir, fastani_dir, pipelinelist, binmethods)
        # GTDB_tk_RNAdir = os.path.join(workdir, "04GTDB_tk+RNA")
        # tRNA_rRNA = os.path.join(GTDB_tk_RNAdir, "tRNA_rRNA.csv")
        ########开始处理结果########
        # GTDB_RNA_concat(GTDB_tk_dir, tRNA_rRNA, pipelinelist, binmethods)

        ###结合MAG RNA和fastani RNA的情况，求比值。
        GTDB_tk_RNAdir = os.path.join(workdir, "04GTDB_tk+RNA")
        Metabat2_bin3C_complete = pd.read_table(os.path.join(workdir, 'Metabat2+bin3C.complete.txt'), header=0)
        GTDB_RNA_bac = pd.read_table(os.path.join(GTDB_tk_RNAdir, 'GTDB_RNA_bac.tsv'), sep='\t', header=0)
        print(GTDB_RNA_bac.iloc[0:5,])
        print(GTDB_RNA_bac.loc[0:5,'user_genome'])
        GTDB_RNA_bac[['sample', 'binname']] = GTDB_RNA_bac['user_genome'].str.split('\+bin',1, expand=True)
        GTDB_RNA_bac['binname'] = 'bin' + GTDB_RNA_bac['binname'].astype(str)
        print(GTDB_RNA_bac.iloc[0:5,])
        Metabat2_bin3C_complete_filter = Metabat2_bin3C_complete[['sample','binmethod','binname','pipeline_y','group','tRNA','rna.16S','rna.23S','rna.5S', 'Completeness','Contamination','quality']].copy()
        Metabat2_bin3C_GTDB_RNA = pd.merge(Metabat2_bin3C_complete_filter, GTDB_RNA_bac, left_on=['sample', 'binmethod', 'binname'], right_on=['sample', 'binmethod', 'binname'])
        Metabat2_bin3C_GTDB_RNA.to_csv(os.path.join(outdir, '{}_Metabat2_bin3C_GTDB_RNA.tsv'.format(dataset)), sep='\t', index=False)

        Metabat2_bin3C_GTDB_RNA_compare = os.path.join(outdir, '{}_Metabat2_bin3C_GTDB_RNA_compare.tsv'.format(dataset))
        Metabat2_bin3C_GTDB_RNA_compare2 = os.path.join(outdir, '{}_Metabat2_bin3C_GTDB_RNA_compare2.tsv'.format(dataset))
        compare_MAG_to_fastani(Metabat2_bin3C_GTDB_RNA, Metabat2_bin3C_GTDB_RNA_compare)
        os.system("sed 's/Metabat2/MetaBAT2/g' {} > {}".format(Metabat2_bin3C_GTDB_RNA_compare, Metabat2_bin3C_GTDB_RNA_compare2))

if __name__ == '__main__':
    main()