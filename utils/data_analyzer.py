# data_analysis_app/utils/data_analyzer.py

import pandas as pd
import numpy as np

class DataAnalyzer:
    @staticmethod
    def describe_data(data):
        return data.describe()

    @staticmethod
    def correlation_matrix(data):
        return data.corr()

    @staticmethod
    def group_by_analysis(data, group_column, agg_column, agg_func='mean'):
        return data.groupby(group_column)[agg_column].agg(agg_func)

    @staticmethod
    def time_series_analysis(data, date_column, value_column):
        data[date_column] = pd.to_datetime(data[date_column])
        return data.set_index(date_column)[value_column].resample('D').mean()

    @staticmethod
    def detect_outliers(data, column, method='zscore', threshold=3):
        if method == 'zscore':
            z_scores = np.abs((data[column] - data[column].mean()) / data[column].std())
            return data[z_scores > threshold]
        elif method == 'iqr':
            Q1 = data[column].quantile(0.25)
            Q3 = data[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            return data[(data[column] < lower_bound) | (data[column] > upper_bound)]
        else:
            raise ValueError(f"Unsupported outlier detection method: {method}")
