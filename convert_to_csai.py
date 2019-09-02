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
    fpath = join(DIR, fname)
    warnings = StringIO() # to catch the warnings
    with RedirectStdStreams(stderr=warnings):
        pd.read_csv(fpath, 
                    sep='|',
                    encoding='latin_1',
                    header=None,
                    error_bad_lines=False,
                    warn_bad_lines=True)
    warnings.seek(0)
    warns = warnings.read()
    warnings.close()

    if len(warns)>10:
        # for whatever reason the warnings look like "b'Skipping...'\n"
        # so chop off the weird stuff on the edges
        warns = warns[2:len(warns)-2]
        warns = warns.replace('\\n','\n')
        with StringIO(warns) as w:
            warn_df = pd.read_csv(w, sep='\n', header=None)
            warn_df.columns=['warns']
            # https://chrisalbon.com/python/data_wrangling/pandas_regex_to_create_columns/
            warn_df['skipped_lines'] = warn_df['warns'].str.extract('Skipping line (\d+)', expand=True)
            warn_df['expected_cols'] = warn_df['warns'].str.extract('expected (\d+)', expand=True)
            warn_df['actual_cols'] = warn_df['warns'].str.extract('saw (\d+)', expand=True)

            with open(fpath, encoding='latin_1') as f:
                lines = f.readlines()
                line_num = int(warn_df['skipped_lines'][0])
                bad_line = lines[line_num - 1] # because lines are 1-indexed
                print('bad_line is #',line_num,'...',bad_line)

    print(fname,"done","....on to the next one....")

for fname in stat_files:
    warnings = StringIO() # to catch the warnings
    with RedirectStdStreams(stderr=warnings):
        pd.read_csv(join(DIR, fname), 
                    sep='|',
                    encoding='latin_1',
                    header=None,
                    error_bad_lines=False,
                    warn_bad_lines=True)
    warnings.seek(0)
#    print("warnings??",warnings.read())
    print(fname,"done","....on to the next one....")

for fname in club_files:
    warnings = StringIO() # to catch the warnings
    with RedirectStdStreams(stderr=warnings):
        pd.read_csv(join(DIR, fname), 
                    sep='|',
                    encoding='latin_1',
                    header=None,
                    error_bad_lines=False,
                    warn_bad_lines=True)
    warnings.seek(0)
#    print("warnings??",warnings.read())
    print(fname,"done","....on to the next one....")
