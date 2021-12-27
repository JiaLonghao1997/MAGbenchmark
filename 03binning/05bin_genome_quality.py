#!/usr/bin/env python
#PBS -N config.yaml
#PBS -l nodes=2:ppn=4
#PBS -l walltime=999999:00:00
import os
import pandas as pd
import sys

filedict={}

workdir=sys.argv[1]

#refseqlist="/home3/ZXMGroup/VIROME/G3compare/pipeline/data/GIS20.refseq.list"
contigdir=os.path.join(workdir, "contigs")
inputdir=os.path.join(workdir, "01binlabel")
outdir=os.path.join(workdir, "02binstat")

if not os.path.exists(outdir):
    os.makedirs(outdir)

genome_list = []
# with open(refseqlist) as genomes:
#     for genome in genomes:
#         genome_list.append(genome.strip())
# print(genome_list)
genome_N50 = open(os.path.join(outdir, "genome_N50.csv"), 'w')
genome_N50.write("{},{},{},{},{},{},{},{},{},{},{}\n".format("sample", "bin","Completeness","Contamination",'species',
                                                             "tRNA","16S.rna","23S.rna","5S.rna",'Size.MB','quality'))

with open(os.path.join(workdir, "contigs.list")) as contigs_info:
    for line in contigs_info:
        contig_name = line.strip()
        #print("begin to deal with {}".format(contig_name))
        subject, method, tool = contig_name.split("_")
        sample = method+'_'+tool

        binfile =  os.path.join(inputdir, contig_name, "final", "{}.tsv".format(contig_name))
        #print(binfile)
        if os.path.exists(binfile):
            source_bininfo = pd.read_csv(binfile, sep="\t", header=0)
            source_bininfo[['Total.length.....0.bp.', 'Contamination']] = source_bininfo[['Total.length.....0.bp.', 'Contamination']].apply(pd.to_numeric)
            bininfo = source_bininfo[(source_bininfo['Total.length.....0.bp.'] > 200000) & (source_bininfo['Contamination'] < 10)]
            for index, row in bininfo.iterrows():
                quality = ''
                if float(row['Completeness']) > 90 and float(row['Contamination']) < 5 and float(row['tRNA']) >= 18 and float(row['rna.16S']) >= 1 and float(row['rna.23S']) >= 1 and float(row['rna.5S']) >= 1:
                    quality = 'high-quality'
                elif row['Completeness'] > 90 and row['Contamination'] < 5:
                    quality = 'complete'
                elif row['Completeness'] >= 50 and row['Contamination'] < 10:
                    quality = 'medium-quality'
                elif row['Completeness'] < 50 and row['Contamination'] < 10:
                    quality = 'low-quality'

                genome_N50.write("{},{},{},{},{},{},{},{},{},{},{}\n".format(
                                                                      row['Sample'], row['Bin'],
                                                                      row['Completeness'], row['Contamination'],
                                                                      row['Final.Class'],
                                                                      row['tRNA'], row['rna.16S'], row['rna.23S'],
                                                                      row['rna.5S'],
                                                                      row['Size.Mb'], quality))
                #genome_list2.remove(row['Final.Class'])
genome_N50.close()