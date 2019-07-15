import pandas as pd
import os

dirname = os.path.dirname(__file__)
dataset_size_location = "../tuxml-size-analysis-datasets/all_size_withyes.pkl"
dataset_size_filename = os.path.join(dirname, dataset_size_location)

def load_dataset(): 
    return pd.read_pickle(dataset_size_filename)
