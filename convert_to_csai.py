#!/usr/bin/env python
# coding: utf-8

# # Data Conversion
# There is Question/Answer (QA) data inside of `STACIA_QA`.
# 
# The goal of this notebook is to read all of the csv files into a `pandas.DataFrame`
# 
# Then reformat the data to fit the CSAI style.
# 
# Finally, output a CSV file of the newly structured data. 

# In[1]:


from os import listdir, getcwd
from os.path import join
from RedirectStdStreams import RedirectStdStreams
from io import StringIO
import pandas as pd
import re
import numpy as np
import pandas_profiling


# In[2]:


DATA_DIR = 'STACIA_QA'
DIR = join(getcwd(), DATA_DIR)


# In[3]:


files = listdir(DATA_DIR)


# In[4]:


def startswith(y):
    return lambda x: x.startswith(y)


# In[5]:


cs_files = sorted(filter(startswith('cs'), files))
stat_files = sorted(filter(startswith('stat'), files))
club_files = sorted(filter(startswith('club'), files))


# In[6]:


def make_data_frame_from_files(files):
    '''given stacia_qa csv files, return a pandas DataFrame containing the enclosed data'''
    # encodings: https://stackoverflow.com/q/19699367/5411712
    # list-of-encodings:
    # https://docs.python.org/3/library/codecs.html#standard-encodings
    df = pd.DataFrame()
    for fname in files:
        fpath = join(DIR, fname)
        to_concat = [df]
        to_concat.append(
            pd.read_csv(fpath,
                        sep='|',
                        encoding='latin_1',
                        header=None,
                        # fun fact: setting the `names` param avoids warnings
                        # because then pandas knows how many columns to make
                        # also the purpose of the "other" columns is to catch weird 
                        # extras that would otherwise be trimmed off after the delimeter
                        names=['id','q_format','a_format','notes','other','other2','other3'],
                        error_bad_lines=False,
                        warn_bad_lines=True))
        df = pd.concat(to_concat)
        print(fname, "done", "....on to the next one....")
    return df


# In[7]:


cs_df   = make_data_frame_from_files(cs_files)
stat_df = make_data_frame_from_files(stat_files)
club_df = make_data_frame_from_files(club_files)


# In[8]:


# remove the comments at the end of each file 
cs_df = cs_df[cs_df['id'].str.startswith("[") != True]
stat_df = stat_df[stat_df['id'].str.startswith("[") != True]
club_df = club_df[club_df['id'].str.startswith("[") != True]

all_df = pd.concat([cs_df, stat_df, club_df])


# ## Let's have a quick look at `all_df`

# In[9]:


print('all_df.shape:', all_df.shape)
print('So there are {} question/answer pairs'.format(all_df.shape[0]))
all_df.tail()


# ## Is there bad data?  `yes` 😢

# In[10]:


def make_weird_columns_mask(df):
    '''given a pandas DataFrame of STACIA_QA data, return a mask to find the rows with extra columns'''
    wierd_columns_mask = df['notes'].notnull() 
    wierd_columns_mask |= df['other'].notnull() 
    wierd_columns_mask |= df['other2'].notnull() 
    wierd_columns_mask |= df['other3'].notnull()
    return wierd_columns_mask


# In[11]:


wierd_columns_mask = make_weird_columns_mask(all_df)
needs_to_be_fixed = all_df[wierd_columns_mask]
print('needs_to_be_fixed.shape:', needs_to_be_fixed.shape)
print('So there are {} rows that do not follow the standard STACIA_QA format'.format(needs_to_be_fixed.shape[0]))


# In[12]:


all_df[wierd_columns_mask].head()


# In[13]:


all_df[wierd_columns_mask].tail()


# ## Frankly, `84` bad rows is so few that it might be reasonable to drop those rows

# In[14]:


all_df[wierd_columns_mask != True][['id','q_format','a_format']].head()


# In[15]:


all_df[wierd_columns_mask != True][['id','q_format','a_format']].tail()


# ## Finally, some reasonable looking data!
# ### To be continued...

# In[16]:


pandas_profiling.ProfileReport(all_df).to_file('index.html')


# In[ ]:




