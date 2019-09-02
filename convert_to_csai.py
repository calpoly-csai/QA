#!/usr/bin/env python3

from os import listdir, getcwd
from os.path import join
from RedirectStdStreams import RedirectStdStreams
from io import StringIO
import pandas as pd

DATA_DIR = 'STACIA_QA'
DIR = join(getcwd(), DATA_DIR)

files = listdir(DATA_DIR)


def startswith(y):
    return lambda x: x.startswith(y)

cs_files = [f for f in filter(startswith('cs'), files)]
stat_files = [f for f in filter(startswith('stat'), files)]
club_files = [f for f in filter(startswith('club'), files)]

# encodings: https://stackoverflow.com/q/19699367/5411712
# list-of-encodings: 
# https://docs.python.org/3/library/codecs.html#standard-encodings
for fname in cs_files:
    warnings = StringIO() # to catch the warnings
    with RedirectStdStreams(stderr=warnings):
        pd.read_csv(join(DIR, fname), 
                    sep='|',
                    encoding='latin_1',
                    error_bad_lines=False,
                    warn_bad_lines=True)
    warnings.seek(0)
    print("warnings??",warnings.read())
    print(fname,"done","....on to the next one....")

for fname in stat_files:
    pd.read_csv(join(DIR, fname), 
                sep='|', 
                encoding='latin_1',
                error_bad_lines=False)

for fname in club_files:
    pd.read_csv(join(DIR, fname), 
                sep='|', 
                encoding='latin_1',
                error_bad_lines=False)
