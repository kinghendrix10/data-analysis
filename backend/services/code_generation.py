# backend/services/code_generation.py

def generate_code_snippet(intent):
    if intent == "basic_statistics":
        return """
import pandas as pd

df = pd.read_excel('uploaded_file.xlsx')
print(df.describe())
"""
    elif intent == "correlation_matrix":
        return """
import pandas as pd

df = pd.read_excel('uploaded_file.xlsx')
print(df.corr())
"""
    elif intent == "time_series_analysis":
        return """
import pandas as pd

df = pd.read_excel('uploaded_file.xlsx')
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)
print(df['column_name'].resample('M').mean())
"""
    else:
        return "# No code snippet available for this intent."
