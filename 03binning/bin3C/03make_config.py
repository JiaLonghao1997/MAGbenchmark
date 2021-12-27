#!/usr/bin/env python
#PBS -N config.yaml
#PBS -l nodes=2:ppn=4
#PBS -l walltime=999999:00:00
import multiprocessing
import argparse, operator, os, random, sys, time
import random, subprocess

def make_config(contig_name):
    subject, method, tool = contig_name.split("_")
    # if 'hybridSPAdes' in tool or 'OPERA-MS' in tool:
    #      readname = "{}_mNGS".format(subject)
    # else:
    #      readname = "{}_{}".format(subject, method)
    readname = "{}_mNGS".format(subject)
    method = readname.split('_')[1]
    contigfile = os.path.join(contigdir, "{}.fa".format(contig_name))
    configfile = os.path.join(outdir, "{}_config.yaml".format(contig_name))
    #if not os.path.exists(configfile):
    outfile = open(configfile, 'w')
    outfile.write("assembly: {}\n".format(contigfile))
    outfile.write("sample: {}\n".format(contig_name))
    reads = filedict[readname].split(",")
    print("{} reads: {}".format(contig_name, reads))
    print(reads)
    if len(reads) == 1:
        outfile.write("reads1: {}\n".format(reads[0]))
    elif len(reads) == 2:
        outfile.write("reads1: {}\n".format(reads[0]))
        outfile.write("reads2: {}\n".format(reads[1]))

    ##begin to deal with HiC reads.
    HiC_name = "{}_HiC".format(subject)
    HiC_reads = filedict[HiC_name].split(',')
    print('HiC_reads: {}'.format(HiC_reads))
    if len(HiC_reads) == 1:
        outfile.write("HiC_reads: {}\n".format(HiC_reads[0]))
    elif len(HiC_reads) == 2:
        outfile.write("HiC_reads1: {}\n".format(HiC_reads[0]))
        outfile.write("HiC_reads2: {}\n".format(HiC_reads[1]))
    print("enzyme: {}".format(enzyme))
    outfile.write("enzyme: {}\n".format(enzyme))
    outfile.write("krakendb: {}\n".format(krakendb))
    if method == "PacBio" or method == "PacBio+CCS":
        reads_len = lendict[readname]
        outfile.write("read_length: {}\n".format(round(float(reads_len))))
        outfile.write("long_read: True")
    if method == "Nanopore":
        reads_len = lendict[readname]
        outfile.write("read_length: {}\n".format(round(float(reads_len))))
        outfile.write("long_read: True")
    if method == "mNGS":
        reads_len = lendict[readname]
        outfile.write("read_length: {}\n".format(round(float(reads_len))))
        outfile.write("long_read: False")
    outfile.close()

def main():
    with open(reads_list) as file_info:
        for line in file_info:
            if line.startswith('Sample'):
                continue
            readname, read_len, reads = line.strip().split("\t")
            lendict[readname] = read_len
            filedict[readname] = reads
    print(filedict)
    print(lendict)

    pool = multiprocessing.Pool(processes=16)
    # workdir = "/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/GIS20/results"
    with open(os.path.join(workdir, "contigs.list")) as contigs_info:
        for line in contigs_info:
            contig_name = line.strip()
            print("begin to deal with {}".format(contig_name))
            #pool.apply_async(func=make_config, args=(contig_name,))
            make_config(contig_name)
    pool.close()
    pool.join()
    # merge(args.BasePath,args.outputdir)

if __name__ == '__main__':
    filedict = {}
    lendict = {}
    workdir = sys.argv[1]
    dataset = sys.argv[2]
    contigdir = sys.argv[3]
    enzyme = sys.argv[4]
    #os.system("")
    #contigdir = os.path.join(workdir, "contigs")
    outdir = os.path.join(workdir, "configs")
    os.system('mkdir -p {}'.format(outdir))
    contiglist = os.path.join(workdir, "contigs.list")
    if dataset == 'GIS20':
        reads_list = "/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/pipeline/data/GIS20_reads.tsv"
        krakendb = "/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/GIS20/kraken2db/GIS20"
    elif dataset == 'CAMISIM':
        reads_list = "/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/pipeline/data/CAMISIM_reads.tsv"
        krakendb = "/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/CAMISIM/kraken2db/CAMISIM"
    elif dataset == 'RealData':
        reads_list = "/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/pipeline/data/RealData_reads.tsv"
        krakendb = "/share/inspurStorage/home1/jialh/human_virome/tools/kraken2-2.1.1/minikraken_8GB_20200312"

    elif dataset == 'NBT2020':
        reads_list = "/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/pipeline/data/NBT2020_reads.tsv"
        krakendb = "/share/inspurStorage/home1/jialh/human_virome/tools/kraken2-2.1.1/minikraken_8GB_20200312"

    #os.system("ls -l " + contigdir + " | awk '{print $9}' | grep -v '^$' | awk -F '.' '{print $1 }' > " + contiglist)

    if not os.path.exists(outdir):
        os.makedirs(outdir)
    main()
