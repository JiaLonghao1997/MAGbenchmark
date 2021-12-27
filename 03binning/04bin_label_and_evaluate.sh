#!/bin/bash
#PBS -N bin_label_and_evaluate
#PBS -l nodes=2:ppn=8
#PBS -l walltime=999999:00:00

export PATH=/home1/jialh/tools/miniconda3/bin:$PATH

sample=$1
workdir=$2
method=$3
assembler=$4

configdir=${workdir}/configs

echo "begin to deal with ${sample}"
if [ -s ${configdir}/${sample}_config.yaml ] && [ ! -s ${workdir}/01binlabel/${sample}/final/${sample}.tsv ]
then
echo "${workdir}/${sample}_config.yaml exists."
mkdir -p ${workdir}/01binlabel
cd ${workdir}/01binlabel

/home1/jialh/tools/miniconda3/bin/snakemake \
-s /home3/ZXMGroup/VIROME/G3compare/pipeline/bin_label_and_evaluate/${method}_Snakefile \
--configfile ${configdir}/${sample}_config.yaml \
--restart-times 0 --keep-going --cores 16 --latency-wait 100 --forcerun

cd ${workdir}

elif  [ -s ${workdir}/01binlabel/${sample}/final/${sample}.tsv ]
then
  echo "${sample}/final/${sample}.tsv exists."
else
  echo "${workdir}/${sample}_config.yaml doesn't exist."
fi
#done