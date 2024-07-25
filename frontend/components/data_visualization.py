import streamlit as st
import plotly.express as px
import pandas as pd

def data_visualization_component(data=None):
    if data is None:
        st.write("No data available for visualization.")
        return

    df = pd.DataFrame(data)
    if not df.empty:
        st.write("Data Visualization:")
        fig = px.line(df, x='x', y='y')
        st.plotly_chart(fig)
    else:
        st.write("No data available for visualization.")
