#!/usr/bin/env python
# -*- coding: utf-8 -*-
#author @islekburak

import os
import subprocess
import argparse, textwrap
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

parser=argparse.ArgumentParser(prog="clustermapper.py",
	usage="python3 %(prog)s [options] <path_of_file>",
	description=textwrap.dedent("""\
		author:		islekburak
		contact:	islekburakk@gmail.com"""),

	add_help=True,
	formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("-i","--input", metavar="<CSV FILE>", required=True, help="Write the path of your input file (i.e. /home/Desktop/finaltable.csv")

args=parser.parse_args()
file_path=args.input

#using matrix file for create heatmap
df=pd.read_csv(file_path)
df=df.set_index("0")
df.index.name=None

sns.clustermap(df, method="average", metric="euclidean", standard_scale=1, cmap="Spectral" , figsize=(10,10))
plt.savefig("clustermap.png")
plt.close()