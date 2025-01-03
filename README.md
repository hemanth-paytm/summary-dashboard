# :earth_americas: Contact Ratio Dashboard - Weekly + Daily

This dashboard uses **Streamlit** to display weekly and daily **contact ratio** data. Follow the steps below to set it up and run it.

---

## 1. Add Your CSV File
- Ensure your CSV file, named `summary_data_1.csv`, is in the `data/` folder (or at a path referenced in the script).
- The CSV columns should include:
  - `session_date`
  - `session_month`
  - `session_week`
  - `session_count`
  - `week_txn_counts`

If you have different column names or file paths, **update** the `load_data()` function accordingly.

---

## 2. Understand the Columns
1. **`session_date`**: Date (converted to a Python `date`).
2. **`session_month`**: Month number (e.g. `12` for December).
3. **`session_week`**: Week number (e.g. `49`, `50`).
4. **`session_count`**: Number of sessions in that day.
5. **`week_txn_counts`**: Daily or average transaction count for that week.

---

## 3. How Contact Ratio is Calculated
For both weekly and daily aggregations, we use the formula:

> contact_ratio = 1,000,000 * ( sum(session_count) / mean(week_txn_counts) )

- **Weekly Aggregation**: All daily rows for a given `session_week` are summed (for session counts) and averaged (for `week_txn_counts`), then plugged into the formula.
- **Daily Aggregation**: Rows are grouped by `session_date`. Each date’s session counts are summed, and `week_txn_counts` is averaged for that date.

---

## 4. Interact with the Dashboard
- **Week Range Slider**: Adjust the minimum and maximum `session_week`.
- **Charts**:
  - **Weekly**: Shows a single data point per `session_week`.
  - **Daily**: Shows each `session_date` as a single data point.
- **Tables**: Display both the weekly and daily aggregated data.

---
