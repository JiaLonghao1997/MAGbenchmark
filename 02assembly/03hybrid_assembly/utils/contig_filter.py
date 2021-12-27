import math


def readfa(filename):
    
    file = open(filename, 'r')
    seq = ''
    sequences = []
    names = []
    
    for line in file:
        if line.startswith(">"):
            names.append(line[1:-1])
            if seq != '':
                sequences.append(seq)
            seq = ''
            continue
        if line.startswith("\n"):
            continue
        seq += line[:-1]
    
    sequences.append(seq)
    file.close()
    return sequences, names


def writefa(genomes, names, path):
    
    file = open(path, 'w')
    for i in range(len(genomes)):
        seq = genomes[i]
        file.write('>'+names[i])
        file.write('\n')
        nrow = math.ceil(len(seq) / 100)
        for row in range(nrow):
            if (row+1) < nrow:
                file.write(seq[100*row:100*(row+1)])
                file.write('\n')
            elif (row+1) == nrow:
                file.write(seq[100*row:])
                file.write('\n')
    file.close()
    
    
def contig_filter(filepath, minlen, outpath):
    
    contigs_all, headers_all = readfa(filepath)
    contigs, headers = [], []
    for i in range(len(contigs_all)):
        tig = contigs_all[i]
        header = headers_all[i]
        if len(tig) >= minlen:
            contigs.append(tig)
            headers.append(header)
    
    writefa(contigs, headers, outpath)


minlen = 1000
filepath = '../CAMISIM/assemblies/metaFlye/PacBio/2021.05.12_10.32.55_sample1/assembly.fasta'
outpath = '../CAMISIM/assemblies/metaFlye/PacBio/2021.05.12_10.32.55_sample1/assembly.filter.fasta'
contig_filter(filepath, minlen, outpath)

# filepath4 = '../RealData/assemblies/hybridSPAdes/ONT/F/contigs.fasta'
# outpath4 = '../RealData/assemblies/hybridSPAdes/ONT/F/contigs.filter.fa'
# contig_filter(filepath4, minlen, outpath4)


# filepath5 = '../CAMI2/assemblies/OPERA-MS/metaSPAdes/contigs.fasta'
# outpath5 = '../CAMI2/assemblies/OPERA-MS/metaSPAdes/contigs.filter.fa'
# contig_filter(filepath5, minlen, outpath5)
