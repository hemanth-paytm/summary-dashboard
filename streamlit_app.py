import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

# --------------------------------------------------------------------
# 1. LOAD THE CSV DATA
# --------------------------------------------------------------------
@st.cache_data
def load_data():

    DATA_FILENAME = Path(__file__).parent / "data/summary_data_1.csv"
    df = pd.read_csv(DATA_FILENAME)
    
    # Convert session_date to datetime
    df['session_date'] = pd.to_datetime(df['session_date'], errors='coerce')

    # Convert session_date to date
    #df['session_date'] = pd.to_datetime(df['session_date'], errors='coerce').dt.date

    # Convert key columns from string to numeric if needed
    df['session_month'] = pd.to_numeric(df['session_month'], errors='coerce')
    df['session_week']  = pd.to_numeric(df['session_week'],  errors='coerce')
    df['session_count'] = pd.to_numeric(df['session_count'], errors='coerce')
    df['week_txn_counts'] = pd.to_numeric(df['week_txn_counts'], errors='coerce')
    
    return df

# --------------------------------------------------------------------
# 2. SETUP STREAMLIT APP & INTRO
# --------------------------------------------------------------------
st.set_page_config(page_title="Week-wise Contact Ratio", layout="wide")
df = load_data()

st.title("Week-wise vs. Date-wise Contact Ratio Dashboard")

# --------------------------------------------------------------------
# 3. USER INPUT: WEEK RANGE
# --------------------------------------------------------------------
min_week_in_data = int(df['session_week'].min())
max_week_in_data = int(df['session_week'].max())

min_week, max_week = st.slider(
    "Select the session_week range:",
    min_value=min_week_in_data,
    max_value=max_week_in_data,
    value=(min_week_in_data, max_week_in_data)
)

# Filter data to only keep rows within the chosen week range
filtered_df = df[
    (df['session_week'] >= min_week) &
    (df['session_week'] <= max_week)
].copy()

# --------------------------------------------------------------------
# 4. WEEKLY AGGREGATION & CHART
# --------------------------------------------------------------------
st.subheader("1) Weekly Contact Ratio Chart")

# Group daily rows by session_week
weekly_df = filtered_df.groupby('session_week', as_index=False).agg(
    sum_session=('session_count', 'sum'),
    avg_week_txn=('week_txn_counts', 'mean')
)

# Calculate contact ratio for each week
weekly_df['contact_ratio'] = (
    1_000_000 * weekly_df['sum_session'] / weekly_df['avg_week_txn']
)

# Sort weeks in ascending order
weekly_df.sort_values(by='session_week', ascending=False, inplace=True)

# Convert session_week to string to avoid decimals on x-axis
weekly_df['WeekStr'] = weekly_df['session_week'].astype(int).astype(str)

# Plot the weekly contact ratio
st.line_chart(
    data=weekly_df,
    x='WeekStr',
    y='contact_ratio',
    height=400
)

# --------------------------------------------------------------------
# 5. DATE-WISE AGGREGATION & CHART
# --------------------------------------------------------------------
st.subheader("2) Date-wise Contact Ratio Chart")

# Now we group by session_date to get a separate point for each calendar day
daily_df = filtered_df.groupby('session_date', as_index=False).agg(
    sum_session=('session_count', 'sum'),
    avg_week_txn=('week_txn_counts', 'mean')
)

# Calculate contact ratio for each date
daily_df['contact_ratio'] = (
    1_000_000 * daily_df['sum_session'] / daily_df['avg_week_txn']
)

# Sort dates
daily_df.sort_values(by='session_date', ascending=False, inplace=True)

# Plot date-wise contact ratio
# We can keep session_date as a date for the x-axis to show real calendar dates
st.line_chart(
    data=daily_df,
    x='session_date',
    y='contact_ratio',
    height=400
)

# --------------------------------------------------------------------
# 6. TABULAR VIEWS
# --------------------------------------------------------------------

st.subheader("Weekly & Daily Data Tables")

# Remove columns, display tables in a vertical layout
st.write("**Weekly Aggregation**")
st.dataframe(weekly_df)

st.write("**Daily Aggregation**")
st.dataframe(daily_df)