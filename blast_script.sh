#!/bin/bash
# blast: bacteria against arbidopsis

while read line
do
	genomes=/IMG/$line/"$line".genes.faa
        echo doing genome: $genomes

	blastp -query $genomes -subject Araport11_genes.201606.pep.fasta -out /blast_results/"$line"_output -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qlen slen"
done < $1



# blast: Bacterial genes with more than 35% amino acid sequence identity across more than 80% of the Arabidopsis genes compared to control organisms

blastp -db list_bacteria_genes_to_blast_fasta -query control_organisms.fasta -num_threads 30 -out /blast_results/control_organisms/output -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qlen slen"



