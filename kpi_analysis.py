def calculate_kpis(df):
    revenue = (df["quantity"] * df["unit_price"]).sum()
    orders = df["order_id"].nunique()
    units = df["quantity"].sum()

    return {
        "revenue": revenue,
        "orders": orders,
        "units": units,
        "average_order_value": revenue / orders if orders else 0
    }

def category_performance(df):
    data = df.copy()
    data["revenue"] = data["quantity"] * data["unit_price"]

    return (
        data.groupby("category", as_index=False)
        .agg(
            Revenue=("revenue", "sum"),
            Units=("quantity", "sum"),
            Orders=("order_id", "nunique")
        )
        .sort_values("Revenue", ascending=False)
    )

def product_performance(df):
    data = df.copy()
    data["revenue"] = data["quantity"] * data["unit_price"]

    return (
        data.groupby("product", as_index=False)
        .agg(
            Revenue=("revenue", "sum"),
            Units=("quantity", "sum")
        )
        .sort_values("Revenue", ascending=False)
    )
