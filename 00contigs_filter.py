#!/usr/bin/env python
import pandas as pd
import multiprocessing
import argparse, operator, os, random, sys, time
import random, subprocess

# asssmbler="multi"
workdir = "/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/RealData/results"
dataset = 'RealData'
binlabelscript = "/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/pipeline/04bin_label_and_evaluate.sh"
contiglist = os.path.join(workdir, "contigs.list")
contigdir = "/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/RealData/results/contigs"
contigdir_1k = "/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/RealData/results/contigs_1k"
contig_filter = "/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/pipeline/06parse_genome_1000.py"
contig_stat = "/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/pipeline/02contigs/01contigs_stat.py"

def run(infasta, outfasta):
    os.system("python {} {} {}".format(contig_filter, infasta, outfasta))

def main():
    pool = multiprocessing.Pool(processes=8)
    with open(contiglist) as contigs:
        for sample in contigs:
            sample = sample.strip()
            print("Processing {} ".format(sample))
            method = sample.split('_')[1]
            infasta = os.path.join(contigdir, '{}.fa'.format(sample))
            outfasta = os.path.join(contigdir_1k, '{}.fa'.format(sample))
            #pool.apply_async(func=run, args=(infasta, outfasta,))
            # run(sample, method)
    pool.close()
    pool.join()
    # merge(args.BasePath,args.outputdir)
    os.system("python {} {}".format(contig_stat, workdir))

if __name__ == '__main__':
    main()
