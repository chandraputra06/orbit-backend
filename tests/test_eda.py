import pandas as pd

from app.services.preprocessing import clean_transactions
from app.services.rfm import calculate_rfm
from app.services.eda import build_eda


def test_eda():
    raw = pd.DataFrame([
        {
            "InvoiceNo": "1",
            "InvoiceDate": "2011-01-01",
            "CustomerID": 7,
            "Quantity": 2,
            "UnitPrice": 3,
            "StockCode": "A",
            "Country": "UK"
        },
        {
            "InvoiceNo": "1",
            "InvoiceDate": "2011-01-01",
            "CustomerID": 7,
            "Quantity": 1,
            "UnitPrice": 4,
            "StockCode": "B",
            "Country": "UK"
        },
        {
            "InvoiceNo": "2",
            "InvoiceDate": "2011-01-03",
            "CustomerID": 8,
            "Quantity": 3,
            "UnitPrice": 2,
            "StockCode": "A",
            "Country": "FR"
        }
    ])

    clean = clean_transactions(raw)
    rfm = calculate_rfm(clean)
    eda = build_eda(clean, rfm)

    assert len(rfm) == 2

    assert sum(
        b["count"]
        for b in eda["rfm_distributions"]["recency"]["bins"]
    ) == 2

    assert eda["top_products_by_quantity"][0]["stock_code"] == "A"
    assert eda["top_products_by_quantity"][0]["quantity"] == 5

    assert eda["monthly_orders"] == [
        {"month": "2011-01", "orders": 2}
    ]
