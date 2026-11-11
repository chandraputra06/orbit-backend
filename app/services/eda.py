import numpy as np
import pandas as pd


def calculate_distribution(values, bins=10):
    numbers = pd.to_numeric(
        values, errors="coerce"
    ).dropna().astype(float)

    if numbers.empty:
        return {"stats": {}, "bins": []}

    stats = {
        "min": round(float(numbers.min()), 2),
        "p25": round(float(numbers.quantile(0.25)), 2),
        "median": round(float(numbers.median()), 2),
        "mean": round(float(numbers.mean()), 2),
        "p75": round(float(numbers.quantile(0.75)), 2),
        "p95": round(float(numbers.quantile(0.95)), 2),
        "max": round(float(numbers.max()), 2)
    }

    edges = np.unique(
        np.quantile(
            numbers,
            np.linspace(0, 1, bins + 1)
        )
    )

    if len(edges) == 1:
        return {
            "stats": stats,
            "bins": [{
                "min": float(edges[0]),
                "max": float(edges[0]),
                "count": int(len(numbers))
            }]
        }

    counts, edges = np.histogram(
        numbers, bins=edges
    )

    histogram = [
        {
            "min": round(float(edges[i]), 2),
            "max": round(float(edges[i + 1]), 2),
            "count": int(counts[i])
        }
        for i in range(len(counts))
    ]

    return {
        "stats": stats,
        "bins": histogram
    }


def build_eda(clean_df: pd.DataFrame,
              rfm: pd.DataFrame) -> dict:

    # 1. Distribusi RFM
    rfm_distributions = {
        feature: calculate_distribution(rfm[feature])
        for feature in [
            "recency", "frequency", "monetary"
        ]
    }

    # 2. Top 10 produk berdasarkan quantity
    top_products = []

    if "StockCode" in clean_df.columns:
        products = clean_df.copy()
        products["StockCode"] = (
            products["StockCode"].astype(str)
        )

        grouped = products.groupby("StockCode").agg(
            quantity=("Quantity", "sum"),
            sales=("TotalAmount", "sum")
        ).sort_values(
            "quantity", ascending=False
        ).head(10)

        top_products = [
            {
                "stock_code": str(code),
                "quantity": int(row.quantity),
                "sales": round(float(row.sales), 2)
            }
            for code, row in grouped.iterrows()
        ]

    # 3. Top 10 negara berdasarkan invoice
    top_countries = []

    if "Country" in clean_df.columns:
        grouped = clean_df.groupby(
            "Country", dropna=False
        ).agg(
            orders=("InvoiceNo", "nunique"),
            customers=("CustomerID", "nunique"),
            sales=("TotalAmount", "sum")
        ).sort_values(
            "orders", ascending=False
        ).head(10)

        top_countries = [
            {
                "country": str(country),
                "orders": int(row.orders),
                "customers": int(row.customers),
                "sales": round(float(row.sales), 2)
            }
            for country, row in grouped.iterrows()
        ]

    # 4. Jumlah invoice unik per bulan
    monthly = clean_df.groupby(
        clean_df["InvoiceDate"].dt.strftime("%Y-%m")
    )["InvoiceNo"].nunique()

    monthly_orders = [
        {
            "month": str(month),
            "orders": int(count)
        }
        for month, count in monthly.items()
    ]

    return {
        "rfm_distributions": rfm_distributions,
        "top_products_by_quantity": top_products,
        "top_countries_by_orders": top_countries,
        "monthly_orders": monthly_orders
    }
