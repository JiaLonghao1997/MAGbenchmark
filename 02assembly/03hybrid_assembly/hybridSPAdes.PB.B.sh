#! /bin/bash
/home1/YQ_Dong/tools/SPAdes-3.15.2-Linux/bin/spades.py \
-o ../assemblies/hybridSPAdes/PacBio/new/B \
--meta \
--only-assembler \
--pe1-1 ../assemblies/hybridSPAdes/ONT/B/corrected/B_trim1.paired.fq.00.0_0.cor.fastq.gz \
--pe1-2 ../assemblies/hybridSPAdes/ONT/B/corrected/B_trim2.paired.fq.00.0_0.cor.fastq.gz \
--pe1-s ../assemblies/hybridSPAdes/ONT/B/corrected/B_trim_unpaired.00.0_0.cor.fastq.gz \
--pacbio /share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/RealData/PacBio/data_merge/B.fastq \
-t 50 -m 1000 \
-k 21,31,41,61,81,101,121
