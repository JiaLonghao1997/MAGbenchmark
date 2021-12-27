#! /bin/bash
time /home1/YQ_Dong/tools/SPAdes-3.15.2-Linux/bin/spades.py \
-o ../assemblies/metaSPAdes --meta \
-1 ../Reads/NGS/combined_trim_paired_R1.fq \
-2 ../Reads/NGS/combined_trim_paired_R2.fq \
-t 60 -m 1000 -k 21,31,41,61,81,101,121 \
