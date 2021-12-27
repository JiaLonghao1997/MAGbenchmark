workdir=$1
bin=$2
bindir=$3

mkdir -p ${workdir}/rna/rrna
/share/inspurStorage/home1/jialh/tools/miniconda3/bin/barrnap ${bindir}/${bin}.fa > ${workdir}/rna/rrna/${bin}.fa.txt

mkdir -p ${workdir}/rna/trna
/share/inspurStorage/home1/jialh/tools/miniconda3/bin/aragorn -t ${bindir}/${bin}.fa -o ${workdir}/rna/trna/${bin}.fa.txt

