#! /bin/bash
perl /home1/YQ_Dong/tools/OPERA-MS-OPERA-MS-0.9.0/OPERA-MS.pl \
--short-read1 /home3/ZXMGroup/VIROME/G3compare/G2/02_trim/F_trim1.paired.fq.gz \
--short-read2 /home3/ZXMGroup/VIROME/G3compare/G2/02_trim/F_trim2.paired.fq.gz \
--long-read /home3/ZXMGroup/VIROME/G3compare/RealData/Nanopore/data/F.fastq \
--out-dir ../assemblies/OPERA-MS/ONT/F \
--no-polishing --num-processors 20 \
--contig-file /home3/ZXMGroup/VIROME/G3compare/G2/03metaspades/F/contigs.fasta
