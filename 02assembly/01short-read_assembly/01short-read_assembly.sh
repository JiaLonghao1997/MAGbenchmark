#!/bin/bash
# need to be modified
set -o errexit
sample=$1
workdir=$2  # 原始rawdata存储路径
assembler=$3

##1.assemble by MEGAHIT
if [ ${assembler} == 'megahit' ];
then
  echo "begin to megahit ${sample}"
  mkdir -p ${workdir}/03megahit
  if [ -s ${workdir}/02_trim/${sample}_trim1.paired.fq.gz ] && [ -s ${workdir}/02_trim/${sample}_trim2.paired.fq.gz ] && [ ! -s ${workdir}/03megahit/${sample}/final.contigs.fa ];
  then
    rm -rf ${workdir}/03megahit/${sample}
    /share/inspurStorage/home1/jialh/tools/miniconda3/bin/megahit \
    -1 ${workdir}/02_trim/${sample}_trim1.paired.fq.gz \
    -2 ${workdir}/02_trim/${sample}_trim2.paired.fq.gz \
    --k-list 21,29,39,59,79,99,119,141 \
    --min-contig-len 1000 \
    -t 16 -o ${workdir}/03megahit/${sample} > ${workdir}/03megahit/${sample}.log
  elif [ -s ${workdir}/03megahit/${sample}/final.contigs.fa ]
  then
    echo ${workdir}/03megahit/${sample}/final.contigs.fa exits.
  fi
fi

##2.assemble by metaspades
if [ ${assembler} == 'metaSPAdes' ];
then
  echo "begin to metaspades ${sample}"
  mkdir -p ${workdir}/03metaspades/${sample}
  if [ -s ${workdir}/02_trim/${sample}_trim1.paired.fq.gz ] && [ -s ${workdir}/02_trim/${sample}_trim2.paired.fq.gz ] && [ ! -s ${workdir}/03metaspades/${sample}/contigs.fasta ];
  then
  /home1/jialh/tools/miniconda3/bin/spades.py \
  --meta -k 21,31,41,61,81,101,121 \
  -t 16 -m 800 \
  -1 ${workdir}/02_trim/${sample}_trim1.paired.fq.gz \
  -2 ${workdir}/02_trim/${sample}_trim2.paired.fq.gz \
  -o ${workdir}/03metaspades/${sample} > ${workdir}/03metaspades/${sample}.log
  else
    echo ${workdir}/03metaspades/${sample}/contigs.fasta exits.
  fi
fi

##3.assemble by IDBA-UD
if [ ${assembler} == 'idba-ud' ];
then
  echo "begin to idba-ud ${sample}"
  mkdir -p ${workdir}/03idba-ud/${sample}
  if [ -s ${workdir}/02_trim/${sample}_trim1.paired.fq.gz ] && [ -s ${workdir}/02_trim/${sample}_trim2.paired.fq.gz ];
  then
    if [ ! -s ${workdir}/03idba-ud/${sample}.reads.fa ];
    then
      zcat ${workdir}/02_trim/${sample}_trim1.paired.fq.gz > ${workdir}/03idba-ud/${sample}_1.fq

      zcat ${workdir}/02_trim/${sample}_trim2.paired.fq.gz > ${workdir}/03idba-ud/${sample}_2.fq

      /home1/jialh/human_virome/tools/idba/bin/fq2fa --merge --filter \
      ${workdir}/03idba-ud/${sample}_1.fq ${workdir}/03idba-ud/${sample}_2.fq ${workdir}/03idba-ud/${sample}.reads.fa
    else
      echo ${workdir}/03idba-ud/${sample}.reads.fa exits.
    fi

  /home1/jialh/human_virome/tools/idba/bin/idba_ud -r ${workdir}/03idba-ud/${sample}.reads.fa \
  -o ${workdir}/03idba-ud/${sample} --pre_correction --maxk 120 --mink 20 --step 20 --num_threads 16 > ${workdir}/03idba-ud/${sample}.log
  fi
fi