#!/usr/bin/env python
# -*- coding: utf-8 -*-
#author @islekburak

import pip
def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        pip.main(["install", package])

import_or_install("argparse")
import_or_install("pandas")
import_or_install("matplotlib.pyplot")
import_or_install("seaborn")
import_or_install("Bio.Align.Applications")

import os
import subprocess
import argparse, textwrap
import pandas as pd

parser=argparse.ArgumentParser(prog="gettingfasta.py",
	usage="python3 %(prog)s [options] <path_of_file>",
	description=textwrap.dedent("""\
		author:		islekburak
		contact:	islekburakk@gmail.com"""),

	add_help=True,
	formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("-i","--input", metavar="<FASTA FILE>", required=True, help="Write the path of your input -output of BLAST- file (i.e. /home/Desktop/input.fasta)")
parser.add_argument("-db","--database", metavar="<DATABASE>", required=True, help="Write the path of your database -fasta- file (i.e. /home/Desktop/mydb.fasta)")

args=parser.parse_args()

file_path=args.input
path=args.database

a=pd.read_csv(file_path, comment="#", sep="\t")
a.columns =["query_id", "subject_id", "identity", "alignment_length", "mismatches", "gap_opens", "s.end", "evalue", "bit_score", "subject_title"]



subjectlist=a.subject_id.tolist()
uniquesubjects=list(set(subjectlist))

infile=path

outfile="combined.fasta"
outfile = open (outfile, "w")

found=False
with open (path, "r") as myfasta:
	for line in myfasta:
		if ">" in line and not found:
			for item in uniquesubjects:
				if str(item) in line:
					outfile.write(line)
					found=True
					break
		elif ">" in line and found:
			for item in uniquesubjects:
				if str(item) in line:
					outfile.write(line)
					found=True
					break
				else:
					found=False
		elif ">" not in line and found:
			outfile.write(line)
outfile.close()