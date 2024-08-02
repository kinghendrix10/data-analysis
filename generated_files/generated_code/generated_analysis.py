import pandas as pd
import altair as alt
import streamlit as st

# Load data from CSV file
df = pd.read_csv('temp_data.csv')

# Filter data for the last four months
df['Date'] = pd.to_datetime(df['Date'])
last_four_months = df[df['Date'] >= df['Date'].max() - pd.DateOffset(months=4)]

# Filter data for 'Rent' category
rent_data = last_four_months[last_four_months['Description'].str.contains('Rent')]

# Group data by month and calculate total 'Amount' for each month
rent_data['Month'] = rent_data['Date'].dt.to_period('M')
rent_expenses = rent_data.groupby('Month')['Amount'].sum().reset_index()

# Create a bar chart using Altair
chart = alt.Chart(rent_expenses).mark_bar().encode(
    x='Month',
    y='Amount'
)

# Display the chart
st.altair_chart(chart, use_container_width=True)