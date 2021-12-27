#!/bin/bash
set -o errexit
sample=$1
workdir=$2
rawdatadir=$3


Bowtie2=/home1/Laisenying/miniconda3/bin/bowtie2
Human_database=/home1/Laisenying/Tools/data/human/human2/hg38

# Step 0 quality control
echo "begin to deal with ${sample}"
mkdir -p ${workdir}/00_fastqc
mkdir -p ${workdir}/00_fastqc/${sample}
if
[ -s ${rawdatadir}/${sample}_R1.fq.gz ] && [ -s ${rawdatadir}/${sample}_R2.fq.gz ] && [ ! -s ${workdir}/00_fastqc/${sample}/${sample}_R1_fastqc.html ]
then
/home1/jialh/human_virome/tools/FastQC/fastqc -o ${workdir}/00_fastqc/${sample} \
-t 16 ${rawdatadir}/${sample}_R1.fq.gz ${rawdatadir}/${sample}_R2.fq.gz
fi

# Step 1 remove DNA from human host.
echo "begin to remove human sequence of ${sample}."
mkdir -p ${workdir}/01_rmhuman/${sample}
if
[ -s "${rawdatadir}/${sample}_R1.fq.gz" ] && [ -s "${rawdatadir}/${sample}_R2.fq.gz" ] && [ ! -s "${workdir}/01_rmhuman/${sample}_clean2.fq.gz" ];
then
$Bowtie2 -x $Human_database  \
    -p 16 \
    --very-sensitive \
    -1 ${rawdatadir}/${sample}_R1.fq.gz \
    -2 ${rawdatadir}/${sample}_R2.fq.gz \
    --un-conc-gz ${workdir}/01_rmhuman/${sample}_clean%.fq.gz \
    --al-conc-gz ${workdir}/01_rmhuman/${sample}_contam%.fq.gz > /dev/null 2>&1
#rm -rf ${workdir}/01_rmhuman/${sample}_contam1.fq.gz
#rm -rf ${workdir}/01_rmhuman/${sample}_contam2.fq.gz
elif [ -s ${workdir}/01_rmhuman/${sample}_clean2.fq.gz ]
then
  echo ${workdir}/01_rmhuman/${sample}_clean2.fq.gz exits.
fi

## Step 2 remove adapters.
echo "begin to remove adapters of ${sample}."
mkdir -p ${workdir}/02_trim
if [ -s "${workdir}/01_rmhuman/${sample}_clean1.fq.gz" ] && [ -s "${workdir}/01_rmhuman/${sample}_clean2.fq.gz" ] && [ ! -s "${workdir}/02_trim/${sample}_trim2.paired.fq.gz" ];
then
java -jar /home1/jialh/human_virome/tools/Trimmomatic-0.39/trimmomatic-0.39.jar PE -threads 16 \
${workdir}/01_rmhuman/${sample}_clean1.fq.gz \
${workdir}/01_rmhuman/${sample}_clean2.fq.gz \
${workdir}/02_trim/${sample}_trim1.paired.fq.gz ${workdir}/02_trim/${sample}_trim1.unpaired.fq.gz \
${workdir}/02_trim/${sample}_trim2.paired.fq.gz ${workdir}/02_trim/${sample}_trim2.unpaired.fq.gz \
ILLUMINACLIP:/home1/jialh/microbiome/metaHiC/pipeline/adapters.fa:2:40:15 \
LEADING:3 TRAILING:3 \
SLIDINGWINDOW:4:15 \
MINLEN:25
fi