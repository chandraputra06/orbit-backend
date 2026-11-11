import pandas as pd

def calculate_rfm(df: pd.DataFrame) -> pd.DataFrame:
    reference = df["InvoiceDate"].max() + pd.Timedelta(days=1)
    rfm = df.groupby("CustomerID").agg(
        last_purchase=("InvoiceDate", "max"),
        frequency=("InvoiceNo", "nunique"),
        monetary=("TotalAmount", "sum"),
    ).reset_index()
    rfm["recency"] = (reference - rfm["last_purchase"]).dt.days.astype(int)
    rfm["customer_id"] = rfm["CustomerID"].map(
        lambda x: str(int(x)) if isinstance(x, (int, float)) and float(x).is_integer() else str(x)
    )
    return rfm[["customer_id", "recency", "frequency", "monetary"]]
