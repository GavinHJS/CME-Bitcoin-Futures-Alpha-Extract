import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


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
    
    # df = df.pct_change()
    return df
    
    
    
    
    
if __name__ =="__main__":
    df = get_returns("CME - Bitcoin Composite Index Future")