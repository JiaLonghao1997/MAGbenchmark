tabfile=$1
bedfile=$2
awk 'BEGIN {FS="\t"} $3>95 {print $1 "\t" $7 "\t" $8 }'  ${tabfile} |sort -k 1 -t $'\t' |sed 's/[[:space:]]*$//'|tr -d " "|sort -k1,1 -k2,2n > ${bedfile}.1
/home1/jialh/ML/PPFinder/tools/bedtools2/bin/bedtools merge -i ${bedfile}.1 > ${bedfile}
