import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Customer Churn Analytics",
    layout="wide"
)

df = pd.read_csv(
    "../data/WA_Fn-UseC_-Telco-Customer-Churn.csv"
)

df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

df = df.dropna()

st.sidebar.header("Filters")

contract = st.sidebar.multiselect(
    "Contract Type",
    df["Contract"].unique(),
    default=df["Contract"].unique()
)

internet = st.sidebar.multiselect(
    "Internet Service",
    df["InternetService"].unique(),
    default=df["InternetService"].unique()
)

filtered_df = df[
    (df["Contract"].isin(contract))
    &
    (df["InternetService"].isin(internet))
]

total_customers = len(filtered_df)

churn_rate = (
    (filtered_df["Churn"] == "Yes")
    .mean()
) * 100

revenue = filtered_df[
    "MonthlyCharges"
].sum()

revenue_risk = filtered_df.loc[
    filtered_df["Churn"] == "Yes",
    "MonthlyCharges"
].sum()

st.title(
    "Customer Churn & Revenue Risk Analytics"
)

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Customers",
    f"{total_customers:,}"
)

c2.metric(
    "Churn Rate",
    f"{churn_rate:.2f}%"
)

c3.metric(
    "Revenue",
    f"${revenue:,.0f}"
)

c4.metric(
    "Revenue At Risk",
    f"${revenue_risk:,.0f}"
)

fig1 = px.histogram(
    filtered_df,
    x="Contract",
    color="Churn",
    barmode="group",
    title="Contract Type vs Churn"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

fig2 = px.box(
    filtered_df,
    x="Churn",
    y="tenure",
    title="Customer Tenure Analysis"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

fig3 = px.histogram(
    filtered_df,
    x="PaymentMethod",
    color="Churn",
    title="Payment Method Analysis"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.subheader(
    "Business Recommendations"
)

st.markdown(
"""
- Focus retention campaigns on month-to-month customers.
- Promote annual and two-year contracts.
- Target high-value customers with loyalty programs.
- Improve onboarding for new customers.
"""
)