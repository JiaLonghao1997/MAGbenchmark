#!/usr/bin/env python
import os
import shutil
import sys
from Bio import SeqIO

# Takes fasta file and counts total bases
def count_bases(infile):
    sum = 0
    with open(infile, 'r') as lines:
        for line in lines:
            if ">" not in line:
                sum += len(line.strip())
    # print(sum)
    return sum

def main():
    inputdir = sys.argv[1]
    outdir = sys.argv[2]
    print("inputdir: {}".format(inputdir))
    print("outdir: {}".format(outdir))
    os.system("mkdir -p {}".format(outdir))
    files = os.listdir(inputdir)
    for file in files:  # 遍历文件夹
        infasta = os.path.join(inputdir, file)
        bps = count_bases(infasta)
        if bps > 200000:  # 判断是否是文件夹，不是文件夹才打开
            number = file.split('CL')[1].split('.fna')[0]
            binfile = 'bin' + str(number) + '.fa'
            outfasta = os.path.join(outdir, binfile)
            #shutil.copyfile(infasta, outfasta)
            #os.system("cp {} {}".format(infasta, outfasta))
            output = open(outfasta, 'w')
            with open(infasta) as lines:
                for line in lines:
                    if line.startswith('>'):
                        contig_name = line.strip().split(' ')[1].split(':')[1]
                        new_header = '>{}\n'.format(contig_name)
                        output.write(new_header)
                    else:
                        output.write(line)
            output.close()

if __name__ == "__main__":
    main()
