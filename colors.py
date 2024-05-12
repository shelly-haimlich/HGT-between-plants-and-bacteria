import pandas as pd
import sys
import os
from os.path import sep
pd.set_option('display.max_rows', None)
# A script that selects colors for the phylogenetic tree, for each gene.
# Creates a file for iTOL
# https://htmlcolorcodes.com/

######################################################
#part_A
######################################################

GENE_NAME = sys.argv[1]

file = pd.read_csv(f'../{GENE_NAME}/genes+genomes_{GENE_NAME}_COMBINED_without_LD.txt', delimiter="\t", names=['source', 'geneID', 'GENOME'], dtype={'geneID':'str', 'GENOME':'str'})
#print(file)

# PA: blue
file.loc[file['source'] == f'/{GENE_NAME}/genes+genomes_{GENE_NAME}_PA', 'color'] = "#1911BF"

# bacteria: red
file.loc[file['source'] == f'/{GENE_NAME}/genes+genomes_{GENE_NAME}_NPA', 'color'] = "#AE2206"


# plants: green
# Vascular plant #159E0E
file.loc[
    (file['GENOME'] == 'Glycine_max') | (file['GENOME'] == 'Brassica_rapa') | (file['GENOME'] == 'Oryza_sativa') |
    (file['GENOME'] == 'Cannabis_sativa') | (file['GENOME'] == 'Olea_europaea') |
    (file['GENOME'] == 'Solanum_lycopersicum') | (file['GENOME'] == 'Capsicum_baccatum') |
    (file['GENOME'] == 'Beta_vulgaris'), 'color'] = "#159E0E"

# Bryophyta #19E40E
file.loc[file['GENOME'] == 'Physcomitrium_patens', 'color'] = "#19E40E"

# Archaea: #d4830b
file.loc[(file['GENOME'] == 'Methanothermobacter') | (file['GENOME'] == 'Sulfolobus_acidocaldarius'), 'color'] = "#d4830b"


# Amorphea #9A0CCB
file.loc[
    (file['GENOME'] == 'Caenorhabditis_elegans') | (file['GENOME'] == 'Danio_rerio') |
    (file['GENOME'] == 'Dictyostelium_discoideum') | (file['GENOME'] == 'Drosophila_melanogaster') |
    (file['GENOME'] == 'Homo_sapiens') | (file['GENOME'] == 'Mus_musculus'), 'color'] = "#9A0CCB"



# Amorphea #9A0CCB (fungus)
file.loc[(file['GENOME'] == 'Saccharomyces_cerevisiae') | (file['GENOME'] == 'Aspergillus_luchuensis') |
    (file['GENOME'] == 'Botrytis_cinerea') | (file['GENOME'] == 'Cryptococcus_neoformans') |
    (file['GENOME'] == 'Lentinula_edodes') | (file['GENOME'] == 'Thermothielavioides_terrestris') |
    (file['GENOME'] == 'Zymoseptoria_tritici') | (file['GENOME'] == 'Schizosaccharomyces_pombe'), 'color'] = "#9A0CCB"


# SAR #CCCCFF
file.loc[file['GENOME'] == 'Plasmodium_falciparum', 'color'] = "#CCCCFF"



file_additional_organisms = pd.read_csv(f'../{GENE_NAME}/genes+genomes_{GENE_NAME}_additional_organisms.txt', delimiter="\t", names=['geneID', 'GENOME'])

all_sequenced_genomes = pd.read_csv('new_organisms/all_sequenced_genomes_final_list.txt', delimiter="\t", names=['Group', 'GENOME', 'name', 'Assembly_Level'])

file_additional_organisms = file_additional_organisms.merge(all_sequenced_genomes, how="left", on='GENOME')
#print(file_additional_organisms)

# green_algae #023001
file_additional_organisms.loc[(file_additional_organisms['Group'] == 'chlorophyta_green_algae') | (file_additional_organisms['Group'] == 'charophyceae') | (file_additional_organisms['Group'] == 'zygnematophyceae'), 'color'] = "#023001"

# red_algae #76030F
file_additional_organisms.loc[file_additional_organisms['Group'] == "Rhodophyta_red_algae", 'color'] = "#76030F"

# cryptista #E496FF
file_additional_organisms.loc[file_additional_organisms['Group'] == "cryptophyceae_cryptomonads", 'color'] = "#E496FF"

# SAR #CCCCFF
file_additional_organisms.loc[file_additional_organisms['Group'] == "sar", 'color'] = "#CCCCFF"

# Amorphea #9A0CCB
file_additional_organisms.loc[(file_additional_organisms['Group'] == 'amoebozoa') | (file_additional_organisms['Group'] == 'opisthokont') | (file_additional_organisms['Group'] == 'apusomonadida'), 'color'] = "#9A0CCB"

# Archaea #d4830b
file_additional_organisms.loc[file_additional_organisms['Group'] == "archaea", 'color'] = "#d4830b"

# Vascular plant #159E0E
file_additional_organisms.loc[file_additional_organisms['Group'] == "tracheophyta_vascular_plants", 'color'] = "#159E0E"

# Bryophyta #19E40E
file_additional_organisms.loc[(file_additional_organisms['Group'] == 'bryophytina_mosses') | (file_additional_organisms['Group'] == 'marchantiophyta_liverworts'), 'color'] = "#19E40E"

file1 = file[["geneID", "color"]]


file_additional_organisms = file_additional_organisms[["geneID", "color"]]
#print(file_additional_organisms)

file_additional_organisms_all = pd.concat([file1, file_additional_organisms])
file_additional_organisms_all = file_additional_organisms_all.drop_duplicates()
file_additional_organisms_all.to_csv(f'../{GENE_NAME}/file_additional_organisms_{GENE_NAME}.txt', index=False, sep='\t', header=None)


# Write the correct values for the beginning of the file
colorpool = {"#1911BF": "PA Bacteria", "#AE2206" : "NPA Bacteria", "#159E0E": "Vascular Plant", "#19E40E": "Bryophyta", "#023001": "Green Algae", "#76030F": "Red Algae",
             "#d4830b": "Archaea", "#9A0CCB": "Amorphea", "#CCCCFF": "SAR", "#E496FF": "Cryptista"}
colors = file_additional_organisms_all['color'].unique()
FS = '\t'
separator = 'TAB'
DATASET_LABEL = 'Classification'
COLOR = '#ff0000'
currentcategory = 'Classification'
COLOR_BRANCHES = "0" # 0 is no
fileout = "../" +str(GENE_NAME) + "/Color_changer_ordered_additional_organisms_" + str(GENE_NAME) + ".txt"
kind_of_document = 'DATASET_COLORSTRIP'
MARGIN  = "6"
STRIP_WIDTH = "55"


LEGEND_SHAPES = '1\t' * len(colors)
LEGEND_COLORS = ""
for i in colors:
    LEGEND_COLORS += i
    LEGEND_COLORS += FS
LEGEND_LABELS = ""
for i in colors:
    LEGEND_LABELS += (colorpool[i] + FS)



with open(fileout, 'a+') as f:
    to_write = (kind_of_document + "\n"
                + "SEPARATOR" + FS + separator + "\n"
                + "DATASET_LABEL" + FS + DATASET_LABEL + "\n"
                + "COLOR" + FS + COLOR + "\n"
                + "COLOR_BRANCHES" + FS + COLOR_BRANCHES + "\n"
                + "LEGEND_TITLE" + FS + currentcategory + "\n"
                + "LEGEND_SHAPES" + FS + LEGEND_SHAPES + "\n"
                + "LEGEND_COLORS" + FS + LEGEND_COLORS + "\n"
                + "LEGEND_LABELS" + FS + LEGEND_LABELS + "\n"
		+ "MARGIN" + FS + MARGIN + "\n"
		+ "STRIP_WIDTH" + FS + STRIP_WIDTH + "\n"
                + "DATA\n"
		+ str(GENE_NAME) + FS + "#159E0E" + FS + "Arabidopsis\n"
                )
    f.write(to_write)
#    print(to_write)



"""
#####################################################################
#part_B
################################################################

file = pd.read_csv(f'./{GENE_NAME}/genes+genomes_{GENE_NAME}_COMBINED.txt', delimiter="\t", names=['source', 'geneID', 'GENOME'], dtype={'geneID':'str', 'GENOME':'str'})
#print(file)

phylum = pd.read_csv('./Phylum_NPA_analysis_new_and_diverse.txt', delimiter="\t")
phylum['genome'] = phylum['genome'].astype(str)

file = file.merge(phylum, how="left", right_on='genome', left_on='GENOME')

file.loc[file['Phylum'] == "Actinobacteria", 'color'] = "#9d8189"
file.loc[file['Phylum'] == "Bacteroidetes", 'color'] = "#FF6683"
file.loc[file['Phylum'] == "Firmicutes", 'color'] = "#d8e2dc"
file.loc[file['Phylum'] == "Proteobacteria", 'color'] = "#f4acb7"
file.loc[file['Phylum'] == "Unknown", 'color'] = "#FFEBFF"

# plants: green
# Monocotyledons #19C810
file.loc[file['GENOME'] == 'Oryza_sativa', 'color'] = "#1CFE10"

# dicotyledons #159E0E
file.loc[
    (file['GENOME'] == 'Glycine_max') | (file['GENOME'] == 'Brassica_rapa') |
    (file['GENOME'] == 'Cannabis_sativa') | (file['GENOME'] == 'Olea_europaea') |
    (file['GENOME'] == 'Solanum_lycopersicum') | (file['GENOME'] == 'Capsicum_baccatum')
    | (file['GENOME'] == 'Beta_vulgaris'), 'color'] = "#159E0E"

# Moss #023001
file.loc[file['GENOME'] == 'Physcomitrium_patens', 'color'] = "#023001"

# Different from Mammalia
file.loc[
    (file['GENOME'] == 'Caenorhabditis_elegans') | (file['GENOME'] == 'Danio_rerio') |
    (file['GENOME'] == 'Dictyostelium_discoideum') | (file['GENOME'] == 'Drosophila_melanogaster') |
    (file['GENOME'] == 'Leishmania_donovani') | (file['GENOME'] == 'Plasmodium_falciparum'), 'color'] = "#CCCCFF"

#Mammalia
file.loc[
     (file['GENOME'] == 'Homo_sapiens') | (file['GENOME'] == 'Mus_musculus'), 'color'] = "#E496FF"


# Archaea: dark purple
file.loc[file['GENOME'] == 'Methanothermobacter', 'Phylum'] = 'Euryarchaeota'
file.loc[file['GENOME'] == 'Methanothermobacter', 'color'] = '#cf0016'

file.loc[file['GENOME'] == 'Sulfolobus_acidocaldarius', 'Phylum'] = 'Crenarchaeota'
file.loc[file['GENOME'] == 'Sulfolobus_acidocaldarius', 'color'] = '#76030F'


# fungus plant-associated
file.loc[
    (file['GENOME'] == 'Botrytis_cinerea') | (file['GENOME'] == 'Lentinula_edodes') |
     (file['GENOME'] == 'Zymoseptoria_tritici') | (file['GENOME'] == 'Saccharomyces_cerevisiae'), 'color'] = "#F7DC6F"

# fungus NOT plant-associated
file.loc[
    (file['GENOME'] == 'Aspergillus_luchuensis') | (file['GENOME'] == 'Cryptococcus_neoformans') |
    (file['GENOME'] == 'Thermothielavioides_terrestris') | (file['GENOME'] == 'Schizosaccharomyces_pombe'), 'color'] = "#F49601"


file1 = file[["geneID", "color", 'Phylum']]
file1 = file1.drop_duplicates()
file1.to_csv(f'./{GENE_NAME}/file_second_layer_{GENE_NAME}.txt', index=False, sep='\t', header=None)

# Write the correct values for the beginning of the file
colorpool = {"#9d8189": "Actinobacteria", "#FF6683": "Bacteroidetes", "#d8e2dc": "Firmicutes", "#f4acb7": "Proteobacteria",
             "#FFEBFF" : "Unknown", "#1CFE10": "Monocotyledons", "#159E0E": "Dicotyledons", "#023001": "Moss",
              "#CCCCFF": "Non Mammals Eukaryotes","#E496FF": "Mammals", "#cf0016": "Euryarchaeota", "#76030F": "Crenarchaeota",
             "#F7DC6F": "PA Fungi", "#F49601": "NPA Fungi"}
colors = file['color'].unique()
FS = '\t'
separator = 'TAB'
DATASET_LABEL = 'Taxonomy'
COLOR = '#ff0000'
currentcategory = "Taxonomy"
COLOR_BRANCHES = "0" # 0 is no
fileout ="./" +str(GENE_NAME) + "/Color_changer_ordered_second_layer_" + str(GENE_NAME) + ".txt"
kind_of_document = 'DATASET_COLORSTRIP'


LEGEND_SHAPES = '1\t' * len(colors)
LEGEND_COLORS = ""
for i in colors:
    LEGEND_COLORS += i
    LEGEND_COLORS += FS
LEGEND_LABELS = ""
for i in colors:
    LEGEND_LABELS += (colorpool[i] + FS)



with open(fileout, 'a+') as f:
    to_write = (kind_of_document + "\n"
                + "SEPARATOR" + FS + separator + "\n"
                + "DATASET_LABEL" + FS + DATASET_LABEL + "\n"
                + "COLOR" + FS + COLOR + "\n"
                + "COLOR_BRANCHES" + FS + COLOR_BRANCHES + "\n"
                + "LEGEND_TITLE" + FS + currentcategory + "\n"
                + "LEGEND_SHAPES" + FS + LEGEND_SHAPES + "\n"
                + "LEGEND_COLORS" + FS + LEGEND_COLORS + "\n"
                + "LEGEND_LABELS" + FS + LEGEND_LABELS + "\n"
                + "DATA\n"
		+ str(GENE_NAME) + FS + "#159E0E" + FS + "Arabidopsis\n"
                )
    f.write(to_write)
    print(to_write)

"""
