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

#bin_stat = open(os.path.join(outdir, "bin_per_species.csv"), 'w')
#bin_stat.write("{},{},{},{},{},{},{}\n".format("contig_name", "pipeline", "subject", "method", "tool", "bin_count", "count"))
genomestat = open(os.path.join(outdir, "genome_bins_quality.csv"), 'w')
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
            #print(source_bininfo['Total.length.....0.bp.'])
            source_bininfo[['Total.length.....0.bp.', 'Contamination']] = source_bininfo[['Total.length.....0.bp.', 'Contamination']].apply(pd.to_numeric)
            bininfo = source_bininfo[(source_bininfo['Total.length.....0.bp.'] > 200000) & (source_bininfo['Contamination'] < 10)]
            bin_per_species = bininfo.loc[:, 'Final.Class'].value_counts()
            checkm_90_5 = bininfo[(bininfo['Completeness'] > 90) & (bininfo['Contamination'] < 5)].shape[0]
            checkm_50_5 = bininfo[(bininfo['Completeness'] >= 50) & (bininfo['Contamination'] < 10)].shape[0]
            checkm_0_5 = bininfo[(bininfo['Completeness'] > 0) & (bininfo['Completeness'] < 50) & (bininfo['Contamination'] < 10)].shape[0]
            genomestat.write("{},{},{},{},{},{},{}\n".format(contig_name, sample, subject, method, tool, '> 90% / < 5%', checkm_90_5))
            genomestat.write("{},{},{},{},{},{},{}\n".format(contig_name, sample, subject, method, tool, '>=50% / < 10%', str(checkm_50_5 - checkm_90_5)))
            genomestat.write("{},{},{},{},{},{},{}\n".format(contig_name, sample, subject, method, tool, '< 50% / < 10%', checkm_0_5))

#bin_stat.close()
genomestat.close()