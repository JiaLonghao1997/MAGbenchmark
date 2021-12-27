#! /bin/bash
perl /home1/YQ_Dong/tools/OPERA-MS-OPERA-MS-0.9.0/OPERA-MS.pl \
--short-read1 /home3/ZXMGroup/VIROME/G3compare/G2/02_trim/A_trim1.paired.fq.gz \
--short-read2 /home3/ZXMGroup/VIROME/G3compare/G2/02_trim/A_trim2.paired.fq.gz \
--long-read /home3/ZXMGroup/VIROME/G3compare/RealData02/00fastq/A_Nanopore_3200000.fastq \
--out-dir ../subsample/ONT/Nanopore_3200000/A \
--no-polishing --num-processors 20 \
--contig-file /home3/ZXMGroup/VIROME/G3compare/G2/03metaspades/A/contigs.fasta
