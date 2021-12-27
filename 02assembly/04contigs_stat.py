#!/usr/bin/env python
#PBS -N S1_PacBio_canu
#PBS -l nodes=2:ppn=8
#PBS -l walltime=999999:00:00
#import pandas as pd
import multiprocessing
import argparse, operator, os, random, sys, time
import random, subprocess
import pandas as pd

#asssmbler="multi"

# workdir="/home3/ZXMGroup/VIROME/G3compare/RealData/results"
# script="/home3/ZXMGroup/VIROME/G3compare/RealData/results/04long_contig_stat.sh"
# contiglist=os.path.join(workdir, "assemblies.list")
workdir = sys.argv[1]
contiglist=os.path.join(workdir, "assembly.circulization.list")

def run(sample,workdir):
    quastdir=os.path.join(workdir, 'quast', sample)
    os.system("mkdir -p {}".format(quastdir))
    os.system("mkdir -p {}".format(os.path.join(workdir, 'contigs_1k')))
    infasta = os.path.join(workdir, 'contigs', '{}.fa'.format(sample))
    contig=os.path.join(workdir, 'contigs_1k', '{}.fa'.format(sample))
    os.system("python /home3/ZXMGroup/VIROME/G3compare/pipeline/02assembly/06parse_genome_1000.py {} {} {}".format(infasta, 1000, contig))
    os.system("/share/inspurStorage/home1/jialh/tools/miniconda3/bin/quast.py -o {} {} \
        --contig-thresholds 0,1000,10000,100000,1000000 --fast".format(quastdir, contig))
          
def main():
    pool = multiprocessing.Pool(processes=4)
    #workdir = "/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/GIS20/results"
    with open(contiglist) as contigs_1k:
        for sample in contigs_1k:
            sample = sample.strip()
            if not os.path.exists(os.path.join(workdir, 'qaust', sample, 'report.tsv')):
                print("Processing {} ".format(sample))
                #pool.apply_async(func=run, args=(sample, workdir,))
                #run(sample, workdir)
    pool.close()
    pool.join()

    groupdic = {"mNGS_metaSPAdes": "mNGS",
                "mNGS_metaSPAdes+polish": "mNGS",
                "PacBio_metaflye": "PacBio",
                "PacBio_metaflye2": "PacBio2",
                "PacBio_metaflye+polish": "PacBio",
                "PacBio_OPERA-MS": "mNGS+PacBio",
                "PacBio_OPERA-MS2": "mNGS+PacBio2",
                "PacBio_OPERA-MS+polish": "mNGS+PacBio",
                "Nanopore_metaflye": "Nanopore",
                "Nanopore_metaflye+polish": "Nanopore",
                "Nanopore_OPERA-MS": "mNGS+Nanopore",
                "Nanopore_OPERA-MS+polish": "mNGS+Nanopore"
                }
    if not os.path.exists('{}/quast/merge_report.filter.tsv'.format(workdir)):
        print('/usr/bin/paste {}/quast/*/report.tsv > {}/quast/merge_report.tsv'.format(workdir, workdir))
        os.system('/usr/bin/paste {}/quast/*/report.tsv > {}/quast/merge_report.tsv'.format(workdir, workdir))

        merge_df = pd.read_table('{}/quast/merge_report.tsv'.format(workdir), header=None, index_col=0)
        merge_df = merge_df.T
        merge_df = merge_df.loc[merge_df['Assembly']!='Assembly', ]
        merge_df.to_csv('{}/quast/merge_report.filter.tsv'.format(workdir), sep='\t', header=True, index=False)
    else:
        outfile = open('{}/quast/merge_report.modify.tsv'.format(workdir), 'w')
        with open('{}/quast/merge_report.filter.tsv'.format(workdir)) as lines:
            for line in lines:
                if line.startswith('Assembly'):
                    line = line.strip()
                    newline = 'subject\tseqmethod\tassembler\tpipeline\tgroup\t{}\n'.format(line)
                    outfile.write(newline)
                else:
                    print('sample: {}'.format(sample))
                    sample = line.strip().split('\t')[0]
                    subject = sample.split('_')[0]
                    seqmethod = sample.split('_')[1].split('+')[0]
                    assembler = sample.split('_')[2]
                    assembler2 = assembler.split('+')[0]
                    pipeline = '{}_{}'.format(seqmethod, assembler2)
                    print("pipeline:", pipeline)
                    if pipeline in groupdic:
                        group = groupdic[pipeline]
                        line = line.strip()
                        newline = '{}\t{}\t{}\t{}\t{}\t{}\n'.format(subject, seqmethod, assembler, pipeline, group, line)
                        outfile.write(newline)
       
if __name__ == '__main__':
    main()