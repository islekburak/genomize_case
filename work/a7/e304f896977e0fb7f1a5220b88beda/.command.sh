#!/bin/bash -ue
makeblastdb -in /Users/islekbro/Desktop/genomize_case1/inputs/human_proteomes.fasta -parse_seqids -dbtype 'prot' -out inputs/human_proteomes
