import pandas as pd

def load_data(filename):
    df = pd.read_csv(filename)

    required = {
        "order_id", "date", "city", "product",
        "category", "quantity", "unit_price", "payment_method"
    }

    missing = required - set(df.columns)

    if missing:
        raise ValueError(f"Missing columns: {', '.join(sorted(missing))}")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

    df = df.dropna(subset=["date", "quantity", "unit_price"])
    df = df[df["quantity"] > 0]
    df = df[df["unit_price"] >= 0]

    return df
