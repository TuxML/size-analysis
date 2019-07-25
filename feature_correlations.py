#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import os

IGRIDA=True 
if (IGRIDA):
    dirname = os.path.dirname(__file__)
    dataset_size_location = "../rf-analysis/all_size_withyes.pkl"
    dataset_size_filename = os.path.join(dirname, dataset_size_location) 
    df = pd.read_pickle(dataset_size_filename)
#else:
#    import tuxml
#    df = tuxml.load_dataset()


# In[ ]:


size_methods = ["vmlinux", "GZIP-bzImage", "GZIP-vmlinux", "GZIP", "BZIP2-bzImage", 
              "BZIP2-vmlinux", "BZIP2", "LZMA-bzImage", "LZMA-vmlinux", "LZMA", "XZ-bzImage", "XZ-vmlinux", "XZ", 
              "LZO-bzImage", "LZO-vmlinux", "LZO", "LZ4-bzImage", "LZ4-vmlinux", "LZ4"]


# In[ ]:


def _filter(df):
    return df.drop(columns=["cid"]).drop(columns=size_methods)
fdf = _filter(df)

dict_corr = []
def _samecolumns_after_ithcolumn(fd, i):
    col_i = fd[fd.columns[i]] # the column we want to compare with
    for j in range(i+1, len(fd.columns) - 1):
        if (col_i.equals(fd[fd.columns[j]])):
            dict_corr.append({fd.columns[i] : fd.columns[j]})

# TIME CONSUMING !!
# can be tuned
starting_point = 9000
ending_point = len(fdf)
for i in range(starting_point, ending_point):
    _samecolumns_after_ithcolumn(fdf, i)


# In[ ]:

pd.DataFrame(dict_corr).to_csv('ft-correlations-' + str(starting_point) + '-' + str(ending_point) + '.csv')




