#!/bin/bash -ue
blastp -num_threads 2 -query FZDs.2.fasta -db inputs/human_proteomes -max_target_seqs 20 -outfmt '7 qseqid sseqid pident length mismatch gapopen send evalue bitscore stitle' -out FZDs.blastout
