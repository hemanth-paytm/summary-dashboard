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
    This function loads our CSV file named 'summary_data.csv' and converts
    the relevant columns to numeric types. We also parse 'session_date'
    as a datetime if needed for future operations.
    """
    DATA_FILENAME = Path(__file__).parent / "data/summary_data.csv"
    df = pd.read_csv(DATA_FILENAME)
    
    # Convert session_date to datetime
    df['session_date'] = pd.to_datetime(df['session_date'], errors='coerce')
    
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

st.title("Week-wise Contact Ratio Dashboard")

st.markdown("""
We have **daily data** with columns like `session_week`, and we want to 
**aggregate** those days to display a **single entry per week**.

**Formula** for the Contact Ratio:

\\[
\\text{Contact Ratio} = 1{,}000{,}000 \\times \\frac{\\sum(\\text{session\\_count})}{\\text{mean}(\\text{week\\_txn\\_counts})}
\\]

Select a range of **session_week** values below to view the weekly totals.
""")

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
# 4. GROUP DATA BY WEEK & CALCULATE CONTACT RATIO
# --------------------------------------------------------------------
#   - Summation for 'session_count' 
#   - Mean for 'week_txn_counts'
#   - Contact Ratio:
#       contact_ratio = 1,000,000 * sum_session / avg_week_txn

grouped_df = filtered_df.groupby('session_week', as_index=False).agg(
    sum_session=('session_count', 'sum'),
    avg_week_txn=('week_txn_counts', 'mean')
)

grouped_df['contact_ratio'] = (
    1_000_000 * grouped_df['sum_session'] / grouped_df['avg_week_txn']
)

# --------------------------------------------------------------------
# 5. DISPLAY RESULTS
# --------------------------------------------------------------------
st.subheader("Weekly Aggregated Table")
st.write("""
Below, each row corresponds to a **single session_week** after aggregation.
We show:
- sum_session (total of daily session_count)
- avg_week_txn (average of daily week_txn_counts)
- contact_ratio (calculated via the formula above)
""")

grouped_df.sort_values(by='session_week', inplace=True)
st.dataframe(grouped_df)

# --------------------------------------------------------------------
# 6. VISUALIZE THE CONTACT RATIO
# --------------------------------------------------------------------
st.subheader("Contact Ratio by session_week")

# Convert session_week to string to ensure no decimals when zooming
grouped_df['WeekStr'] = grouped_df['session_week'].astype(int).astype(str)

st.line_chart(
    data=grouped_df,
    x='WeekStr',
    y='contact_ratio',
    height=400
)

st.markdown("""
**Interpretation:**
- The x-axis shows each `session_week` as a category (string), so no decimals appear.
- The y-axis is the aggregated contact ratio, where each point represents 
  the combined daily data for that week.
""")