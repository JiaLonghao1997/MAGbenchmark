#!/bin/bash
#PBS -N bin_label_and_evaluate
#PBS -l nodes=2:ppn=8
#PBS -l walltime=999999:00:00

export PATH=/home1/jialh/tools/miniconda3/bin:$PATH

sample=$1
workdir=$2

configdir=${workdir}/configs

echo "begin to deal with ${sample}"
if [ -s ${configdir}/${sample}_config.yaml ] && [ ! -s ${workdir}/01binlabel/${sample}/final/${sample}.tsv ]
then
echo "${configdir}/${sample}_config.yaml exists."
mkdir -p ${workdir}/01binlabel
cd ${workdir}/01binlabel

/home1/jialh/tools/miniconda3/bin/snakemake \
-s /share/inspurStorage/home3/ZXMGroup/VIROME/G3compare/pipeline/bin_label_and_evaluate/bin3C_Snakefile \
--configfile ${configdir}/${sample}_config.yaml \
--restart-times 0 --keep-going --cores 32 --latency-wait 100 --rerun-incomplete

cd ${workdir}

elif  [ -s ${workdir}/01binlabel/${sample}/final/${sample}.tsv ]
then
  echo "${sample}/final/${sample}.tsv exists."
else
  echo "${workdir}/${configdir}/${sample}_config.yaml doesn't exist."
fi
#done