workdir=$1
mkdir -p ${workdir}/final

(echo 'Bin tRNA' | tr ' ' '\t';
ls ${workdir}/rna/trna/ | xargs -n 1 -I foo sh -c "grep 'Number of' ${workdir}/rna/trna/foo | cut -f2 -d= | tr -d ' ' | tr '\\n' '+' | sed 's/+$//g' | xargs echo | bc | sed 's/^/foo\t/g' " | sed 's/.fa.txt//g') > ${workdir}/final/trna.tmp;

echo "(echo 'Sample Bin tRNA' | tr ' ' '\t';
ls ${workdir}/rna/trna/ | xargs -n 1 -I foo sh -c "grep 'Number of' ${workdir}/rna/trna/foo | cut -f2 -d= | tr -d ' ' | tr '\\n' '+' | sed 's/+$//g' | xargs echo | bc | sed 's/^/foo\t/g' " | sed 's/^/${workdir}\\t/g' | sed 's/.fa.txt//g') > ${workdir}/final/trna.tmp;"

grep -c 16S ${workdir}/rna/rrna/* | sed 's/\/rna\/rrna\//\t/g' | sed 's/.fa.txt:/\t/g' > ${workdir}/final/16S_rrna.tmp
grep -c 23S ${workdir}/rna/rrna/* | sed 's/\/rna\/rrna\//\t/g' | sed 's/.fa.txt:/\t/g' | cut -f3 > ${workdir}/final/23S_rrna.tmp
grep -c 5S ${workdir}/rna/rrna/* | sed 's/\/rna\/rrna\//\t/g' | sed 's/.fa.txt:/\t/g' | cut -f3 > ${workdir}/final/5S_rrna.tmp

(echo 'Sample Bin rna.16S rna.23S rna.5S' | tr ' ' '\t';
paste ${workdir}/final/16S_rrna.tmp ${workdir}/final/23S_rrna.tmp ${workdir}/final/5S_rrna.tmp ) > ${workdir}/final/rrna.tmp;
