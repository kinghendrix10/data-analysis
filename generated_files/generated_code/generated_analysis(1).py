import pandas as pd
import altair as alt
import streamlit as st

# Load data from CSV file
data = pd.read_csv('temp_data.csv')

# Convert 'Date' column to datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Filter data for last four months
last_four_months = data[data['Date'] >= data['Date'].max() - pd.DateOffset(months=4)]

# Filter 'Rent' category
rent_expenses = last_four_months[last_four_months['Description'].str.contains('Rent')]

# Group by month and calculate sum of 'Amount'
rent_expenses_monthly = rent_expenses.resample('M', on='Date')['Amount'].sum().reset_index()

# Create bar chart
chart = alt.Chart(rent_expenses_monthly).mark_bar().encode(
    x='Date:T',
    y='Amount:Q'
)

# Display full width interactive chart
st.altair_chart(chart, use_container_width=True)