#! /bin/bash
metaquast -o ./ -r ../../Ref/Acinetobacter_baumannii.fna,../../Ref/Bifidobacterium_adolescentis.fasta,../../Ref/Bifidobacterium_longum.fasta,../../Ref/Capnocytophaga_ochracea.fasta,../../Ref/Enterobacter_cloacae.fasta,../../Ref/Enterococcus_faecium.fasta,../../Ref/Finegoldia_magna.fasta,../../Ref/Fusobacterium_nucleatum_subsp.polymorphum.fna,../../Ref/Helicobacter_cinaedi.fasta,../../Ref/Jonquetella_anthropi.fna,../../Ref/Klebsiella_pneumoniae.fasta,../../Ref/Lactobacillus_reuteri.fasta,../../Ref/Parascardovia_denticolens.fna,../../Ref/Prevotella_oris.fna,../../Ref/Salmonella_enterica_subsp.enterica_serovar_typhimurium.fna,../../Ref/Staphylococcus_epidermidis.fasta,../../Ref/Streptococcus_parasanguinis.fasta \
-t 20 -l IDBA-UD,MegaHit,MetaSPAdes,Canu_ONT,Canu_PB,wtdbg2_ONT,wtdbg2_PB,MetaFlye_ONT,MetaFlye_PB,hybridSPAdes_ONT,hybridSPAdes_PB,OPERA-MS_ONT,OPERA-MS_PB -a all \
--fragmented -1 ../../NGS/ERR3200809_1_trim_paired.fastq -2 ../../NGS/ERR3200809_2_trim_paired.fastq --no-read-stats \
../../assemblies/IDBA-UD/contig.pilon.filter.fasta \
../../assemblies/MEGAHIT/final.contigs.pilon.filter.fasta \
../../assemblies/metaSPAdes/contigs.pilon.filter.fasta \
/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/GIS20/bestcontigs/S1_Nanopore_canu+50m+100m+polish.fa \
/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/GIS20/bestcontigs/S1_PacBio_canu+20m+40m+polish.fa \
/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/GIS20/bestcontigs/S1_Nanopore_wtdbg2+40m+80m+polish.fa \
/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/GIS20/bestcontigs/S1_PacBio_wtdbg2+40m+80m+polish.fa \
/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/GIS20/bestcontigs/S1_Nanopore_metaflye+100m+250m+polish.fa \
/share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/GIS20/bestcontigs/S1_PacBio_metaflye+40m+100m+polish.fa \
../../assemblies/hybridSPAdes/ONT/contigs.pilon.filter.fasta \
../../assemblies/hybridSPAdes/Pacbio/contigs.pilon.filter.fasta \
../../assemblies/OPERA-MS/ONT/metaSPAdes/contigs.pilon.filter.fasta \
../../assemblies/OPERA-MS/Pacbio/metaSPAdes/contigs.pilon.filter.fasta
