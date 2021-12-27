import pandas as pd
import os

basedir="/home3/ZXMGroup/VIROME/G3compare/"
datasets=['GIS20','CAMISIM', 'RealData']

GTDBdir = "/home3/ZXMGroup/VIROME/G3compare/pipeline/GTDB"
GTDBmetadata = pd.read_table(os.path.join(GTDBdir, "bac120_metadata_r95.filter.tsv"), header=0, low_memory=False)
print("GTDBmetadata.shape: ", GTDBmetadata.shape)
for dataset in datasets:
    print("begin to deal with {}".format(dataset))
    #workdir = os.path.join(basedir, dataset, 'merge', '04GTDB_tk+RNA')
    workdir = "/home3/ZXMGroup/VIROME/G3compare/pipeline/GTDB"
    GTDB_RNA = os.path.join(GTDBdir, '04GTDB_tk+RNA.py')
    os.system("python {} {}".format(GTDB_RNA, dataset))
    GTDB_tk = pd.read_table(os.path.join(workdir, '{}_Metabat2_bin3C_GTDB_RNA_compare2.tsv'.format(dataset)), header=0)
    GTDB_tk.loc[GTDB_tk['fastani_reference'].str.contains('GCA'), 'fastani_reference'] = 'GB_' + \
        GTDB_tk.loc[GTDB_tk['fastani_reference'].str.contains('GCA'), 'fastani_reference'].astype(str)
    GTDB_tk.loc[GTDB_tk['fastani_reference'].str.contains('GCF'), 'fastani_reference'] = 'RS_' + \
        GTDB_tk.loc[GTDB_tk['fastani_reference'].str.contains('GCF'), 'fastani_reference'].astype(str)
    print("GTDB_tk.columns.values.tolist():", GTDB_tk.columns.values.tolist())
    print("GTDB_tk.shape: ", GTDB_tk.shape)
    GTDB_tk_metadata = pd.merge(GTDB_tk, GTDBmetadata, left_on='fastani_reference', right_on='accession')
    print("GTDB_tk_metadata.shape: ", GTDB_tk_metadata.shape)
    outfile = os.path.join(workdir, '{}_Metabat2_bin3C_GTDB_RNA_compare_metadata.tsv'.format(dataset))
    GTDB_tk_metadata.to_csv(outfile, index=False, sep='\t')

    RNAstat_file = os.path.join(basedir, dataset, 'results', '02RNA', 'RNA_cluster.stat.csv')
    os.system("head {}".format(RNAstat_file))
    RNAstat = pd.read_csv(RNAstat_file, header=0)
    print(RNAstat.columns.values.tolist())
    RNAstat[['binname', 'suffix']] =  RNAstat['bin'].str.split('.fa', 1, expand=True)
    GTDB_tk = pd.read_table(os.path.join(basedir, dataset, 'merge', 'Metabat2+bin3C.complete.txt'), header=0)
    GTDB_tk_RNA = pd.merge(GTDB_tk, RNAstat, left_on=['sample','binmethod', 'binname'], right_on=['sample', 'binmethod', 'binname'])
    GTDB_tk_RNA.to_csv(os.path.join(GTDBdir, '{}_RNA_cluster.txt'.format(dataset)), sep='\t')

