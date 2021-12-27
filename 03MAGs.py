#!/usr/bin/env python
#PBS -N S1_Nanopore_canu
#PBS -l nodes=2:ppn=8
#PBS -l walltime=999999:00:00
import multiprocessing
import argparse, operator, os, random, sys, time
import random, subprocess
import pandas as pd

workdir = "/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/RealData/results"
#bin3Cdir = "/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/RealData/bin3C02"
bin_annotation_script = "/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/pipeline/06MAG_checkm_GTDBtk.sh"
contiglist="/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/RealData/results/contigs.list"
os.system("mkdir -p {}/03MAG".format(workdir))
binmethods = ['metabat2', 'bin3C']

def filter_mhbins(contigname, inputdir, mh_bindir):
    final_tsv = os.path.join(inputdir, '01binlabel', contigname, 'final', '{}.tsv'.format(contigname))
    final_df = pd.read_table(final_tsv, header=0)
    final_df_filter = final_df.loc[(final_df['Completeness'] > 50) & (final_df['Contamination'] < 10), ]
    for index, row in final_df_filter.iterrows():
        binname = row['Bin']
        binfile = os.path.join(inputdir, '01binlabel', contigname, 'bins', '{}.fa'.format(binname))
        os.system('cp  {} {}'.format(binfile, mh_bindir))

def run(outdir, bindir):
    os.system("sh {} {} {} >/dev/null 2>&1".format(bin_annotation_script,outdir, bindir))

def main():
    pool = multiprocessing.Pool(processes=2)
    with open(contiglist) as contignames:
        for contigname in contignames:
            #if 'OPERA-MS' in contigname:
            contigname = contigname.strip()
            print("begin to deal with {}".format(contigname))
            subject, seqmethod, assembler = contigname.split("_")
            for binmethod in binmethods:
                inputdir = ''
                if binmethod == 'metabat2':
                    inputdir = '/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/RealData/results'
                elif binmethod == 'bin3C':
                    inputdir = '/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/RealData/bin3C'

                mh_bindir = os.path.join(workdir, '02bins', '{}'.format(binmethod), contigname)
                os.system("mkdir -p {}".format(mh_bindir))
                ###<-----------------filter medium and high-quality bins---------->
                filter_mhbins(contigname, inputdir, mh_bindir)

                ##<------------------GTDB-tk and CheckM------------------>##
                # outdir = os.path.join(workdir, '03MAG', binmethod, contigname)
                # os.system("mkdir -p {}".format(outdir))
                # pool.apply_async(func=run, args=(outdir, mh_bindir,))
                #run(outdir, mh_bindir)

    pool.close()
    pool.join()

if __name__ == '__main__':
    main()