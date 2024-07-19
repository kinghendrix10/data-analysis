import streamlit as st
import requests
import plotly.express as px
import pandas as pd

def data_visualization_component():
    response = requests.get("http://localhost:8000/visualization")  # Ensure 'localhost' is used
    if response.status_code == 200:
        data = response.json().get('data')
        if data:
            df = pd.DataFrame(data)
            fig = px.line(df, x='x', y='y')
            st.plotly_chart(fig)
        else:
            st.error("No data found for visualization")
    else:
        st.error("Failed to retrieve visualization")
