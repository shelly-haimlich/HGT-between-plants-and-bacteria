#!/bin/bash

while read line
do
  GENE=$(echo $line | awk '{print $1}')
  GENOME=$(echo $line | awk '{print $2}')

seqkit grep -p "$GENE" new_organisms/genomes_downloading/data/$GENOME/protein.faa >> "$1"_fasta

done < $1