import pandas as pd
import os

workdir="/home3/ZXMGroup/VIROME/G3compare/pipeline/GTDB"
metadata = pd.read_table(os.path.join(workdir, "bac120_metadata_r95.tsv"), header=0, low_memory=False)
metadata_filter = metadata[['accession', 'checkm_completeness','checkm_contamination','gtdb_genome_representative','gtdb_representative', 'gtdb_taxonomy','ncbi_assembly_level', 'ncbi_date', 'ncbi_rrna_count','ncbi_trna_count']].copy()
metadata_filter.to_csv(os.path.join(workdir, "bac120_metadata_r95.filter.tsv"), header=True, index=False, sep='\t')