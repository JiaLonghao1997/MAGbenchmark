#! /bin/bash
/home1/YQ_Dong/tools/SPAdes-3.15.2-Linux/bin/spades.py \
-o ../assemblies/hybridSPAdes/ONT/F \
--meta \
-1 /share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/G2/02_trim/F_trim1.paired.fq.gz \
-2 /share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/G2/02_trim/F_trim2.paired.fq.gz \
--nanopore /share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/RealData/Nanopore/data/F.fastq \
-t 70 -m 900 \
-k 21,31,41,61,81,101,121
