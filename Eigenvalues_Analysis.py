import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.stats import rankdata

import matplotlib.pyplot as plt

os.chdir(r"D:\CME-Bitcoin-Futures-Alpha-Extract")


def data_describe():
    list_of_names = ["CME Chicago Mercantile Exchange Micro Bitcoin Electronic Commodity Future",
                     "CME Chicago Mercantile Exchange Bitcoin Electronic Commodity Future",
                     "CME Chicago Mercantile Exchange Micro Bitcoin Electronic Commodity Index Future",
                     "CME - Bitcoin Composite Index Future"
                     ]
    return list_of_names

def convert_parquet(directory:str):
    directory = os.path.abspath(directory)
    for files in os.listdir(directory):
        file_path = os.path.join(directory, files)
        print("Converting csv to parquet for file : ", file_path)
        df = pd.read_csv(file_path)
        df.to_parquet("./Data/"+files+'.parquet', engine='fastparquet')
    
def get_returns(contract_type:str):
    prices = pd.read_parquet("./Data/Historical Levels_Futures.CSV.parquet")
    cols_with_string = [col for col in prices.columns if contract_type in col]
    df = prices[['Date[Date]'] + cols_with_string]
    df = df.rename(columns = {'Date[Date]':'Date'})
    df['Date']  = pd.to_datetime(df['Date'] , format = '%m/%d/%Y')
    
    df = df.set_index("Date")

    for col in cols_with_string:
        df[col] = df[col].str.replace(',', '').astype(float)
    
    
    return df.pct_change()
    
    
    
    
if __name__ =="__main__":
    returns = get_returns("CME - Bitcoin Composite Index Future")
    xxx = returns.describe().T
    coins = xxx[xxx['count'] > 500].index

    returns = returns[coins].iloc[-500:]

    corr = returns.corr()
    tri_a, tri_b = np.triu_indices(len(corr), k=1)
 
    flat_corr = corr.values[tri_a, tri_b]

    plt.hist(flat_corr, bins=100)
    plt.axvline(flat_corr.mean(), color='k')
    plt.show()
    eigenvals, eigenvecs = np.linalg.eig(corr)
    idx = eigenvals.argsort()[::-1]   
    pca_eigenvecs = eigenvecs[:, idx]
    plt.hist(pca_eigenvecs[:, 0])
    plt.show()
    plt.figure(figsize=(18, 6))
    plt.plot(pca_eigenvecs[:, 0])
    plt.axhline(np.mean(pca_eigenvecs[:, 0]), color='k', linestyle='--')
    plt.xticks(range(len(returns.columns)), returns.columns, rotation=90)
    plt.show()
    corr_weight = corr.sum(axis=1)
    
    corr_weight.sort_values()
    normalized_weights = sum(pca_eigenvecs[:, 0]) * corr_weight / corr_weight.sum()

    normalized_weights.sum(), sum(pca_eigenvecs[:, 0])
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    plt.scatter(normalized_weights, pca_eigenvecs[:, 0])
    plt.subplot(1, 2, 2)
    plt.scatter(rankdata(normalized_weights),
                rankdata(pca_eigenvecs[:, 0]));
    plt.show()