import os
import multiprocessing
import argparse, operator, os, random, sys, time
import random, subprocess

subjects=["A","B",'F']

#workdir="/home3/ZXMGroup/VIROME/G3compare/RealData/bin3C"
#prepare_scripts="/home3/ZXMGroup/VIROME/G3compare/GIS20/bin3C/01prepare_bindir.sh"

groupdic={"mNGS_metaSPAdes":"mNGS",
          "mNGS_metaSPAdes+polish":"mNGS",
          "PacBio_metaflye":"PacBio",
          "PacBio_OPERA-MS":"mNGS+PacBio",
          "Nanopore_metaflye":"Nanopore",
          "Nanopore_metaflye+polish":"Nanopore",
          "Nanopore_OPERA-MS":"mNGS+Nanopore",
          "Nanopore_OPERA-MS+polish":"mNGS+Nanopore"
          }

if "S1_mNGS_metaSPAdes" in groupdic:
    print("S1_mNGS_metaSPAdes in groupdic.")
    print(groupdic["S1_mNGS_metaSPAdes"])

gq_stat = open("genome_quality.csv", "w")
bin_stat = open("bin_stat.csv", "w")


###bin3C
bin3Cdir="/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/RealData/bin3C"
os.system("python /share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/pipeline/05bin-stat.py {}".format(bin3Cdir))
os.system("python /share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/pipeline/05bin-stat-bin3C.py {}".format(bin3Cdir))
os.system("python /share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/pipeline/05bin_genome_quality.py {}".format(bin3Cdir))
os.system("python /share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/pipeline/05bin_genome_quality_complete.py {}".format(bin3Cdir))
os.system("python /share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/pipeline/05bin_genome_quality_high.py {}".format(bin3Cdir))
genomequality_file = os.path.join(bin3Cdir, "02binstat", "genome_quality.csv")
with open(genomequality_file) as genomequality:
    for line in genomequality:
        outline = ""
        if line.startswith("contig_name"):
            outline = line.strip() + ",binmethod,final,group"
        else:
            contig_name = line.strip().split(',')[1]
            #print(contig_name)
            if contig_name in groupdic:
                #print("{} is in group".format(contig_name))
                group = groupdic[contig_name]
                outline = line.strip() + ",bin3C,1,{}".format(group)
            else:
                outline = line.strip() + ",bin3C,0,unused"
        gq_stat.write(outline + "\n")

binstat_file = os.path.join(bin3Cdir, "02binstat", "bin_per_species.csv")
with open(binstat_file) as binstat:
    for line in binstat:
        outline = ""
        if line.startswith("contig_name"):
            outline = line.strip() + ",binmethod,final,group"
        else:
            contig_name = line.strip().split(',')[1]
            if contig_name in groupdic:
                group = groupdic[contig_name]
                outline = line.strip() + ",bin3C,1,{}".format(group)
            else:
                outline = line.strip() + ",bin3C,0,unused"
        bin_stat.write(outline + "\n")

metabat_bindirs = ["/home3/ZXMGroup/VIROME/G3compare/RealData/results"]
for metabat_bindir in metabat_bindirs:
    genomequality_file = os.path.join(metabat_bindir, "02binstat", "genome_quality.csv")
    os.system("python /home3/ZXMGroup/VIROME/G3compare/pipeline/05bin-stat.py {}".format(metabat_bindir))
    os.system("python /home3/ZXMGroup/VIROME/G3compare/pipeline/05bin-stat-bin3C.py {}".format(metabat_bindir))
    os.system("python /home3/ZXMGroup/VIROME/G3compare/pipeline/05bin_genome_quality.py {}".format(metabat_bindir))
    os.system("python /home3/ZXMGroup/VIROME/G3compare/pipeline/05bin_genome_quality_complete.py {}".format(metabat_bindir))
    os.system("python /home3/ZXMGroup/VIROME/G3compare/pipeline/05bin_genome_quality_high.py {}".format(metabat_bindir))
    with open(genomequality_file) as genomequality:
        for line in genomequality:
            outline = ""
            if line.startswith("contig_name"):
                outline = line.strip() + ",binmethod,final,group"
            else:
                contig_name = line.strip().split(',')[1]
                if contig_name in groupdic:
                    group = groupdic[contig_name]
                    outline = line.strip() + ",Metabat2,1,{}".format(group)
                else:
                    outline = line.strip() + ",Metabat2,0,unused"
            gq_stat.write(outline + "\n")

    binstat_file = os.path.join(metabat_bindir, "02binstat", "bin_per_species.csv")
    with open(binstat_file) as binstat:
        for line in binstat:
            outline = ""
            if line.startswith("contig_name"):
                outline = line.strip() + ",binmethod,final,group"
            else:
                contig_name = line.strip().split(',')[1]
                if contig_name in groupdic:
                    group = groupdic[contig_name]
                    outline = line.strip() + ",Metabat2,1,{}".format(group)
                else:
                    outline = line.strip() + ",Metabat2,0,unused"
            bin_stat.write(outline + "\n")
bin_stat.close()
gq_stat.close()