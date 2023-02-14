# Critical assessment of genome-resolved gut metagenomics on short-, long-read and metaHiC sequencing data

Recovering high-quality metagenome-assembled genomes (HQ-MAGs) is critical for exploring microbial compositions and microbe-phenotype associations. However, multiple sequencing platforms and computational tools for this purpose may confuse researchers and thus call for extensive evaluation. 

We systematically evaluated a total of **40** combinations of popular computational tools and sequencing platforms (i.e., strategies), involving **eight assemblers, eight metagenomic binners, and four sequencing technologies**, including short-, long-read and metaHiC sequencing. We identified the best tools for the individual tasks (e.g., the assembly and binning) and combinations (e.g., for generating more HQ-MAGs) depending on the availability of the sequencing data. 

Depending on the data availability, we found that the combination of the hybrid assemblies and metaHiC-based binning performed best, followed by the hybrid and long-read assemblies. More importantly, both long-read and metaHiC sequencings link more mobile elements and antibiotic resistance genes to bacterial hosts and improve the quality of public human gut reference genomes with 32% (34/105) HQ-MAGs that were either of better quality than those in the UHGG2 or novel.

![Figure 1](https://github.com/JiaLonghao1997/MAGbenchmark/blob/main/Figure%201.jpg)

#### 1. Preprocess

- Trim the adapter regions and low-quality reads: [**Trimmomatic v.039**](http://www.usadellab.org/cms/?page=trimmomatic)  (using LEADING:3 TRAILING:3, SLIDINGWINDOW:4:15, MINLEN:25)
- Remove human reads: Filtered reads were aligned to the human genome (NCBI, hg38) using [**Bowtie2**](http://bowtie-bio.sourceforge.net/bowtie2/manual.shtml).

#### 2. Assemblies

##### 2.1 Short-read assemblies

- [**IDBA-UD**](http://www.cs.hku.hk/~alse/idba_ud) v.1.1.3 (using --pre_correction --maxk 120 --mink 20 --step 20).
- **[MEGAHIT](https://github.com/voutcn/megahit)** v.1.2.9 (using --k-list 21,29,39,59,79,99,119,141)
- [**metaSPAdes**](https://github.com/ablab/spades) v.3.14.1(using --meta -k 21,31,41,61,81,101,121)

##### 2.2 Long-read assemblies

- **[Canu](https://github.com/marbl/canu)** v.2.0 (using genomeSize=50m/100m)
- **[metaFlye](https://github.com/fenderglass/Flye)** v. 2.7 (using –meta –g 100m/250m)
- **[wtdbg2](https://github.com/ruanjue/wtdbg2)** v.2.5 (using genomesize=50m/100m) 

Two long-read assembled contigs were then merged by [**quickmerge**](https://github.com/mahulchak/quickmerge) v.0.40  as previous described in **[Lathe](https://github.com/bhattlab/lathe)**, which is a tool for generating bacterial genomes from metagenomes with Nanopore long read sequencing.  

##### 2.3 Hybrid assemblies

- [**OPERA-MS**](https://github.com/CSB5/OPERA-MS) v.0.9.0 (using --no-polishing)
- [**hybridSPAdes**](https://github.com/ablab/spades) v.3.14.1 (using --meta -k 21,31,41,61,81,101,121)

##### 2.4 Polish and evaluation of metagenomic assemblies

- Polish: **[Pilon](https://github.com/broadinstitute/pilon)** v.1.24 
- Evaluation of metagenomic assemblies: **[MetaQUAST](http://quast.sourceforge.net/metaquast)** v.5.0.2
- **[Circos Assembly Comparison Visualization Workflow](https://github.com/elimoss/metagenomics_workflows/tree/master/assembly_comparison_circos)** are from public available scripts. 

#### 3. Binning

##### 3.1 Similarity-based binners

- [**MetaBAT2**](https://bitbucket.org/berkeleylab/metabat/src/master/) v.2.15 (--minContig 2500 --minContigDepth 1 --percentIdentity 97) 
- [**metaWRAP**](https://github.com/bxlab/metaWRAP) v.1.3.2
- [**DAS_Tool**](https://github.com/cmks/DAS_Tool) v. 1.1.4
- [**VAMB**](https://github.com/RasmussenLab/vamb) v. 3.0.2
- [**SemiBin**](https://github.com/BigDataBiology/SemiBin/ ) v.1.0.0

##### 3.2 MetaHiC-based binners

-   [**bin3C**](https://github.com/cerebis/bin3C) v.0.1.1
-   [**MetaTOR**](https://github.com/koszullab/metaTOR) v. 1.1.4
-   [**HiCBin**](https://github.com/dyxstat/HiCBin) v.1.0.0

##### 3.3 Generation and quality evaluation of MAGs

**[bin_label_and_evaluate](https://github.com/elimoss/metagenomics_workflows)** is a public available Snakemake workflow for aligning, binning, classifying and evaluating a metagenomic assembly. We  modified some of the scripts to make it suitable for bin3C binning.

- Assembly size and contiguity: **[MetaQUAST](http://quast.sourceforge.net/metaquast)** v.5.0.2
- Completeness and contamination: [**CheckM**](https://ecogenomics.github.io/CheckM/) v.1.1.3
- Gene Content: **[Prokka](https://github.com/tseemann/prokka)** v.1.14.6
- tRNA sequences:  [**Aragorn**](http://www.ansikte.se/ARAGORN/) v.1.2.38
- Ribosomal RNA loci:  [**Barrnap**](https://github.com/tseemann/barrnap) v.0.9
- Taxonomic classification: [**GTDB-tk**](https://github.com/Ecogenomics/GTDBTk) v1.4.1.

#### 4. tRNA and rRNA

The close reference genome of MAG was determined by  [**GTDB-tk**](https://github.com/Ecogenomics/GTDBTk) v.1.4.1. 

 tRNA and rRNA genes of MAGs and reference genomes were identified as previously mentioned. 

#### 5. extrachromosomal mobile genetic elements (eMGEs)

- Phages: [**VirSorter2**](https://github.com/jiarong/VirSorter2) v.2.1(using --min-length 1500 all) and [**CheckV**](https://bitbucket.org/berkeleylab/checkv/src/master/) v0.8.1 (using end_to_end) 
- Plasmids: **[MOB-suite](https://github.com/phac-nml/mob-suite)** v.3.0.0
- Antibiotic resistance genes: [**ARG-ANNOT**](https://www.mediterranee-infection.com/acces-ressources/base-de-donnees/arg-annot-2/) and [**BLASTN**](https://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs).

#### 6. References

1. Kuleshov V, Jiang C, Zhou W, Jahanbani F, Batzoglou S, Snyder M. Synthetic long-read sequencing reveals intraspecies diversity in the human microbiome. Nat Biotechnol 2016, 34:64-69.
2. Bishara A, Moss EL, Kolmogorov M, Parada AE, Weng Z, Sidow A, Dekas AE, Batzoglou S, Bhatt AS. High-quality genome sequences of uncultured microbes by assembly of read clouds. Nat Biotechnol 2018.
3. Moss EL, Maghini DG, Bhatt AS. Complete, closed bacterial genomes from microbiomes using nanopore sequencing. Nat Biotechnol 2020, 38:701-707.
