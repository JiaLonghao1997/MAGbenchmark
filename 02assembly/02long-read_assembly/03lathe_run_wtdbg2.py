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
bigcontiglength = '800k'
lathescript="/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/pipeline/01lathe_run.sh"
sourceconfig="/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/pipeline/config.yaml"

def run(workdir,configfile, genomesize1, genomesize2, bigcontiglength,assembler,sample, seqmethod):
    infile1="{}/{}_{}_{}/1.assemble/assemble_{}.fa".format(workdir,sample, genomesize1, genomesize2,
                                                                            genomesize1)
    outdir1="{}/{}_{}_{}/1.assemble/assemble_{}".format(workdir, sample, genomesize1, genomesize2, genomesize1)
    outfile1="{}/{}_{}_{}/1.assemble/assemble_{}/{}_{}_{}_{}.contigs.fasta".format(workdir,sample, genomesize1,
                                                                                   genomesize2, genomesize1, sample,
                                                                                   genomesize1, genomesize2,genomesize1)
    if os.path.exists(infile1):
        os.system("mkdir -p {}".format(outdir1))
        os.system("cp {} {}".format(infile1, outfile1))

    infile2 = "{}/{}_{}_{}/1.assemble/assemble_{}.fa".format(workdir, sample, genomesize1, genomesize2,
                                                                              genomesize2)
    outdir2 = "{}/{}_{}_{}/1.assemble/assemble_{}".format(workdir, sample, genomesize1, genomesize2, genomesize2)
    outfile2 = "{}/{}_{}_{}/1.assemble/assemble_{}/{}_{}_{}_{}.contigs.fasta".format(workdir, sample, genomesize1,
                                                                                     genomesize2, genomesize2, sample,
                                                                                     genomesize1, genomesize2,
                                                                                     genomesize2)
    if os.path.exists(infile2):
        os.system("mkdir -p {}".format(outdir2))
        os.system("cp {} {}".format(infile2, outfile2))
    print("sh {} {} {} {} {} {} {} {} {}".format(lathescript, workdir, configfile, genomesize1, genomesize2, bigcontiglength, assembler, sample, seqmethod))
    os.system("sh {} {} {} {} {} {} {} {} {}".format(lathescript, workdir, configfile, genomesize1, genomesize2, bigcontiglength, assembler, sample, seqmethod))
          
def main():
    pool = multiprocessing.Pool(processes=16)
    for sample in samples:
        subject, seqmethod, assembler = sample.split('_')
        input = os.path.join(longdir, '{}.fastq.gz'.format(subject))
        reads1 = os.path.join(shortdir, '{}_trim1.paired.fq.gz'.format(subject))
        reads2 = os.path.join(shortdir, '{}_trim2.paired.fq.gz'.format(subject))
        if assembler == 'wtdbg2':
            genomesize1, genomesize2 = genomesize
            print("Processing {} in {} {}".format(sample, genomesize1, genomesize2))
            filename_txt = open(os.path.join(workdir, "{}_{}_{}.txt".format(sample, genomesize1, genomesize2)), 'w')
            filename_txt.write("{}_{}_{}".format(sample, genomesize1, genomesize2)+"\t"+input+"\t"+reads1+','+reads2)
            filename_txt.close()
            filename_txt_str = os.path.join(workdir, "{}_{}_{}.txt".format(sample, genomesize1, genomesize2))
            configfile = os.path.join(workdir, "contig_{}_{}_{}.yaml".format(sample, genomesize1, genomesize2))
            os.system("sed 's#file_names_path#{}#g' {} | sed 's#100m,250m#{},{}#g' | sed s/flye/canu/g > {}".format(filename_txt_str, sourceconfig, genomesize1, genomesize2, configfile))
            pool.apply_async(func=run, args=(workdir, configfile, genomesize1, genomesize2, bigcontiglength,assembler,sample,seqmethod, ))
            #run(workdir,configfile, genomesize1, genomesize2, bigcontiglength,assembler, sample, seqmethod)

    pool.close()
    pool.join()
    #merge(args.BasePath,args.outputdir)    
       
if __name__ == '__main__':
    main()