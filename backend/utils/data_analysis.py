import pandas as pd

def analyze_data(df: pd.DataFrame):
    # Example analysis
    summary = df.describe()
    return summary