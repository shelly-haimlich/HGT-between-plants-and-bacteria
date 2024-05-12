import pandas as pd


blast_results_file = pd.read_csv('/blast_results/all_blast_results.txt', delimiter="\t", header=None, names=['Assembly','qseqid', 'sseqid', 'pident',
                                                                   'length', 'mismatch', 'gapopen', 'qstart',
                                                                  'qend', 'sstart', 'send', 'evalue', 'bitscore',
                                                                   'qlen', 'slen'])


#print(len(blast_results_file))

blast_results_file = blast_results_file.loc[(blast_results_file["pident"] >= 35) & (blast_results_file['length'] / blast_results_file['qlen'] >= 0.8) &
                (blast_results_file['length'] / blast_results_file['slen'] >= 0.8)]



file.to_csv('/blast_results/NPA_additional_organisms/'all_blast_results_filter.txt', index=False, sep='\t')
