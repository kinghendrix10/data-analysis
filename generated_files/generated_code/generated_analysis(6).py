import pandas as pd
import altair as alt
import streamlit as st

# Load data from CSV file
data = pd.read_csv('temp_data.csv')

# Filter data for last four months
data['Date'] = pd.to_datetime(data['Date'])
data = data[data['Date'] >= data['Date'].max() - pd.Timedelta(days=120)]

# Filter data for rent expenses
data = data[data['Description'].str.contains('Rent')]

# Group data by month and calculate total rent expenses
data['Month'] = data['Date'].dt.to_period('M')
data_rent = data.groupby('Month')['Amount'].sum().reset_index()

# Create line chart for rent expenses
chart = alt.Chart(data_rent).mark_line().encode(
    x='Month',
    y='Amount'
)

# Display interactive chart
st.altair_chart(chart, use_container_width=True)