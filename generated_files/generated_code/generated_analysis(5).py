import pandas as pd
import altair as alt
import streamlit as st

# Load data from CSV file
data = pd.read_csv('temp_data.csv')

# Preprocess data: filter rent-related transactions and get last four months
data['Date'] = pd.to_datetime(data['Date'])
data = data[(data['Description'].str.contains('Rent')) & (data['Date'] >= data['Date'].max() - pd.DateOffset(months=4))]
data = data.groupby(data['Date'].dt.to_period('M')).agg({'Amount': 'sum'}).reset_index()
data.columns = ['Date', 'Amount']

# Create bar chart with Altair
chart = alt.Chart(data).mark_bar().encode(
    x='Date',
    y='Amount'
)

# Display chart with Streamlit
st.altair_chart(chart, use_container_width=True)