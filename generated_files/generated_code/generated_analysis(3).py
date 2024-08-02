import pandas as pd
import streamlit as st
import altair as alt

# Load data from CSV file
data = pd.read_csv('temp_data.csv')

# Convert 'Date' column to datetime type
data['Date'] = pd.to_datetime(data['Date'])

# Filter data for last four months
last_four_months = data[data['Date'] >= data['Date'].max() - pd.DateOffset(months=4)]

# Filter data for 'Rent' category
rent_expenses = last_four_months[last_four_months['Description'].str.contains('Rent', case=False)]

# Select required columns
rent_expenses_table = rent_expenses[['Date', 'Description', 'Amount']]

# Display table
st.dataframe(rent_expenses_table)