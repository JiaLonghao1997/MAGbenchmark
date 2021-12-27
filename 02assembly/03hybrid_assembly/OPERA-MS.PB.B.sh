#! /bin/bash
perl /home1/YQ_Dong/tools/OPERA-MS-OPERA-MS-0.9.0/OPERA-MS.pl \
--short-read1 /home3/ZXMGroup/VIROME/G3compare/G2/02_trim/B_trim1.paired.fq.gz \
--short-read2 /home3/ZXMGroup/VIROME/G3compare/G2/02_trim/B_trim2.paired.fq.gz \
--long-read /home3/ZXMGroup/VIROME/G3compare/RealData/PacBio/data_merge/B.fastq \
--out-dir ../assemblies/OPERA-MS/Pacbio/B \
--no-polishing --num-processors 20 \
--contig-file /home3/ZXMGroup/VIROME/G3compare/G2/03metaspades/B/contigs.fasta
