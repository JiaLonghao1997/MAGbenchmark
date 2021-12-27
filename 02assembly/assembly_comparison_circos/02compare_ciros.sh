#!/bin/bash
#PBS -N bin_label_and_evaluate
#PBS -l nodes=2:ppn=8
#PBS -l walltime=999999:00:00

export PATH=/home1/jialh/tools/miniconda3/bin:$PATH

#workdir="/home3/ZXMGroup/VIROME/G3compare/data/PRJNA380276/results/metagenomics_workflows/assembly_comparison_circos"
configdir="/home3/ZXMGroup/VIROME/G3compare/data/PRJNA380276/results/metagenomics_workflows/assembly_comparison_circos"

echo "begin to deal with compare circos genome."
if [ -s ${configdir}/config.yaml ]
then
  /home1/jialh/tools/miniconda3/bin/snakemake \
  -s /home3/ZXMGroup/VIROME/G3compare/data/PRJNA380276/results/metagenomics_workflows/assembly_comparison_circos/Snakefile \
  --configfile ${configdir}/config.yaml \
  --restart-times 0 --cores 16 --latency-wait 100 --rerun-incomplete
fi
