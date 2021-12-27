#!/bin/bash

outdir=$1
binfile=$2
binname=$3

##(1)CRISPR序列识别
CRISPRdir=${outdir}/01crispr
mkdir -p ${CRISPRdir}
if [ -s ${binfile} ] && [ ! -f ${CRISPRdir}/${binname}.txt ]
then
  echo "CRISPR for ${CRISPRdir}"
  /home1/jialh/tools/miniconda3/bin/java -cp /home1/jialh/human_virome/tools/CRISPR_Recognition_Tool/CRT1.2-CLI.jar crt ${binfile} ${CRISPRdir}/${binname}.txt
fi

#(2) 抗生素耐药性基因预测
#makeblastdb -dbtype nucl -in nucleotide_fasta_protein_homolog_model.fasta -input_type fasta -out CARDnucl
ARGdir=${outdir}/02ARG/${binname}
mkdir -p ${ARGdir}
if [ -s ${binfile} ] && [ ! -f ${ARGdir}/card.m8.tab ]
then
  echo "blastn ARG for ${ARGdir}"
  /home1/jialh/tools/miniconda3/bin/blastn -query ${binfile} \
  -db /home1/jialh/human_virome/tools/00BacAnnotation/arg-annot/ARG-Annot.fasta \
  -out ${ARGdir}/card.m8.tab \
  -outfmt 6 -evalue 1e-5 -num_threads 2
fi

##(3) 毒力因子预测
##makeblastdb -dbtype nucl -in VFDB_setA_nt.fas -input_type fasta -out VFDB_setA_nt.fas
VFdir=${outdir}/03VF/${binname}
mkdir -p ${VFdir}
if [ -s ${binfile} ] && [ ! -f  ${VFdir}/vfdb.m8.tab ]
then
  echo "blastn VFDB for ${VFdir}"
  /home1/jialh/tools/miniconda3/bin/blastn -query ${binfile} \
  -db /home1/jialh/human_virome/tools/00BacAnnotation/VFDB/VFDB_setA_nt.fas \
  -out ${VFdir}/vfdb.m8.tab \
  -outfmt 6 -evalue 1e-5 -num_threads 2
fi

#(4)prophage识别
prophagedir=${outdir}/04prophage/${binname}
mkdir -p ${prophagedir}
if [ -s ${binfile} ] && [ ! -f ${outdir}/04prophage/${binname}/final-viral-score.tsv ]
then
  echo "virsorter for ${prophagedir}"
  rm -rf ${prophagedir}/iter-0
  mkdir -p ${prophagedir}/iter-0
  #export PATH=/share/inspurStorage/home1/jialh/tools/miniconda3/envs/vs2/bin:$PATH
  /share/inspurStorage/home1/jialh/tools/miniconda3/envs/vs2/bin/python \
  /share/inspurStorage/home1/jialh/tools/miniconda3/envs/vs2/bin/virsorter run \
  -w ${prophagedir} -i ${binfile} --min-length 1500 -j 2 all
fi

#vibrant病毒识别
vibrantdir=${outdir}/04vibrant/${binname}
mkdir -p ${vibrantdir}
binname_split=${binname%.fa*}
if [ -s ${binfile} ] && [ ! -f ${vibrantdir}/VIBRANT_${binname_split}/${binname_split}.prodigal.faa ]
then
  echo "vibrantdir for ${vibrantdir}"
  rm -rf ${vibrantdir}
  ###要求输入序列至少含有4个ORFs, 不满足这个要求的bins，无法处理。
  export PATH=/share/inspurStorage/home1/jialh/tools/miniconda3/envs/vibrant/bin:$PATH
  /share/inspurStorage/home1/jialh/tools/miniconda3/envs/vibrant/bin/python3 \
  /share/inspurStorage/home1/jialh/tools/miniconda3/envs/vibrant/bin/VIBRANT_run.py \
  -i ${binfile} -folder ${vibrantdir}
fi

####(4.2)质粒预测
mob_suitedir=${outdir}/04mob_suite/${binname}
if [ -s ${binfile} ] && [ ! -f ${mob_suitedir}/contig_report.txt ]
then
  echo "mob_suite for ${mob_suitedir}"
  rm -rf ${mob_suitedir}
  mkdir -p ${mob_suitedir}
  #export PATH=/home1/YQ_Dong/miniconda3/envs/mob-suite/bin:$PATH
  /home1/YQ_Dong/miniconda3/envs/mob-suite/bin/python \
  /home1/YQ_Dong/miniconda3/envs/mob-suite/bin/mob_recon \
  -i ${binfile} -o ${mob_suitedir} --force
fi

###plasmidfinder预测
plasmidfinder_dir=${outdir}/04plasmidfinder/${binname}
mkdir -p ${plasmidfinder_dir}
if [ -s ${binfile} ] && [ ! -f  ${plasmidfinder_dir}/data.json ];
then
  echo "plasmidfinder for ${plasmidfinder_dir}"
  /home1/jialh/tools/miniconda3/bin/python /home3/ZXMGroup/MGEs_database/tools/plasmidfinder/plasmidfinder.py \
  -i ${binfile} -p /home3/ZXMGroup/MGEs_database/tools/plasmidfinder/plasmidfinder_db -o ${plasmidfinder_dir}
fi

####(5)次级代谢基因的注释
#antismashdir=${outdir}/05antismash
#mkdir -p ${antismashdir}
#echo "antismash for ${antismashdir}"
#if [ -s ${binfile} ]
#then
#/home1/jialh/human_virome/tools/antismash5/run_antismash \
#${binfile} ${antismashdir} \
#--cb-general --cb-knownclusters --cb-subclusters --asf --pfam2go --smcog-trees \
#--genefinding-tool prodigal -c 4 > ${antismashdir}/antismash.log 2>&1
#fi