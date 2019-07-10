#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd

df = pd.read_pickle("all_size_withyes.pkl")
df[:10]
df.shape


# In[4]:


df.sort_values("vmlinux")


# In[5]:


size_methods = ["vmlinux", "GZIP-bzImage", "GZIP-vmlinux", "GZIP", "BZIP2-bzImage", 
              "BZIP2-vmlinux", "BZIP2", "LZMA-bzImage", "LZMA-vmlinux", "LZMA", "XZ-bzImage", "XZ-vmlinux", "XZ", 
              "LZO-bzImage", "LZO-vmlinux", "LZO", "LZ4-bzImage", "LZ4-vmlinux", "LZ4"]


# In[7]:


import matplotlib.pyplot as plt
plt.figure()
pd.DataFrame(df['vmlinux']).plot.box()
plt.show(block=False)

plt.figure()
pd.DataFrame(df['LZO']).plot.box()
plt.show(block=False)

plt.figure()
pd.DataFrame(df['BZIP2']).plot.box()
plt.show(block=False)


df['vmlinux'].describe()


# In[ ]:





# In[9]:


import scipy.stats
import seaborn as sns
import numpy as np



def color_negative_positive(val, pcolor="green", ncolor="red"):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    color = pcolor if val > 0 else ncolor 
    if val == 0:
        color = 'black' 
    return 'color: %s' % color

compress_methods = ["GZIP", "BZIP2", "LZMA", "XZ", "LZO", "LZ4"]
def compareCompress(size_measure_of_interest): #"" # "-vmlinux" #"-bzImage" # prefix
    rCompressDiff = pd.DataFrame(index=list(map(lambda c: c + "o", compress_methods)) , columns=compress_methods) 
    for compress_method in compress_methods:
        for compress_method2 in compress_methods:
            rCompressDiff.loc[compress_method + "o"][compress_method2] = (np.mean(df[compress_method + size_measure_of_interest] / df[compress_method2 + size_measure_of_interest]) * 100) - 100
    return rCompressDiff

#cmy = sns.light_palette("red", as_cmap=True)
compareCompress("").style.set_caption('Difference (average in percentage) per compression methods').applymap(color_negative_positive)


# In[10]:


compareCompress("-vmlinux").style.set_caption('Difference (average in percentage) per compression methods, vmlinux').applymap(color_negative_positive)


# In[11]:


cm = sns.light_palette("green", as_cmap=True)
print(pd.DataFrame.corr(df[size_methods]).style.set_caption('Correlations between size measures').background_gradient(cmap=cm))

# In[ ]:




