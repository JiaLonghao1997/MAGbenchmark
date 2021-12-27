#!/usr/bin/env python
import pandas as pd
import multiprocessing
import argparse, operator, os, random, sys, time
import random, subprocess

#asssmbler="multi"

workdir="/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/RealData/results"
dataset='RealData'
binlabelscript="/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/pipeline/04bin_label_and_evaluate.sh"
contiglist=os.path.join(workdir, "contigs.list")
contigdir="/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/RealData/results/contigs"
enzyme="DpnII"

def run(sample,workdir, method):
    os.system("sh /share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/pipeline/04bin_label_and_evaluate_all.sh {} {} {}".format(sample, workdir, method))
          
def main():
    os.system("python /share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/pipeline/03make_config.py {} {} {} {}".format(workdir, dataset, contigdir, enzyme))
    pool = multiprocessing.Pool(processes=8)
    #workdir = "/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/GIS20/results"
    with open(contiglist) as contigs:
        for sample in contigs:
            sample = sample.strip()
            print("Processing {} ".format(sample))
            method = sample.split('_')[1]
            pool.apply_async(func=run, args=(sample, workdir, method,))
            #run(sample, method)
    pool.close()
    pool.join()    
    #merge(args.BasePath,args.outputdir)    
       
if __name__ == '__main__':
    main()