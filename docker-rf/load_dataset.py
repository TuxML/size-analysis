import pandas as pd
import json

'''def load_dataset():

    #Get columns for optimization
    with open("./option_columns.json","r") as f:
        option_columns = json.load(f)

    #Find the dataset
    df = pd.read_csv("./dataset_encoded_all_size.csv", dtype={k:"int8" for k in option_columns})

    #Filter and clean the data
    df.query("cid >= 30000", inplace=True)
    df.fillna(-1, inplace=True)
    df.query("vmlinux >= 0", inplace=True)
    
    #Add the nbyes column
    NBYES = "nbyes"
    def nbyes(row):
        return sum(row == 1)                    
    df[NBYES] = df.apply(nbyes, axis=1)

    return df'''


def load_dataset(nb_yes):
    df = pd.read_pickle("all_size_withyes.pkl")
    if nb_yes == 0:
        df.drop(columns=["nbyes"])
    return df