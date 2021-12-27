#!/usr/bin/env python
#PBS -N config.yaml
#PBS -l nodes=2:ppn=4
#PBS -l walltime=999999:00:00
import os
import pandas as pd
import sys
filedict={}

workdir=sys.argv[1]
accs_id=os.path.join(workdir, "contigs.list")
inputdir=os.path.join(workdir, "01binlabel")
outdir=os.path.join(workdir, "02binstat")

if not os.path.exists(outdir):
    os.makedirs(outdir)

bin_stat = open(os.path.join(outdir, "bin_per_species.csv"), 'w')
bin_stat.write("{},{},{},{},{},{},{}\n".format("contig_name", "pipeline", "subject", "method", "tool", "bins_per_species", "count"))
genomestat = open(os.path.join(outdir, "genome_quality.csv"), 'w')
genomestat.write("{},{},{},{},{},{},{}\n".format("contig_name", "pipeline", "subject", "method", "tool", "quality", "count"))

with open(os.path.join(workdir, "contigs.list")) as contigs_info:
    for line in contigs_info:
        contig_name = line.strip()
        print("begin to deal with {}".format(contig_name))
        subject, method, tool = contig_name.split("_")
        sample = method+'_'+tool

        binfile =  os.path.join(inputdir, contig_name, "final", "{}.tsv".format(contig_name))
        #print(binfile)
        if os.path.exists(binfile):
            source_bininfo = pd.read_csv(binfile, sep="\t", header=0)
            source_bininfo[['Total.length.....0.bp.', 'Contamination']] = source_bininfo[['Total.length.....0.bp.', 'Contamination']].apply(pd.to_numeric)
            bininfo = source_bininfo[(source_bininfo['Total.length.....0.bp.'] > 200000) & (source_bininfo['Contamination'] < 10)]
            bin_per_species = bininfo.loc[:, 'Final.Class'].value_counts()
            #print(bin_per_species)
            #print(bin_per_species)
            bin_count_dic={'1':0,'2':0,'>=3':0}
            #bin_per_speceis.columns=['species', 'count']
            for index, value in bin_per_species.items():
                if value == 1:
                    bin_count_dic['1'] += 1
                elif value == 2:
                    bin_count_dic['2'] += 2
                elif value >= 3:
                    bin_count_dic['>=3'] += value
            for key,value in bin_count_dic.items():
                bin_stat.write("{},{},{},{},{},{},{}\n".format(contig_name, sample, subject, method, tool, key, value))

            genome_quality_dic={'high-quality': 0, 'medium-quality': 0, 'low-quality': 0}
            high_species = 0
            medium_species = 0
            low_species = 0
            for index, row in bininfo.iterrows():
                if float(row['Completeness']) > 90 and float(row['Contamination'])<5 and float(row['tRNA'])>=18 and float(row['rna.16S'])>=1 and float(row['rna.23S'])>=1 and float(row['rna.5S'])>=1:
                    high_species = high_species + 1
                elif (row['Completeness'] >= 50 and row['Contamination'] < 10) :
                    medium_species = medium_species + 1
                elif (row['Completeness'] < 50 and row['Contamination'] < 10) :
                    low_species = low_species + 1
            genome_quality_dic['high-quality']=high_species
            genome_quality_dic['medium-quality']=medium_species
            genome_quality_dic['low-quality'] = low_species
            for key, value in genome_quality_dic.items():
                genomestat.write("{},{},{},{},{},{},{}\n".format(contig_name, sample, subject, method, tool, key, value))

bin_stat.close()
genomestat.close()