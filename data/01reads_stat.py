#!/usr/bin/env python
#PBS -N config.yaml
#PBS -l nodes=2:ppn=4
#PBS -l walltime=999999:00:00
import multiprocessing
import argparse, operator, os, random, sys, time
import random, subprocess

def reads_stat(workdir, readname, read, outfile):
    print("reads stat of {}".format(readname))
    reads = read.strip().split(',')
    if len(reads) == 1:
        os.system("seqkit stats -j 8 {} >> {}".format(reads[0], outfile))
    elif len(reads) == 2:
        print("read1: {}".format(reads[0]))
        print("read2: {}".format(reads[1]))
        inter_reads = os.path.join(workdir, '{}_merge.fasta'.format(readname))
        #print("inter_reads: {}".format(inter_reads))
        #if not os.path.exists(inter_reads):
        print("sh /home1/jialh/human_virome/tools/bbmap/reformat.sh minlength=60 trimq=20 -Xmx=100G ow=t in1={} in2={} out={}".format(reads[0], reads[1], inter_reads))
        os.system("sh /home1/jialh/human_virome/tools/bbmap/reformat.sh -Xmx=100G ow=t in1={} in2={} out={}".format(reads[0], reads[1], inter_reads))
        os.system("seqkit stats -j 16 {} >> {}".format(inter_reads, outfile))
        # elif os.path.exists(inter_reads):
        #     os.system("seqkit stats -j 8 {} >> {}".format(inter_reads, outfile))

def main():
    pool = multiprocessing.Pool(processes=6)
    datasets = ['CAMISIM']
    workdir = "/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/pipeline/data"
    inputdir = "/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/pipeline/data"
    outfile = os.path.join(inputdir, 'reads_stat_CAMISIM_longreads.csv')
    for dataset in datasets:
        print("stat read length of {}".format(dataset))
        readslist = os.path.join(inputdir, "{}_reads.tsv".format(dataset))
        with open(readslist) as readfiles:
            for line in readfiles:
                if ('PacBio' in line) or ('Nanopore' in line) :
                    readname, readlen, read = line.split('\t')
                    pool.apply_async(func=reads_stat, args=(workdir, readname, read, outfile))
                    #reads_stat(workdir, readname, read, outfile)
    pool.close()
    pool.join()
    # merge(args.BasePath,args.outputdir)

if __name__ == '__main__':
    main()

