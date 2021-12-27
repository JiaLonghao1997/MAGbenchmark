# !/usr/bin/env python
import pandas as pd
import multiprocessing
import argparse, operator, os, random, sys, time
import random, subprocess
import re

workdir = sys.argv[1]
bindir= sys.argv[2]
script = "/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/pipeline/04rRNA/00tRNA_rRNA.sh"
RNAstat_script = "/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/pipeline/04rRNA/02RNAstat.py"
binlist = os.path.join(workdir, "fastani.list")

def merge(workdir):
    tRNA = pd.read_table(os.path.join(workdir, 'final', 'trna.tmp'))
    rRNA = pd.read_table(os.path.join(workdir, 'final', 'rrna.tmp'))
    tRNA_rRNA = pd.merge(tRNA, rRNA, left_on='Bin', right_on='Bin')
    tRNA_rRNA.to_csv(os.path.join(workdir, 'tRNA_rRNA.csv'), index=False)

def run(workdir, bin, bindir):
    os.system("sh {} {} {} {}".format(script, workdir, bin, bindir))
    os.system("python {} {}".format(RNAstat_script, workdir))

def main():
    print("ls -l {}".format(bindir) + " | awk '{print $9}' | grep '.fa$' | awk -F '.fa' '{print $1}' " + " > {}".format(binlist))
    os.system("ls -l {}".format(bindir) + " | awk '{print $9}' | grep '.fa$' | awk -F '.fa' '{print $1}' " + " > {}".format(binlist))
    pool = multiprocessing.Pool(processes=16)
    with open(binlist) as bins:
        for bin in bins:
            bin = bin.strip()
            print("Processing {} ".format(bin))
            pool.apply_async(func=run, args=(workdir, bin, bindir,))
            #run(workdir, bin, bindir)
    pool.close()
    pool.join()
    os.system("sh /share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/pipeline/04rRNA/01tRNA_rRNA.stat.sh {}".format(workdir))
    merge(workdir)

if __name__ == '__main__':
    main()
