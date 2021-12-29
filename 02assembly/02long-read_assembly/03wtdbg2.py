#!/usr/bin/env python
#PBS -N S1_Nanopore_canu
#PBS -l nodes=2:ppn=8
#PBS -l walltime=999999:00:00
import pandas as pd
import multiprocessing
import argparse, operator, os, random, sys, time
import random, subprocess
from Bio import SeqIO

workdir="/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/RealData/Nanopore/wtdbg2"
samples=["A_Nanopore_wtdbg2", "B_Nanopore_wtdbg2","F_Nanopore_wtdbg2"]
longdir="/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/RealData/Nanopore/data"
shortdir="/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/G2/02_trim"
genomesize = ('50m', '100m')

def run(sample,genomesize1, genomesize2, workdir, input, seqmethod):
    os.system("sh /home3/ZXMGroup/VIROME/G3compare/pipeline/01wtdbg2.sh {} {} {} {} {} {}".format(sample, genomesize1,genomesize2, workdir, input, seqmethod))
          
def main():
    pool = multiprocessing.Pool(processes=16)
    for sample in samples:
        subject, seqmethod, assembler = sample.split('_')
        input = os.path.join(longdir, '{}.fastq.gz'.format(subject))
        genomesize1, genomesize2 = genomesize
        print("Processing {} in {} {}".format(sample, genomesize1, genomesize2))
        pool.apply_async(func=run, args=(sample,genomesize1, genomesize2, workdir, input,seqmethod, ))
        #run(sample,genomesize1, genomesize2, workdir, input, seqmethod)
    pool.close()
    pool.join()    
    #merge(args.BasePath,args.outputdir)    
       
if __name__ == '__main__':
    main()