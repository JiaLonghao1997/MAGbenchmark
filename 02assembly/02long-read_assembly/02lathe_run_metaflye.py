#!/usr/bin/env python
#PBS -N S1_Nanopore_canu
#PBS -l nodes=2:ppn=8
#PBS -l walltime=999999:00:00
import pandas as pd
import multiprocessing
import argparse, operator, os, random, sys, time
import random, subprocess
from Bio import SeqIO

workdir="/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/RealData/Nanopore/metaflye"
samples=["A_Nanopore_metaflye","B_Nanopore_metaflye","F_Nanopore_metaflye"]
#samples=["A_Nanopore_metaflye"]
longdir="/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/RealData/Nanopore/data"
shortdir="/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/G2/02_trim"
genomesize = ('100m', '250m')
bigcontiglength = '800k'
lathescript="/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/pipeline/01lathe_run.sh"
sourceconfig="/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/pipeline/config.yaml"

def run(workdir,configfile, genomesize1, genomesize2, bigcontiglength, assembler, sample, seqmethod):
    os.system("sh {} {} {} {} {} {} {} {} {}".format(lathescript, workdir, configfile, genomesize1, genomesize2,
                                                     bigcontiglength, assembler, sample, seqmethod))
          
def main():
    pool = multiprocessing.Pool(processes=16)

    for sample  in samples:
        subject, seqmethod, assembler = sample.split('_')
        input = os.path.join(longdir, '{}.fastq.gz'.format(subject))
        reads1 = os.path.join(shortdir, '{}_trim1.paired.fq.gz'.format(subject))
        reads2 = os.path.join(shortdir, '{}_trim2.paired.fq.gz'.format(subject))
        genomesize1, genomesize2 = genomesize
        print("Processing {} in {} {}".format(sample, genomesize1, genomesize2))
        filename_txt = open(os.path.join(workdir, "{}_{}_{}.txt".format(sample, genomesize1, genomesize2)), 'w')
        filename_txt.write("{}_{}_{}".format(sample, genomesize1, genomesize2)+"\t"+input+"\t"+reads1+','+reads2)
        filename_txt.close()
        filename_txt_str = os.path.join(workdir, "{}_{}_{}.txt".format(sample, genomesize1, genomesize2))
        configfile = os.path.join(workdir, "contig_{}_{}_{}.yaml".format(sample, genomesize1, genomesize2))
        os.system("sed 's#file_names_path#{}#g' {} | sed 's#100m,250m#{},{}#g' > {}".format(filename_txt_str, sourceconfig, genomesize1, genomesize2, configfile))

        os.system("rm -rf {}".format(os.path.join(workdir, "{}_{}".format(sample, bigcontiglength),
                                                  "{}_{}_{}".format(sample, genomesize1, genomesize2),
                                                  "3.circularization")))
        os.system("rm -rf {}".format(os.path.join(workdir, "{}_{}".format(sample, bigcontiglength),
                                                  "{}_{}_{}".format(sample, genomesize1, genomesize2), "5.final")))

        pool.apply_async(func=run, args=(workdir,configfile, genomesize1, genomesize2, bigcontiglength, assembler, sample, seqmethod ))
    #     final = "{}/{}_800k/{}_100m_250m/5.final/{}_100m_250m_final.fa".format(workdir, sample, sample, sample)
    #     if os.path.exists(final):
    #         os.system(
    #             "rm {}/{}_800k/{}_100m_250m/2.polish/{}_100m_250m_polished.fasta.bam".format(workdir, sample, sample,
    #                                                                                          sample))
    #         os.system("rm {}/{}_800k/{}_100m_250m/2.polish/pilon/short_reads.bam".format(workdir, sample, sample))
    #         os.system(
    #             "rm {}/{}_800k/{}_100m_250m/3.circularization/4.{}_100m_250m_circularized.fasta.bam".format(workdir,
    #                                                                                                         sample,
    #                                                                                                         sample,
    #                                                                                                         sample))
    pool.close()
    pool.join()
    #merge(args.BasePath,args.outputdir)    
       
if __name__ == '__main__':
    main()