import pandas as pd
import altair as alt
import streamlit as st

# Load the data
df = pd.read_csv('temp_data.csv')

# Convert the 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Filter the last four months of data
last_four_months = df[df['Date'] >= df['Date'].max() - pd.Timedelta(days=120)]

# Filter the 'Rent' category
rent_expenses = last_four_months[last_four_months['Description'].str.contains('Rent')]

# Group by month and sum the 'Amount' values
rent_expenses = rent_expenses.groupby(pd.Grouper(key='Date', freq='M')).agg({'Amount': 'sum'}).reset_index()

# Create the bar chart
chart = alt.Chart(rent_expenses).mark_bar().encode(
    x='Date:T',
    y='Amount:Q'
)

# Display the chart
st.altair_chart(chart, use_container_width=True)