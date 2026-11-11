import pandas as pd

def build_dashboard(df: pd.DataFrame, rfm: pd.DataFrame) -> dict:
    total_orders = int(df["InvoiceNo"].nunique())
    total_sales = float(df["TotalAmount"].sum())
    monthly = df.groupby(df["InvoiceDate"].dt.strftime("%Y-%m"))["TotalAmount"].sum()
    return {
        "total_customers": int(len(rfm)),
        "total_orders": total_orders,
        "total_sales": round(total_sales, 2),
        "average_order_value": round(total_sales / total_orders, 2),
        "repeat_purchase_rate": round(float((rfm["frequency"] > 1).mean() * 100), 2),
        "average_recency": round(float(rfm["recency"].mean()), 2),
        "date_start": df["InvoiceDate"].min().isoformat(),
        "date_end": df["InvoiceDate"].max().isoformat(),
        "monthly_sales": [{"month": str(k), "sales": round(float(v), 2)} for k, v in monthly.items()],
    }
