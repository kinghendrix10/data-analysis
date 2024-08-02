import pandas as pd
import altair as alt
import streamlit as st

# Load data from CSV file
df = pd.read_csv('temp_data.csv')

# Convert 'Date' column to datetime type
df['Date'] = pd.to_datetime(df['Date'])

# Filter data for last four months
last_four_months = df[df['Date'] >= df['Date'].max() - pd.DateOffset(months=4)]

# Filter data for 'Rent' expenses
rent_expenses = last_four_months[last_four_months['Description'].str.contains('Rent')]

# Group data by month and calculate total rent expense
rent_expenses_monthly = rent_expenses.resample('M', on='Date')['Amount'].sum().reset_index()

# Create bar chart
chart = alt.Chart(rent_expenses_monthly).mark_bar().encode(
    x='Date:T',
    y='Amount:Q'
)

# Display chart
st.altair_chart(chart, use_container_width=True)