#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import json

print ("Starting...")
with open("option_columns.json","r") as f:
    option_columns = json.load(f)

print ("(end JSON")
print ("loading CSV")
#Find the dataset
df = pd.read_csv("dataset_encoded_size.csv", dtype={k:"int8" for k in option_columns})

df.query("cid >= 30000", inplace=True)
df.fillna(-1, inplace=True)
df.query("kernel_size >= 0", inplace=True)

print("done for CSV")

# In[23]:


with open("optionsRelatedToSize.txt") as f:
    options_about_size = f.readlines()
options_about_size = [x.strip() for x in options_about_size] 
options_distr = pd.DataFrame(columns=["option", "val_0", "val_1", "val_2"])
i = 0
for o in options_about_size:
    vals = df[o].value_counts()
    nvals = vals.sum()
    print(o)
    val0 = 0
    val1 = 0
    val2 = 0
    for k, v in vals.iteritems():
        if (k == 0):
            val0 = v
        elif (k == 1):
            val1 = v
        elif (k == 2):
            val2 == v
        print(k, v, "(", (v / nvals) * 100, "%)")
    options_distr.loc[i] = (o, val0, val1, val2)
    i = i + 1
        
    
print (options_distr)

# In[48]:


# TODO: you can plot the whole (20 here)
#import matplotlib.pyplot as plt
#fig = plt.figure()
#ax = options_distr[:20].plot.bar(figsize=(20, 10))
#ax.set_xticklabels(options_distr['option'].values)
#plt.show()


# In[49]:


#options_distr


# In[ ]:




