setwd('D:\\project\\Benchmark\\RealData\\MGE_AMG')

A_ONT_HB_3C_pmd = read.table('MGE/A/Plasmid/S1_Nanopore_OPERA-MS+bin3C.txt',
                             header=TRUE, sep='\t')
A_ONT_HB_MB_pmd = read.table('MGE/A/Plasmid/S1_Nanopore_OPERA-MS+Metabat2.txt',
                             header=TRUE, sep='\t')
A_PB_HB_3C_pmd = read.table('MGE/A/Plasmid/S1_PacBio_OPERA-MS+bin3C.txt',
                             header=TRUE, sep='\t')
A_PB_HB_MB_pmd = read.table('MGE/A/Plasmid/S1_PacBio_OPERA-MS+Metabat2.txt',
                            header=TRUE, sep='\t')
A_ONT_LR_3C_pmd = read.table('MGE/A/Plasmid/S1_Nanopore_metaflye+bin3C.txt',
                             header=TRUE, sep='\t')
A_ONT_LR_MB_pmd = read.table('MGE/A/Plasmid/S1_Nanopore_metaflye+Metabat2.txt',
                             header=TRUE, sep='\t')
A_PB_LR_3C_pmd = read.table('MGE/A/Plasmid/S1_PacBio_metaflye+bin3C.txt',
                            header=TRUE, sep='\t')
A_PB_LR_MB_pmd = read.table('MGE/A/Plasmid/S1_PacBio_metaflye+Metabat2.txt',
                            header=TRUE, sep='\t')
A_SR_3C_pmd = read.table('MGE/A/Plasmid/S1_mNGS_metaSPAdes+bin3C.txt',
                         header=TRUE, sep='\t')
A_SR_MB_pmd = read.table('MGE/A/Plasmid/S1_mNGS_metaSPAdes+Metabat2.txt',
                         header=TRUE, sep='\t')
len_plasmid = function(report) {
  if(all(report$cluster_id == 'chromosome')) {
    return(0)
  }
  idx = which(report$cluster_id != 'chromosome')
  return(sum(report$contig_length[idx]))
}

A_ONT_HB_3C_pmd_len = len_plasmid(A_ONT_HB_3C_pmd)
A_ONT_HB_MB_pmd_len = len_plasmid(A_ONT_HB_MB_pmd)
A_PB_HB_3C_pmd_len = len_plasmid(A_PB_HB_3C_pmd)
A_PB_HB_MB_pmd_len = len_plasmid(A_PB_HB_MB_pmd)
A_ONT_LR_3C_pmd_len = len_plasmid(A_ONT_LR_3C_pmd)
A_ONT_LR_MB_pmd_len = len_plasmid(A_ONT_LR_MB_pmd)
A_PB_LR_3C_pmd_len = len_plasmid(A_PB_LR_3C_pmd)
A_PB_LR_MB_pmd_len = len_plasmid(A_PB_LR_MB_pmd)
A_SR_3C_pmd_len = len_plasmid(A_SR_3C_pmd)
A_SR_MB_pmd_len = len_plasmid(A_SR_MB_pmd)
A_pmd_len = c(A_SR_MB_pmd_len, A_SR_3C_pmd_len, A_PB_LR_MB_pmd_len,
              A_PB_LR_3C_pmd_len, A_ONT_LR_MB_pmd_len, A_ONT_LR_3C_pmd_len,
              A_PB_HB_MB_pmd_len, A_PB_HB_3C_pmd_len, A_ONT_HB_MB_pmd_len,
              A_ONT_HB_3C_pmd_len)


A_ONT_HB_3C_phg = read.table('MGE/A/Phage/S1_Nanopore_OPERA-MS+bin3C.tsv',
                             header=TRUE, sep='\t')
A_ONT_HB_MB_phg = read.table('MGE/A/Phage/S1_Nanopore_OPERA-MS+Metabat2.tsv',
                             header=TRUE, sep='\t')
A_PB_HB_3C_phg = read.table('MGE/A/Phage/S1_PacBio_OPERA-MS+bin3C.tsv',
                            header=TRUE, sep='\t')
A_PB_HB_MB_phg = read.table('MGE/A/Phage/S1_PacBio_OPERA-MS+Metabat2.tsv',
                            header=TRUE, sep='\t')
A_ONT_LR_3C_phg = read.table('MGE/A/Phage/S1_Nanopore_metaflye+bin3C.tsv',
                             header=TRUE, sep='\t')
A_ONT_LR_MB_phg = read.table('MGE/A/Phage/S1_Nanopore_metaflye+Metabat2.tsv',
                             header=TRUE, sep='\t')
A_PB_LR_3C_phg = read.table('MGE/A/Phage/S1_PacBio_metaflye+bin3C.tsv',
                            header=TRUE, sep='\t')
A_PB_LR_MB_phg = read.table('MGE/A/Phage/S1_PacBio_metaflye+Metabat2.tsv',
                            header=TRUE, sep='\t')
A_SR_3C_phg = read.table('MGE/A/Phage/S1_mNGS_metaSPAdes+bin3C.tsv',
                         header=TRUE, sep='\t')
A_SR_MB_phg = read.table('MGE/A/Phage/S1_mNGS_metaSPAdes+Metabat2.tsv',
                         header=TRUE, sep='\t')

len_phage = function(report) {
  return(sum(report$trim_bp_end-report$trim_bp_start))
}

A_ONT_HB_3C_phg_len = len_phage(A_ONT_HB_3C_phg)
A_ONT_HB_MB_phg_len = len_phage(A_ONT_HB_MB_phg)
A_PB_HB_3C_phg_len = len_phage(A_PB_HB_3C_phg)
A_PB_HB_MB_phg_len = len_phage(A_PB_HB_MB_phg)
A_ONT_LR_3C_phg_len = len_phage(A_ONT_LR_3C_phg)
A_ONT_LR_MB_phg_len = len_phage(A_ONT_LR_MB_phg)
A_PB_LR_3C_phg_len = len_phage(A_PB_LR_3C_phg)
A_PB_LR_MB_phg_len = len_phage(A_PB_LR_MB_phg)
A_SR_3C_phg_len = len_phage(A_SR_3C_phg)
A_SR_MB_phg_len = len_phage(A_SR_MB_phg)
A_phg_len = c(A_SR_MB_phg_len, A_SR_3C_phg_len, A_PB_LR_MB_phg_len,
              A_PB_LR_3C_phg_len, A_ONT_LR_MB_phg_len, A_ONT_LR_3C_phg_len,
              A_PB_HB_MB_phg_len, A_PB_HB_3C_phg_len, A_ONT_HB_MB_phg_len,
              A_ONT_HB_3C_phg_len)

A_MGE_len = A_pmd_len + A_phg_len
bin_len = c()

