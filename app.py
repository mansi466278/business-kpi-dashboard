import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Business KPI Dashboard", page_icon="📊", layout="wide")

st.title("Business KPI Dashboard")
st.caption("Interactive sales and customer performance dashboard")

df = pd.read_csv("business_data.csv")
df["date"] = pd.to_datetime(df["date"])
df["revenue"] = df["quantity"] * df["unit_price"]

st.sidebar.header("Filters")

categories = st.sidebar.multiselect(
    "Category",
    sorted(df["category"].unique()),
    default=sorted(df["category"].unique())
)

cities = st.sidebar.multiselect(
    "City",
    sorted(df["city"].unique()),
    default=sorted(df["city"].unique())
)

filtered = df[
    df["category"].isin(categories) &
    df["city"].isin(cities)
]

revenue = filtered["revenue"].sum()
orders = filtered["order_id"].nunique()
units = filtered["quantity"].sum()
aov = revenue / orders if orders else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Revenue", f"₹{revenue:,.0f}")
c2.metric("Orders", f"{orders:,}")
c3.metric("Units Sold", f"{units:,}")
c4.metric("Average Order Value", f"₹{aov:,.0f}")

st.divider()

left, right = st.columns(2)

with left:
    category = (
        filtered.groupby("category", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
    )
    fig = px.bar(
        category,
        x="category",
        y="revenue",
        title="Revenue by Category",
        labels={"revenue": "Revenue", "category": "Category"}
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    monthly = (
        filtered.assign(month=filtered["date"].dt.to_period("M").astype(str))
        .groupby("month", as_index=False)["revenue"]
        .sum()
    )
    fig = px.line(
        monthly,
        x="month",
        y="revenue",
        markers=True,
        title="Monthly Revenue Trend",
        labels={"revenue": "Revenue", "month": "Month"}
    )
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)

with left:
    city = (
        filtered.groupby("city", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
    )
    fig = px.bar(
        city,
        x="city",
        y="revenue",
        title="Revenue by City",
        labels={"revenue": "Revenue", "city": "City"}
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    payment = filtered["payment_method"].value_counts().reset_index()
    payment.columns = ["payment_method", "transactions"]
    fig = px.pie(
        payment,
        names="payment_method",
        values="transactions",
        title="Payment Method Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Top Products")

products = (
    filtered.groupby("product", as_index=False)
    .agg(
        Revenue=("revenue", "sum"),
        Units=("quantity", "sum")
    )
    .sort_values("Revenue", ascending=False)
)

st.dataframe(products, use_container_width=True, hide_index=True)

st.download_button(
    "Download Filtered Data",
    filtered.to_csv(index=False).encode("utf-8"),
    "filtered_business_data.csv",
    "text/csv"
)
