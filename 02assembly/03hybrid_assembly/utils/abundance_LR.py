import pandas as pd
import numpy as np


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


def abundance_LR(fapath, krpath, outpath):
    
    stats_dict = {'Acinetobacter baumannii': 0,
                  'Bifidobacterium adolescentis': 0,
                  'Bifidobacterium longum': 0,
                  'Capnocytophaga ochracea': 0,
                  'Enterobacter cloacae': 0,
                  'Enterococcus faecium': 0,
                  'Finegoldia magna': 0,
                  'Fusobacterium nucleatum': 0,
                  'Helicobacter cinaedi': 0,
                  'Jonquetella anthropi': 0,
                  'Klebsiella pneumoniae': 0,
                  'Lactobacillus reuteri': 0,
                  'Parascardovia denticolens': 0,
                  'Prevotella oris': 0,
                  'Salmonella enterica': 0,
                  'Staphylococcus epidermidis': 0,
                  'Streptococcus parasanguinis': 0}
    sp_len = [4006698, 2089645, 2385164, 2612925, 5314581,
              2698137, 1797577, 2441632, 2240130, 1675934,
              5315120, 2039414, 1891448, 3063215, 4831756,
              2499279, 2153652]
    
    seqs, headers = readfa(fapath)
    length = []
    for i in range(len(seqs)):
        length.append(len(seqs[i]))
        header = headers[i].split()[0]
        headers[i] = header
    del seqs

    keys = list(stats_dict.keys())
    f2 = open(krpath, 'r')
    i = 0
    for line in f2:
        i += 1
        info = line[:-1].split('\t')
        if info[1] != headers[i-1]:
            raise ValueError('Headers from fastq and report not the same!')
        if info[0] == 'U':
            continue
        elif info[0] == 'C':
            species_list = info[2].split()[0:2]
            species = species_list[0]+' '+species_list[1]
            if not species in keys:
                continue
            stats_dict[species] = stats_dict[species]+length[i-1]
        if i % 100000 == 0:
            print('Read %s finished'%i)

    for i in range(len(keys)):
        stats_dict[keys[i]] = stats_dict[keys[i]] / sp_len[i]

    values = list(stats_dict.values())
    total = sum(values)
    values = np.array(values) / total
    abundance_table = pd.DataFrame(stats_dict, index=[0])
    abundance_table.loc[0] = values
    abundance_table.to_csv(outpath)
    

fapath1 = '../GIS20/evaluation/library_analysis/TGS/Pacbio/corrected_PB.fa'
krpath1 = '../GIS20/evaluation/library_analysis/TGS/Pacbio/kraken2.PB.output'
outpath1 = '../GIS20/evaluation/library_analysis/TGS/Pacbio/relative_abundance_PB.csv'
abundance_LR(fapath1, krpath1, outpath1)

fapath2 = '../GIS20/evaluation/library_analysis/TGS/ONT/corrected_ONT.fa'
krpath2 = '../GIS20/evaluation/library_analysis/TGS/ONT/kraken2.ONT.output'
outpath2 = '../GIS20/evaluation/library_analysis/TGS/ONT/relative_abundance_ONT.csv'
abundance_LR(fapath2, krpath2, outpath2)