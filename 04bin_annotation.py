#!/usr/bin/env python
#PBS -N S1_Nanopore_canu
#PBS -l nodes=2:ppn=8
#PBS -l walltime=999999:00:00
import multiprocessing
import argparse, operator, os, random, sys, time
import random, subprocess
import glob

workdir = "/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/RealData/results"
#bin3Cdir = "/home3/ZXMGroup/VIROME/G3compare/RealData/bin3C02"
bin_annotation_script = "/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/pipeline/06bin_annotation_allbins.sh"
contiglist="/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/RealData/results/contigs.filter.list"
os.system("mkdir -p {}/04MGE".format(workdir))
binmethods = ['bin3C']

def run(outdir, binfile, binname):
    os.system("sh {} {} {} {} 1>/dev/null".format(bin_annotation_script,outdir, binfile, binname))
    infile = os.path.join(outdir, '04prophage', binname, 'final-viral-combined.fa')
    checkvdir = os.path.join(outdir, '04prophage', binname, 'checkv')
    print("/home1/jialh/tools/miniconda3/envs/checkv/bin/checkv end_to_end {} {} -t 4".format(infile, checkvdir))
    os.system("/home1/jialh/tools/miniconda3/envs/checkv/bin/checkv end_to_end {} {} -t 4".format(infile, checkvdir))

def main():
    pool = multiprocessing.Pool(processes=32)
    with open(contiglist) as contignames:
        for contigname in contignames:
            contigname = contigname.strip()
            subject, seqmethod, assembler = contigname.split("_")
            for binmethod in binmethods:
                print("begin to deal with {}_{}".format(contigname, binmethod))
                outdir = os.path.join(workdir, '04MGE', binmethod, contigname)
                os.system("mkdir -p {}".format(outdir))
                bindir = os.path.join(workdir, '02bins', binmethod, contigname)
                #bins = os.listdir(bindir)
                bins = glob.glob(pathname=os.path.join(bindir, '*.fa'))
                print("bin_count: {}".format(len(bins)))
                for i in range(0, len(bins)):
                    binfile = bins[i]
                    #print("binfile: {}".format(binfile))
                    binname = bins[i].split('/')[-1]
                    pool.apply_async(func=run, args=(outdir, binfile, binname,))
                    #run(outdir, binfile, binname)
                #run(outdir, binfile, binname)

    pool.close()
    pool.join()

if __name__ == '__main__':
    main()