# !/usr/bin/env python
import pandas as pd
import multiprocessing
import argparse, operator, os, random, sys, time
import random, subprocess

workdir = "/share/inspurStorage/home1/jialh/tools/UHGG"
bindir="/share/inspurStorage/home1/jialh/tools/UHGG/UHGG"
script = "/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/pipeline/04rRNA/00tRNA_rRNA.sh"
RNAstat_script = "/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/pipeline/04rRNA/02RNAstat.py"
binlist = os.path.join(workdir, "bin.list")

def run(workdir, bin, bindir):
    os.system("sh {} {} {} {}".format(script, workdir, bin, bindir))
    os.system("python {} {}".format(RNAstat_script, workdir))

def main():
    os.system("ls -l {}".format(bindir) + " | awk '{print $9}' | grep '.fa$' | awk -F '.fa' '{print $1}' " + "{}".format(binlist))
    pool = multiprocessing.Pool(processes=32)
    with open(binlist) as bins:
        for bin in bins:
            bin = bin.strip()
            print("Processing {} ".format(bin))
            pool.apply_async(func=run, args=(workdir, bin, bindir,))
            # run(bin, method)
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
