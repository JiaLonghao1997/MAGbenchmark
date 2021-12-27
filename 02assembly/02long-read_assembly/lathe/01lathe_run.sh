#!/bin/bash
#PBS -N bin_label_and_evaluate
#PBS -l nodes=2:ppn=8
#PBS -l walltime=999999:00:00

export PATH=/share/inspurStorage/home1/jialh/tools/miniconda3/bin:$PATH
export PATH=/share/inspurStorage/home1/jialh/human_virome/tools/Flye/bin/flye:$PATH
export PATH=/share/inspurStorage/home1/jialh/tools/samtools-1.9/samtools:$PATH
export PATH=/home1/caojx/wgs_tool/bcftools-1.10.2/htslib-1.10.2/bin:$PATH

workdir="/home3/ZXMGroup/VIROME/G3compare/GIS20/TGS/ONT/lathe"

echo "begin to run lathe"
if [ -s ${workdir}/config.yaml ]
then
/home1/jialh/tools/miniconda3/bin/snakemake \
-s /home3/ZXMGroup/VIROME/G3compare/pipeline/lathe/Snakefile \
--configfile ${workdir}/config.yaml --restart-times 0  --cores 32 --latency-wait 300 --rerun-incomplete
fi