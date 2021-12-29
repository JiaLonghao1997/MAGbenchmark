#!/usr/bin/env python
import pandas as pd
import multiprocessing
import argparse, operator, os, random, sys, time
import random, subprocess
from Bio import SeqIO

workdir="/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/RealData/Nanopore/canu"
samples=["A_Nanopore_canu", "B_Nanopore_canu","F_Nanopore_canu"]
longdir="/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/RealData/Nanopore/data"
shortdir="/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/G2/02_trim"
genomesize = ('50m', '100m')

def run(sample,genomesize1, genomesize2, workdir, input):
    os.system("sh /share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/pipeline/01canu_nanopore.sh {} {} {} {} {}".format(sample, genomesize1,genomesize2, workdir, input))
          
def main():
    pool = multiprocessing.Pool(processes=16)
    for sample in samples:
        subject, seqmethod, assembler = sample.split('_')
        input = os.path.join(longdir, '{}.fastq.gz'.format(subject))
        genomesize1, genomesize2 = genomesize
        print("Processing {} in {} {}".format(sample, genomesize1, genomesize2))
        pool.apply_async(func=run, args=(sample,genomesize1, genomesize2, workdir, input,))
        #run(sample,genomesize1, genomesize2, workdir, input)
    pool.close()
    pool.join()    
    #merge(args.BasePath,args.outputdir)    
       
if __name__ == '__main__':
    main()