import pandas as pd
import numpy as np
import os
import sys

def merge(workdir):
    tRNA = pd.read_table(os.path.join(workdir, 'final', 'trna.tmp'))
    rRNA = pd.read_table(os.path.join(workdir, 'final', 'rrna.tmp'))
    tRNA_rRNA = pd.merge(tRNA, rRNA, left_on='Bin', right_on='Bin')
    tRNA_rRNA.to_csv(os.path.join(workdir, 'tRNA_rRNA.csv'), index=False)

def main():
    workdir = sys.argv[1]
    merge(workdir)
    #tRNA_rRNA = os.path.join(workdir, 'tRNA_rRNA.csv')
    #RNA_df = pd.read_csv(tRNA_rRNA, header=0)
    # RNA_stat = open(os.path.join(workdir, 'RNA_stat.csv'), 'w')
    # RNA_stat.write('genome_type,RNAtype,RNAcount,RNAnum\n')
    # for genome_type in ['Isolate', 'MAG']:
    #    RNA_df_filter = RNA_df.loc[RNA_df['Genome_type']==genome_type, ]
    #    print("{},{}".format(genome_type, RNA_df_filter.shape[0]))
    #    for RNAtype in ['tRNA', 'rna.16S', 'rna.23S', 'rna.5S']:
    #        if RNAtype in ['tRNA']:
    #            for RNAcount in ['<18', '18~36', '36~54', '>=54']:
    #                RNAnum = 0
    #                if RNAcount == '<18':
    #                    RNAnum = RNA_df_filter.loc[RNA_df_filter[RNAtype]<18, ].shape[0]
    #                elif RNAcount == '18~36':
    #                    RNAnum = RNA_df_filter.loc[(RNA_df_filter[RNAtype]>=18) & (RNA_df_filter[RNAtype]<36), ].shape[0]
    #                elif RNAcount == '36~54':
    #                    RNAnum = RNA_df_filter.loc[(RNA_df_filter[RNAtype]>=36) & (RNA_df_filter[RNAtype]<54),].shape[0]
    #                elif RNAcount == '>=54':
    #                    RNAnum = RNA_df_filter.loc[(RNA_df_filter[RNAtype]>=54),].shape[0]
    #                print("{},{},{},{}".format(genome_type,RNAtype,RNAcount, RNAnum))
    #                RNA_stat.write("{},{},{},{}\n".format(genome_type,RNAtype,RNAcount,RNAnum))
    #        elif RNAtype in ['rna.16S', 'rna.23S', 'rna.5S']:
    #            for RNAcount in ['0', '1', '2', '>=3']:
    #                RNAnum = 0
    #                if RNAcount == '0':
    #                    RNAnum = RNA_df_filter.loc[RNA_df_filter[RNAtype]==0, ].shape[0]
    #                elif RNAcount == '1':
    #                    RNAnum = RNA_df_filter.loc[RNA_df_filter[RNAtype] == 1, ].shape[0]
    #                elif RNAcount == '2':
    #                    RNAnum = RNA_df_filter.loc[RNA_df_filter[RNAtype]==2, ].shape[0]
    #                elif RNAcount == '>=3':
    #                    RNAnum = RNA_df_filter.loc[(RNA_df_filter[RNAtype]>=3),].shape[0]
    #                print("{},{},{},{}".format(genome_type,RNAtype,RNAcount, RNAnum))
    #                RNA_stat.write("{},{},{},{}\n".format(genome_type,RNAtype,RNAcount,RNAnum))
    # RNA_stat.close()

if __name__ == '__main__':
    main()