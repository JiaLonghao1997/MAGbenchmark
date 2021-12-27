import os


def readfq(filepath):
    
    f = open(filepath, 'r')
    headers = []
    seqs = []
    Qvalues = []
    i = 0
    for line in f:
        i += 1
        if i % 4 == 1:
            headers.append(line[:-1])
        elif i % 4 == 2:
            seqs.append(line[:-1])
        elif i % 4 == 3:
            continue
        elif i % 4 == 0:
            Qvalues.append(line[:-1])
    f.close()
    
    return headers, seqs, Qvalues


def writefq(headers, seqs, Qvalues, outpath):
    
    f = open(outpath, 'w')
    for i in range(len(headers)):
        f.write(headers[i])
        f.write('\n')
        f.write(seqs[i])
        f.write('\n')
        f.write('+\n')
        f.write(Qvalues[i])
        f.write('\n')
    f.close()


def split(filepath, prefix):
    
    headers, seqs, Qvalues = readfq(filepath)
    headers_fw = []
    headers_rv = []
    seqs_fw = []
    seqs_rv = []
    Qvalues_fw = []
    Qvalues_rv = []
    
    for i in range(len(headers)):
        h_list = list(headers[i])
        if h_list[-1] == '1':
            headers_fw.append(headers[i])
            seqs_fw.append(seqs[i])
            Qvalues_fw.append(Qvalues[i])
        elif h_list[-1] == '2':
            headers_rv.append(headers[i])
            seqs_rv.append(seqs[i])
            Qvalues_rv.append(Qvalues[i])
    
    outpath1 = prefix+'_R1.fq'
    outpath2 = prefix+'_R2.fq'
    writefq(headers_fw, seqs_fw, Qvalues_fw, outpath1)
    writefq(headers_rv, seqs_rv, Qvalues_rv, outpath2)


filepath = '../Reads/NGS/combined_reads.fq'
prefix = '../Reads/NGS/combined_reads'
split(filepath, prefix)
