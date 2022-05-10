#!/usr/bin/env python
# -*- coding: utf-8 -*-
#author @islekburak

import os
import subprocess
import argparse, textwrap
import pandas as pd

parser=argparse.ArgumentParser(prog="pretable.py",
	usage="python3 %(prog)s [options] <path_of_file>",
	description=textwrap.dedent("""\
		author:		islekburak
		contact:	islekburakk@gmail.com"""),

	add_help=True,
	formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("-i","--input", metavar="<MAT FILE>", required=True, help="Write the path of your input file (i.e. /home/Desktop/mat_file)")

args=parser.parse_args()

mat_file=args.input

infile=open(mat_file,"r")
outfile="table.csv"
out=open(outfile,"w")

next(infile)
for i in infile:
	first=i.split()[0].split("|")[2].split("_")[0]
	others=i.split()[1:]
	string= ",".join(others)
	string2=first+","+string
	out.write(string2+"\n")
out.close()