import pandas as pd
import os


def readfa(filename):
    
    file = open(filename, 'r')
    seq = ''
    sequences = []
    
    for line in file:
        if line.startswith(">"):
            if seq != '':
                sequences.append(seq)
            seq = ''
            continue
        if line.startswith("\n"):
            continue
        seq += line[:-1]
    
    sequences.append(seq)
    file.close()
    return sequences


def plasmid_stats(pladir):
    
    plasmid_dict = {'Subject': [], 'Sequencing': [],
                    'Assembler': [], 'Binner': [],
                    'Number': [], 'Length': []}
    
    species = os.listdir(pladir)
    for sp in species:
        path1 = os.path.join(pladir, sp)
        bins = os.listdir(path1)
        for bin_per in bins:
            header = bin_per.replace('+', '_')
            header_list = header.split('_')
            plasmid_dict['Subject'].append(header_list[0])
            assembler = header_list[2]
            if assembler == 'OPERA-MS':
                plasmid_dict['Sequencing'].append('mNGS' + header_list[1])
            else:
                plasmid_dict.append(header_list[1])
            plasmid_dict['Assembler'].append(assembler)
            plasmid_dict['Binner'].append(header_list[3])
            
            path2 = os.path.join(path1, bin_per)
            files = os.listdir(path2)
            if len(files) <= 2:
                plasmid_dict['Number'] = 0
                plasmid_dict['Length'] = 0
            else:
                num = 0
                length = 0
                for file in files:
                    if file.find('plasmid') != -1:
                        num += 1
                        path3 = os.path.join(path2, file)
                        seq = readfa(path3)
                        length += len(seq)
                plasmid_dict['Number'] = num
                plasmid_dict['Length'] = length
                
    plasmid_info = pd.DataFrame(data=plasmid_dict)
    return plasmid_info


pladir = '/home3/ZXMGroup/VIROME/G3compare/02antismash/RealData02/04mob_suite'
plasmid_info = plasmid_stats(pladir)
                        