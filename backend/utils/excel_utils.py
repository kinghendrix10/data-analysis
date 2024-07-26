# backend/utils/excel_utils.py

import pandas as pd

def read_excel(file_content):
    return pd.read_excel(file_content)

def read_csv(file_content):
    return pd.read_csv(file_content)
