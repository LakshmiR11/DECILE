import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(page_title="Customer Decile Dashboard", layout="wide")

st.title("📊 Customer Decile Analysis Dashboard")

# -----------------------------------
# LOAD DATA
# -----------------------------------
@st.cache_data
def load_data():
    return pd.read_csv(r"C:\Users\Sudha\Desktop\customer_data.csv")  # Replace with your file

df = load_data()

# -----------------------------------
# SIDEBAR FILTERS
# -----------------------------------
st.sidebar.header("🔎 Filters")

brand_filter = st.sidebar.multiselect(
    "Select Brand",
    options=df['Brand'].unique(),
    default=df['Brand'].unique()
)

region_filter = st.sidebar.multiselect(
    "Select Region",
    options=df['region'].unique(),
    default=df['region'].unique()
)

# Apply filters
filtered_df = df[
    (df['Brand'].isin(brand_filter)) &
    (df['region'].isin(region_filter))
].copy()

# -----------------------------------
# KPI SECTION
# -----------------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Customers", len(filtered_df))
col2.metric("Total Sales", f"{filtered_df['Sale value'].sum():,.0f}")
col3.metric("Average Sales", f"{filtered_df['Sale value'].mean():,.2f}")

st.divider()

# -----------------------------------
# CREATE DECILES
# -----------------------------------
if len(filtered_df) >= 10:

    filtered_df = filtered_df.sort_values(by='Sale value', ascending=False)

    filtered_df['Decile'] = pd.qcut(
        filtered_df['Sale value'],
        10,
        labels=range(1, 11)
    )

    # -----------------------------------
    # SUMMARY TABLE
    # -----------------------------------
    summary = (
        filtered_df
        .groupby('Decile')
        .agg(
            Total_Sales=('Sale value', 'sum'),
            Customer_Count=('Cust Name', 'count'),
            Avg_Sales=('Sale value', 'mean')
        )
        .sort_index()
        .reset_index()
    )

    # -----------------------------------
    # DISPLAY SUMMARY
    # -----------------------------------
    st.subheader("📋 Decile Summary")
    st.dataframe(summary, use_container_width=True)

    # -----------------------------------
    # BAR CHART
    # -----------------------------------
    st.subheader("📊 Total Sales by Decile")

    fig, ax = plt.subplots()
    ax.bar(summary['Decile'], summary['Total_Sales'])
    ax.set_xlabel("Decile (1 = Highest Sales)")
    ax.set_ylabel("Total Sales")
    ax.set_title("Decile-wise Sales Distribution")

    st.pyplot(fig)

    # -----------------------------------
    # DETAILED DATA
    # -----------------------------------
    st.subheader("📑 Detailed Data with Deciles")
    st.dataframe(filtered_df, use_container_width=True)

    # -----------------------------------
    # DOWNLOAD BUTTON
    # -----------------------------------
    csv = filtered_df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="⬇ Download Filtered Data",
        data=csv,
        file_name="filtered_decile_report.csv",
        mime="text/csv"
    )

else:
    st.warning("⚠ Not enough customers to create 10 equal deciles.")

