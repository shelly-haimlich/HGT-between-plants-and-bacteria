import pandas as pd
import sys

# PA
file = pd.read_csv('../blast_results_united_35_with_genomeID.V2.txt', delimiter="\t", dtype={'qseqid':'str'})


sys.argv[1]
Arbidopsis_gene_name = sys.argv[1].split('.')[0]
Arbidopsis_gene = file.loc[file['locus'] == Arbidopsis_gene_name]


united_file_PA_genes = Arbidopsis_gene[['qseqid', 'genome']]
united_file_PA_genes = united_file_PA_genes.drop_duplicates()
united_file_PA_genes = united_file_PA_genes.rename(columns={"qseqid": "PA_geneID", "genome": "PA_genomeID"})


# NPA against arbidopsis
file_NPA = pd.read_csv('../blast_results_NPA_581_united_35_with_genomeID.V2.txt', delimiter="\t")

Arbidopsis_gene_NPA = file_NPA.loc[file_NPA['locus'] == Arbidopsis_gene_name]

Arbidopsis_gene_NPA = Arbidopsis_gene_NPA.rename(columns={"qseqid": "NPA_geneID", "genome": "NPA_genomeID"})
Arbidopsis_gene_NPA = Arbidopsis_gene_NPA[['NPA_geneID', 'NPA_genomeID']]
Arbidopsis_gene_NPA = Arbidopsis_gene_NPA.drop_duplicates()
Arbidopsis_gene_NPA = Arbidopsis_gene_NPA.astype(int)


##### additional_organisms PA #######

# Open the additional_organisms file and rename the columns
additional_organisms = pd.read_csv('/blast_results_PA_against_additional_organisms_filter.txt', delimiter="\t", dtype={'sseqid':'str'})
additional_organisms = additional_organisms.rename(columns={"Assembly": "additional_organisms_genomeID", "qseqid": "additional_organisms_geneID", "sseqid": "PA_geneID"})

# Connecting files and drop blank lines
united_file_additional_organisms = united_file_PA_genes.merge(additional_organisms, how="left", on='PA_geneID')
united_file_additional_organisms = united_file_additional_organisms.loc[united_file_additional_organisms['additional_organisms_geneID'].notna()]

# Create a file that contains only the ID and Genome ID
# Belonging to the genes of the united_file_PA_genes
united_file_united_file_PA_genes = united_file_additional_organisms[['additional_organisms_geneID', 'additional_organisms_genomeID']]


######## additional_organisms NPA #########

# Open the additional_organisms file and rename the columns
additional_organisms_NPA = pd.read_csv('blast_results_NPA_against_additional_organisms_filter.txt', delimiter="\t")
additional_organisms_NPA = additional_organisms_NPA.rename(columns={"Assembly": "additional_organisms_genomeID", "qseqid": "additional_organisms_geneID", "sseqid": "NPA_geneID"})

# Connecting files and drop blank lines
united_file_additional_organisms_NPA = Arbidopsis_gene_NPA.merge(additional_organisms_NPA, how="left", on='NPA_geneID')
united_file_additional_organisms_NPA = united_file_additional_organisms_NPA.loc[united_file_additional_organisms_NPA['additional_organisms_geneID'].notna()]

# Create a file that contains only the ID and Genome ID
# Belonging to the genes of the landmark
united_file_additional_organisms_NPA = united_file_additional_organisms_NPA[['additional_organisms_geneID', 'additional_organisms_genomeID']]


united_file_additional_organisms_NPA_genes = pd.concat([united_file_united_file_PA_genes, united_file_additional_organisms_NPA])
united_file_additional_organisms_NPA_genes = united_file_additional_organisms_NPA_genes.drop_duplicates(subset=['additional_organisms_geneID'])

# Remove Glycine max
remove = united_file_additional_organisms_NPA_genes['additional_organisms_genomeID'] == 'GCA_000004515.5'
united_file_additional_organisms_NPA_genes = united_file_additional_organisms_NPA_genes[~remove]


united_file_additional_organisms_NPA_genes.to_csv(f'../files_building_trees/{sys.argv[1]}/genes+genomes_{sys.argv[1]}_additional_organisms.txt', index=False, sep='\t', header=False)

