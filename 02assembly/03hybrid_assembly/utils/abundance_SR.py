import pandas as pd
import numpy as np

def abundance_SR(fqpath1, fqpath2, krpath, outpath, headers, length):
    
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
    
    headers = []
    length = []
    fq1 = open(fqpath1, 'r')
    i = 0
    for line in fq1:
        i += 1
        if i % 4 == 1:
            header = line[1:-1].split()[0]
            headers.append(header)
        elif i % 4 == 2:
            length.append(len(line[:-1]))
        if i % 4000000 == 0:
            print('Read %s in fq1 finished'%(i // 4))

    fq2 = open(fqpath2, 'r')
    i = 0
    for line in fq2:
        i += 1
        if i % 4 == 1:
           header = line[1:-1].split()[0]
           if headers[i//4] != header:
               raise ValueError('Headers of read %s from two paired-end files not the same!'%(i//4+1))
        elif i % 4 == 2:
            length[i//4] = length[i//4]+len(line[:-1])
        if i % 4000000 == 0:
             print('Read %s in fq2 finished'%(i // 4))

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
        if i % 1000000 == 0:
            print('Read %s finished'%i)

    for i in range(len(keys)):
        stats_dict[keys[i]] = stats_dict[keys[i]] / sp_len[i]

    values = list(stats_dict.values())
    total = sum(values)
    values = np.array(values) / total
    abundance_table = pd.DataFrame(stats_dict, index=[0])
    abundance_table.loc[0] = values
    abundance_table.to_csv(outpath)
    

fqpath1 = '../GIS20/NGS/ERR3200809_1_trim_paired.fastq'
fqpath2 = '../GIS20/NGS/ERR3200809_2_trim_paired.fastq'
krpath = '../GIS20/evaluation/library_analysis/NGS/kraken2.SR.output'
outpath = '../GIS20/evaluation/library_analysis/NGS/relative_abundance_SR.csv'
abundance_SR(fqpath1, fqpath2, krpath, outpath)