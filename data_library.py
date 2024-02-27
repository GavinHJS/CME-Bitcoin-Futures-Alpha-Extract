# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 21:48:57 2024

@author: Gavin
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class data():
    def __init__(self , contract_number: int):
        self.data_list =  ["CME Chicago Mercantile Exchange Micro Bitcoin Electronic Commodity Future",
                         "CME Chicago Mercantile Exchange Bitcoin Electronic Commodity Future",
                         "CME Chicago Mercantile Exchange Micro Bitcoin Electronic Commodity Index Future",
                         "CME - Bitcoin Composite Index Future"
                         ]
        self.contract_type = contract_number
        prices = pd.read_parquet("./Data/Historical Levels_Futures.CSV.parquet")
        cols_with_string = [col for col in prices.columns if self.data_list[self.contract_type] in col]
        df = prices[['Date[Date]'] + cols_with_string]
        df = df.rename(columns = {'Date[Date]':'Date'})
        df['Date']  = pd.to_datetime(df['Date'] , format = '%m/%d/%Y')
        
        df = df.set_index("Date")

        for col in cols_with_string:
            df[col] = df[col].str.replace(',', '').astype(float)
        self.data = df
        self.info = {index: element for index, element in enumerate(self.data_list)}
        

    def summary_stats(self):

        print(self.data.describe())
        
    def check_missing_values(self):

        print(self.data.isnull().sum())
        
    def plot_time_series(self, column):

        plt.figure(figsize=(10, 6))
        self.data[column].plot(title=f"Time Series for {column}")
        plt.xlabel("Date")
        plt.ylabel("Value")
        plt.show()
        
    def plot_distribution(self, column):

        plt.figure(figsize=(10, 6))
        sns.histplot(self.data[column], kde=True, bins=30)
        plt.title(f"Distribution of {column}")
        plt.xlabel("Value")
        plt.ylabel("Frequency")
        plt.show()
        
    def calculate_volatility(self, column):

        daily_returns = self.data[column].pct_change()
        volatility = daily_returns.rolling(window=30).std() * np.sqrt(252)
        
        plt.figure(figsize=(10, 6))
        volatility.plot(title=f"30-Day Rolling Volatility for {column}")
        plt.xlabel("Date")
        plt.ylabel("Volatility")
        plt.show()
        
    def correlation_matrix(self):

        correlation = self.data.corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Correlation Matrix")
        plt.show()