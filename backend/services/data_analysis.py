# backend/services/data_analysis.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def perform_analysis(data):
    # Example analysis function
    df = pd.DataFrame(data)
    fig = px.line(df, x='Date', y='Value', title='Line Chart')
    return fig.to_json()
