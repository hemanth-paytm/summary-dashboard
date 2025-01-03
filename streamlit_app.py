import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

# --------------------------------------------------------------------
# 1. LOAD THE CSV DATA
# --------------------------------------------------------------------
@st.cache_data
def load_data():
    """
    This function loads our CSV file named 'summary_data.csv'.
    It also does basic data type conversions to ensure we can work
    easily with numeric columns like CreatedWeek, Sum_session_count,
    and Avg_week_txn_counts.
    """
    DATA_FILENAME = Path(__file__).parent / "data/summary_data.csv"
    df = pd.read_csv(DATA_FILENAME)
    
    # Parse session_date as datetime, in case you need it later
    df['session_date'] = pd.to_datetime(df['session_date'], errors='coerce')
    
    # Convert columns from string to numeric if needed
    df['CreatedMonth'] = pd.to_numeric(df['CreatedMonth'], errors='coerce')
    df['CreatedWeek'] = pd.to_numeric(df['CreatedWeek'], errors='coerce')
    df['Sum_session_count'] = pd.to_numeric(df['Sum_session_count'], errors='coerce')
    df['Avg_week_txn_counts'] = pd.to_numeric(df['Avg_week_txn_counts'], errors='coerce')
    
    return df

# --------------------------------------------------------------------
# 2. SETUP STREAMLIT APP
# --------------------------------------------------------------------
st.set_page_config(
    page_title="Week-wise Contact Ratio",
    layout="wide"
)

df = load_data()

# Page title and explanation
st.title("Week-wise Contact Ratio Dashboard")
st.markdown("""
Use this dashboard to see how contact ratio changes from **week to week**.

The **contact ratio** formula is:

\\[
\\text{Contact Ratio} = 1{,}000{,}000 \\times \\frac{\\text{Sum\\_session\\_count}}{\\text{Avg\\_week\\_txn\\_counts}}
\\]

Below, choose the minimum and maximum **week numbers** you'd like to analyze.
""")

# --------------------------------------------------------------------
# 3. USER INPUT: WEEK RANGE
# --------------------------------------------------------------------
min_week_in_data = int(df['CreatedWeek'].min())
max_week_in_data = int(df['CreatedWeek'].max())

min_week, max_week = st.slider(
    "Select CreatedWeek range:",
    min_value=min_week_in_data,
    max_value=max_week_in_data,
    value=(min_week_in_data, max_week_in_data)
)

# Filter the data by the selected week range
filtered_df = df[
    (df['CreatedWeek'] >= min_week) & 
    (df['CreatedWeek'] <= max_week)
].copy()

# --------------------------------------------------------------------
# 4. CALCULATE CONTACT RATIO
# --------------------------------------------------------------------
# For each row: contact_ratio = 1,000,000 * (Sum_session_count / Avg_week_txn_counts)
filtered_df['contact_ratio'] = (
    1_000_000 * 
    (filtered_df['Sum_session_count'] / filtered_df['Avg_week_txn_counts'])
)

# --------------------------------------------------------------------
# 5. DISPLAY FILTERED RESULTS
# --------------------------------------------------------------------
st.subheader("Filtered Results")
st.write(
    "Below table shows rows in the selected week range, including the computed 'contact_ratio'."
)
st.dataframe(filtered_df)

# --------------------------------------------------------------------
# 6. PLOT A CHART OF CONTACT RATIO BY WEEK
# --------------------------------------------------------------------
st.subheader("Contact Ratio by CreatedWeek")

# To avoid decimal ticks, we convert week numbers to string.
# We'll create a separate column so the original numeric data is preserved.
filtered_df['WeekStr'] = filtered_df['CreatedWeek'].astype(int).astype(str)

# Sort based on numeric value of the week before converting to string (so it sorts in actual numeric order).
filtered_df.sort_values(by='CreatedWeek', inplace=True)

# Now we can plot with 'WeekStr' as x-axis, which will remain constant (no decimals).
st.line_chart(
    data=filtered_df,
    x='WeekStr',
    y='contact_ratio',
    height=400
)

st.markdown("""
**Interpretation:**
- The x-axis shows each `CreatedWeek` as a category (string), so no decimals appear.
- The y-axis (contact ratio) is scaled by 1,000,000 to avoid small fractional values.
- This chart helps you see how contact ratio changes from one week to another within your chosen range.
""")