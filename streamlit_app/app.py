import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Customer Churn Analytics",
    layout="wide"
)

# ------------------ LOAD DATA ------------------
df = pd.read_csv(
    "data/WA_Fn-UseC_-Telco-Customer-Churn.csv"
)

# ------------------ CLEAN DATA ------------------
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df = df.dropna()

# ------------------ SIDEBAR FILTERS ------------------
st.sidebar.header("Filters")

contract_filter = st.sidebar.multiselect(
    "Contract Type",
    df["Contract"].unique(),
    default=df["Contract"].unique(),
    key="contract_filter"
)

internet_filter = st.sidebar.multiselect(
    "Internet Service",
    df["InternetService"].unique(),
    default=df["InternetService"].unique(),
    key="internet_filter"
)

payment_filter = st.sidebar.multiselect(
    "Payment Method",
    df["PaymentMethod"].unique(),
    default=df["PaymentMethod"].unique(),
    key="payment_filter"
)

# Apply filters
filtered_df = df[
    (df["Contract"].isin(contract_filter)) &
    (df["InternetService"].isin(internet_filter)) &
    (df["PaymentMethod"].isin(payment_filter))
]

# ------------------ KPIs ------------------
total_customers = len(filtered_df)

churn_rate = (filtered_df["Churn"] == "Yes").mean() * 100

revenue = filtered_df["MonthlyCharges"].sum()

revenue_at_risk = filtered_df.loc[
    filtered_df["Churn"] == "Yes",
    "MonthlyCharges"
].sum()

# ------------------ TITLE ------------------
st.title("Customer Churn & Revenue Risk Analytics Dashboard")

st.markdown("### Executive Summary")
st.info(
"""
This dashboard analyses customer churn behaviour and identifies revenue-at-risk segments.
It helps businesses improve retention strategies using data-driven insights.
"""
)

# ------------------ KPI CARDS ------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Customers", f"{total_customers:,}")
c2.metric("Churn Rate", f"{churn_rate:.2f}%")
c3.metric("Revenue", f"${revenue:,.0f}")
c4.metric("Revenue at Risk", f"${revenue_at_risk:,.0f}")

# ------------------ CHART 1 ------------------
st.subheader("Contract Type vs Churn")

fig1 = px.histogram(
    filtered_df,
    x="Contract",
    color="Churn",
    barmode="group"
)

st.plotly_chart(fig1, use_container_width=True)

# ------------------ CHART 2 ------------------
st.subheader("Tenure Distribution")

fig2 = px.box(
    filtered_df,
    x="Churn",
    y="tenure"
)

st.plotly_chart(fig2, use_container_width=True)

# ------------------ CHART 3 ------------------
st.subheader("Payment Method vs Churn")

fig3 = px.histogram(
    filtered_df,
    x="PaymentMethod",
    color="Churn"
)

st.plotly_chart(fig3, use_container_width=True)

# ------------------ REVENUE AT RISK ------------------
st.subheader("Revenue at Risk by Contract")

rev_by_contract = filtered_df[
    filtered_df["Churn"] == "Yes"
].groupby("Contract")["MonthlyCharges"].sum().reset_index()

fig4 = px.bar(
    rev_by_contract,
    x="Contract",
    y="MonthlyCharges"
)

st.plotly_chart(fig4, use_container_width=True)

# ------------------ HIGH RISK CUSTOMERS ------------------
st.subheader("Top 10 High-Risk Customers")

risk_df = filtered_df[filtered_df["Churn"] == "Yes"].copy()

risk_df = risk_df.sort_values(
    by="MonthlyCharges",
    ascending=False
)

st.dataframe(
    risk_df[[
        "gender",
        "Contract",
        "tenure",
        "MonthlyCharges",
        "TotalCharges"
    ]].head(10)
)

# ------------------ INSIGHTS ------------------
st.subheader("Key Business Insights")

st.success(
"""
• Month-to-month customers show highest churn risk  
• Long-term contracts significantly improve retention  
• Higher monthly charges correlate with churn risk  
• Early-tenure customers are more likely to churn  
"""
)

# ------------------ DOWNLOAD DATA ------------------
st.subheader("Download Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Dataset",
    data=csv,
    file_name="churn_filtered_data.csv",
    mime="text/csv"
)
st.markdown("## Business Impact")

st.success("""
This analysis helps telecom companies reduce churn by identifying high-risk customers
and estimating revenue loss from customer attrition.

Key outcome:
- Identify churn drivers
- Target high-risk segments
- Improve retention strategy
""")
