#!/bin/bash

while read line
do
echo $line

seqkit grep -p "$line" ../Araport11_genes.201606.pep.fasta > ../"$line"/faa_file_"$line"

# finding the faa
sbatch --wait -c30 --time=10:00:00 --wrap="python3 filter_and_find_faa.py $line"


sbatch --wait --mem=16g --time=12:00:00 --wrap="whileloop_seqkit.sh ../$line/genes+genomes_"$line"_additional_organisms.txt"



echo step_3

cat ../$line/genes+genomes_*_fasta >> ../"$line"/faa_file_"$line"

seqkit rmdup ../"$line"/faa_file_"$line" > ../"$line"/faa_file_"$line"_uniq

rm -f ../"$line"/faa_file_"$line"



clustalo -i ../$line/faa_file_"$line" -o ../$line/faa_file_"$line".aln --threads=30

sbatch --wait --mem=400G -c60 --time=12:00:00 --wrap="iqtree2 -s ../$line/faa_file_"$line".aln -mset LG,WAG,JTT,JTTDCMut -T AUTO -B 2000"


python3 mad.py ../$line/faa_file_"$line".aln.treefile



echo step_4_color


sbatch --wait -c10 --wrap="python3 colors.py $line"


cat ../$line/Color_changer_ordered_"$line".txt ../$line/file_additional_organisms_"$line".txt > ../$line/color_ring_additional_organisms_"$line".txt



echo Finished creating the $line tree

done < $1
