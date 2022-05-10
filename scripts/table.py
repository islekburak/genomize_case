#!/usr/bin/env python
# -*- coding: utf-8 -*-
#author @islekburak

import os
import subprocess
import argparse, textwrap
import pandas as pd

parser=argparse.ArgumentParser(prog="ClusterMapper.py",
	usage="python3 %(prog)s [options] <path_of_file>",
	description=textwrap.dedent("""\
		author:		islekburak
		contact:	islekburakk@gmail.com"""),

	add_help=True,
	formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("-i","--input", metavar="<CSV FILE>", required=True, help="Write the path of your input file (i.e. /home/Desktop/table.csv)")

args=parser.parse_args()

file_path=args.input

df=pd.read_csv(file_path, header=None)


headers=df.iloc[:,0].tolist()

df2=df.set_index(list(df)[0])

df2.columns=[i for i in headers]
df2.to_csv("finaltable.csv")