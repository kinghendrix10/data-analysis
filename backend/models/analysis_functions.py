# backend/models/analysis_functions.py

import pandas as pd
import numpy as np

def basic_statistics(df):
    return df.describe().to_json()

def correlation_matrix(df):
    return df.corr().to_json()

def time_series_analysis(df, column):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    return df[column].resample('M').mean().to_json()
