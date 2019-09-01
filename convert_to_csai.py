#!/usr/bin/env python3

from os import listdir, getcwd
from os.path import join

DATA_DIR = 'STACIA_QA'
DIR = join(getcwd(), DATA_DIR)

files = listdir(DATA_DIR)

cs_files = [f for f in filter(lambda x: x.startswith('cs'), files)]
stat_files = [f for f in filter(lambda x: x.startswith('stat'), files)]
club_files = [f for f in filter(lambda x: x.startswith('club'), files)]

# encodings: https://stackoverflow.com/q/19699367/5411712
for fname in cs_files:
    with open(join(DIR, fname), 'r', encoding='ISO-8859-1') as f:
        print(f.read())

for fname in stat_files:
    with open(join(DIR, fname), 'r', encoding='ISO-8859-1') as f:
        print(f.read())

for fname in club_files:
    with open(join(DIR, fname), 'r', encoding='ISO-8859-1') as f:
        print(f.read())
