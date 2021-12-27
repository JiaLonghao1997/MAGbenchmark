#!/bin/bash
#SBATCH --cpus-per-task=16
#SBATCH -o slurm.%N.%j.out        # STDOUT
#SBATCH -e slurm.%N.%j.err        # STDERR

infile=$1
NGS_PATH=$2
G3_PATH=$3
Software='/mnt/raid6/sunchuqing/Softwares'
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/local/lib:/mnt/raid6/sunchuqing/Softwares/MCR/v94/runtime/glnxa64:/mnt/raid6/sunchuqing/Softwares/MCR/v94/sys/os/glnxa64:/mnt/raid6/sunchuqing/Softwares/MCR/v94/extern/glnxa64：/mnt/raid3/wchen/miniconda2/pkgs/libgcc-7.2.0-h69d50b8_2/lib
cd G3
mkdir -p 01_ccs 02_Removed/${infile}
#Run CCS corrction
CCS=`ls ${G3_PATH}/*${infile}*.subreads.bam `
if [ ! -s 02_Removed/${infile}/${infile}.virome.fastq ];then
  if [ ! -s ${G3_PATH}/CCS/${infile}.subreads.bam ];then
    ${Software}/miniconda3/bin/ccs ${CCS} 01_ccs/${infile}.ccs.fastq -j 16
  else 
    CCS=`ls ${G3_PATH}/CCS/${infile}.subreads.bam`
    bedtools bamtofastq -i ${CCS} -fq 01_ccs/${infile}.ccs.fastq
  fi
  #Remove human genome
  bowtie2 -p 16 --un 02_Removed/${infile}/${infile}.fastq  -x /mnt/raid5/sunchuqing/Human_Gut_Phage/ref/hg38_ref -U 01_ccs/${infile}.ccs.fastq  > log
  bowtie2 --end-to-end -x /mnt/raid7/sunchuqing/Human_Gut_Phage/db/HGYG_prophage -U 02_Removed/${infile}/${infile}.fastq -S ../04_Abundance/${infile}_G3_HGYG_prophage.sam -p 16 --al 02_Removed/${infile}/${infile}.prophage.fastq --quiet
  bowtie2 --end-to-end -x /mnt/raid7/sunchuqing/Human_Gut_Phage/db/HGYG -U 02_Removed/${infile}/${infile}.fastq -S ../04_Abundance/${infile}_G3_HGYG.sam -p 16 --un 02_Removed/${infile}/${infile}.phage.fastq --quiet
  cat 02_Removed/${infile}/${infile}.prophage.fastq 02_Removed/${infile}/${infile}.phage.fastq > 02_Removed/${infile}/${infile}.virome.fastq
  seqtk seq -a 02_Removed/${infile}/${infile}.virome.fastq  | /mnt/raid6/sunchuqing/Softwares/miniconda3/bin/seqkit rmdup -s -o  02_Removed/${infile}/${infile}.fa
  rm 02_Removed/${infile}/${infile}.*hage.fastq 02_Removed/${infile}/${infile}.fastq
fi


#Assembly with Canu
rm -rf 03_canu_Assembly/${infile}
mkdir -p 03_canu_Assembly/${infile}
G3=`pwd`
cd 03_canu_Assembly/${infile}
host=`hostname`
if [ "$host" = "bork" ];then 
    /mnt/raid7/sunchuqing/Softwares/OPERAMS-bork/canu/build/bin/canu  \
      -p ${infile} \
      -d ./ genomeSize=20k corOutCoverage=1 \
      -corrected \
      -pacbio ../../02_Removed/${infile}/${infile}.fa  \
      useGrid=false
else
    /mnt/raid6/sunchuqing/Softwares/canu/Linux-amd64/bin/canu  \
      -p ${infile} \
      -d ./ genomeSize=20k corOutCoverage=1 \
      -corrected \
      -pacbio ../../02_Removed/${infile}/${infile}.fa  \
      useGrid=false
fi

cd ${G3}

#Assembly with Flye
mkdir -p 03_Flye_Assembly/${infile}
mkdir -p 05_Assembly/${infile}
zcat 03_canu_Assembly/$infile/${infile}.trimmedReads.fasta.gz >03_canu_Assembly/$infile/${infile}.trimmedReads.fasta
flye --pacbio-corr  02_Removed/${infile}/${infile}.fa \
  --meta --genome-size 20k \
  --out-dir 03_Flye_Assembly/${infile}/ \
  --threads 16  --min-overlap 1000
cat 03_canu_Assembly/${infile}/${infile}.contigs.fasta 03_Flye_Assembly/${infile}/assembly.fasta > 05_Assembly/${infile}_fc.fa

#Binning with MetaBAT
if [ -s 03_canu_Assembly/${infile}/${infile}.unitigs.fasta ];then
  mkdir -p 04_MetaBAT_Assembly/${infile}
  cd 04_MetaBAT_Assembly/${infile}
  mkdir -p db
  bowtie2-build ../../03_canu_Assembly/${infile}/${infile}.unitigs.fasta db/${infile}
  bowtie2 -x db/${infile} -U ../../01_ccs/${infile}.ccs.fastq -S ${infile}.sam
  /mnt/raid6/sunchuqing/Softwares/miniconda3/bin/samtools view -bS ${infile}.sam -o ${infile}.bam
  /mnt/raid6/sunchuqing/Softwares/miniconda3/bin/samtools sort ${infile}.bam > ${infile}.sort.bam
  ${Software}/berkeleylab-metabat*/bin/jgi_summarize_bam_contig_depths --outputDepth depth_var.txt ${infile}.sort.bam
  ${Software}/berkeleylab-metabat*/bin/metabat -i ../../03_canu_Assembly/${infile}/${infile}.unitigs.fasta -a depth_var.txt  -o metabat -v 

  for file in ./metabat.*.fa
    do
      num=${file//[!0-9]/}
      #echo $num
      sed -e "/^>/ s/$/ ${num}/" metabat.$num.fa  >> metabat_binned.concat.fasta 
  done
  grep '>' metabat_binned.concat.fasta | sed 's/>//g' > metabat_binned.info


#需要先对基因组进行组装和完整基因组的筛选
  
  cd ../../05_Assembly/${infile}
  cut -f1 ../../03_canu_Assembly/${infile}/${infile}.unitigs.bed | sort|uniq -c > contig.list
  while read -r contig
  do
    num=`echo ${contig} | awk 'BEGIN {FS=" "} {print $1}'`
    tig=`echo ${contig} | awk 'BEGIN {FS="ctg"} {print $2}'`
    if [ $num -eq 1 ];then
      awk '/^>/ {printf("\n%s\t",$0);next;} {printf("%s",$0);} END {printf("\n");}' < ../../03_canu_Assembly/${infile}/${infile}.contigs.fasta |egrep -v '^$'|tr "\t" "\n" >../../03_canu_Assembly/${infile}/${infile}.n1.contigs.fasta
      grep "$tig" ../../03_canu_Assembly/${infile}/${infile}.n1.contigs.fasta -A 1|sed 's/>tig/>ctg/g' >> ../${infile}.fasta
      echo $tig >> infa.contig.list  
      grep "ctg${tig}" ../../03_canu_Assembly/${infile}/${infile}.unitigs.bed |cut -f4 >>infa.unitig.list
    else
      grep "ctg${tig}" ../../03_canu_Assembly/${infile}/${infile}.unitigs.bed |cut -f4 >unitig.list
      sed 's/utg/tig/g' unitig.list > uni.list
      binnum=`grep -Ff uni.list ../../04_MetaBAT_Assembly/${infile}/metabat_binned.info | awk 'BEGIN {FS=" "} {print $2}' |sort |uniq |wc -l`
      inbin=`grep -Ff uni.list ../../04_MetaBAT_Assembly/${infile}/metabat_binned.info|wc -l`
      uninum=`cat unitig.list | wc -l `
      #echo "$binnum,$uninum,${inbin}"
      if [[ $binnum == 1 && $uninum == $inbin ]];then
      
        grep "$tig" ../../03_canu_Assembly/${infile}/${infile}.contigs.fasta -A 100| awk -v RS='>' 'NR>1{i++}i==1{print ">"$0}' >> ../${infile}.fasta
        echo $tig >> infa.contig.list
        cat unitig.list >> infa.unitig.list
      fi
    fi
  
  done <"contig.list" 
  cut -f4 ../../03_canu_Assembly/${infile}/${infile}.unitigs.bed >unitig.list 
  awk '/^>/ {printf("\n%s\t",$0);next;} {printf("%s",$0);} END {printf("\n");}' < ../../03_canu_Assembly/${infile}/${infile}.unitigs.fasta |egrep -v '^$'|tr "\t" "\n" >../../03_canu_Assembly/${infile}/${infile}.n1.unitigs.fasta
  for unitig in `grep -v -Ff infa.unitig.list unitig.list `
  do
    tig=`echo ${unitig} | awk 'BEGIN {FS="utg"} {print $2}'`
    #echo $tig
    grep "$tig" ../../03_canu_Assembly/${infile}/${infile}.n1.unitigs.fasta -A 1 | sed 's/class=contig/class=unitig/g'|sed 's/>tig/>utg/g' >> ../${infile}.fasta
  done
  cat ../../03_Flye_Assembly/${infile}/assembly.fasta ../${infile}.fasta > ../${infile}_fc.fa
  cd ../..
fi
mkdir -p 06_CD-HIT/${infile}
/mnt/raid6/sunchuqing/Softwares/cdhit-master/cd-hit-est -i 05_Assembly/${infile}_fc.fa -o 06_CD-HIT/${infile}/${infile}.fa -c 0.95 -n 5 -T 16 -M 16000 


#使用Pilon对组装数据进行polish
#假设你的组装文件为draft.fa, 质量控制后的illumina双端测序数据分别为read_1.fq.gz和read_2.fq.gz
Software='/mnt/raid6/sunchuqing/Softwares'
PATH="/mnt/raid6/sunchuqing/Softwares/miniconda3/bin":$PATH
if [ -s ${NGS_PATH}/*${infile}*R1* ];then
  if [ ! -s ../NGS/02_trimmed/*${infile}*clean.1.fq ];then
    TRIMMO_JAR_FILE='/mnt/raid1/tools/ngs_tools/Trimmomatic-0.38/trimmomatic-0.38.jar'
    TRIMMO_ADAPTOR_FILE_PE='/mnt/raid1/tools/ngs_tools/Trimmomatic-0.38/adapters/TruSeq3-PE.fa'
    R1=`ls ${NGS_PATH}/*${infile}*R1*`
    R2=`ls ${NGS_PATH}/*${infile}*R2*`
    mkdir -p ../NGS/02_trimmed
    java -jar $TRIMMO_JAR_FILE PE -threads 4 $R1 $R2 ../NGS/02_trimmed/${infile}_clean.1.fq ../NGS/02_trimmed/${infile}_clean_unpaired.1.fq ../NGS/02_trimmed/${infile}_clean.2.fq ../NGS/02_trimmed/${infile}_clean_unpaired.2.fq ILLUMINACLIP:$TRIMMO_ADAPTOR_FILE_PE:2:15:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:15:30 MINLEN:50
  fi
  mkdir -p 07_Pilon/${infile}
  cd 07_Pilon/${infile}
  mkdir -p index
  bwa index -p index/draft ../../06_CD-HIT/${infile}/${infile}.fa
  R1=`ls ../../../NGS/02_trimmed/*${infile}*clean.1.fq`
  R2=`ls ../../../NGS/02_trimmed/*${infile}*clean.2.fq`
  bwa mem -t 16 index/draft ${R1} ${R2} | /mnt/raid6/sunchuqing/Softwares/miniconda3/bin/samtools sort -@ 10 -O bam -o align.bam
  /mnt/raid6/sunchuqing/Softwares/miniconda3/bin/samtools index -@ 10 align.bam
  /mnt/raid6/sunchuqing/Softwares/miniconda3/bin/samtools sort -n align.bam > align.sort.bam
  /mnt/raid6/sunchuqing/Softwares/miniconda3/bin/samtools fixmate -m align.sort.bam fixmate.bam
  /mnt/raid6/sunchuqing/Softwares/miniconda3/bin/samtools sort -o align.som.bam fixmate.bam
  /mnt/raid6/sunchuqing/Softwares/miniconda3/bin/samtools markdup align.som.bam align_markdup.bam
  /mnt/raid6/sunchuqing/Softwares/miniconda3/bin/samtools view -@ 10 -q 30 -b align_markdup.bam > align_filter.bam
  /mnt/raid6/sunchuqing/Softwares/miniconda3/bin/samtools index -@ 10 align_filter.bam
  #MEMORY= #根据基因组大小而定
  java -Xmx5G -jar ${Software}/pilon-1.23.jar --genome ../../06_CD-HIT/${infile}/${infile}.fa --frags align_filter.bam \
      --fix snps,indels \
      --output ${infile}.pilon 
  cd ../..
fi
cd ..