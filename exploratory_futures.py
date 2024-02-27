# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 21:56:30 2024

@author: Gavin
"""

import pandas as pd
from data_library import data


contract_number = 0  # For Micro Bitcoin Electronic Commodity Future
column_name = "UTS000000326700587 1M(50)[CME Chicago Mercantile Exchange Micro Bitcoin Electronic Commodity Future\1M"
crypto_data = data(contract_number)

# Summary statistics
crypto_data.summary_stats()

# Check for missing values
crypto_data.check_missing_values()

# Plot a time series for a specific column, replace 'column_name' with the actual column name you're interested in
crypto_data.plot_time_series()

# Plot distribution for a specific column
# crypto_data.plot_distribution('column_name')

# Calculate and plot volatility for a specific column
# crypto_data.calculate_volatility('column_name')

# Correlation matrix between the features
crypto_data.correlation_matrix()