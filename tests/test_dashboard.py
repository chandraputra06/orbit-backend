import pandas as pd
from app.services.preprocessing import clean_transactions
from app.services.rfm import calculate_rfm
from app.services.dashboard import build_dashboard

def test_dashboard_aggregation():
    raw = pd.DataFrame([
        {"InvoiceNo": "1", "InvoiceDate": "2011-01-01", "CustomerID": 1, "Quantity": 2, "UnitPrice": 3},
        {"InvoiceNo": "2", "InvoiceDate": "2011-01-02", "CustomerID": 1, "Quantity": 1, "UnitPrice": 4},
    ])
    clean = clean_transactions(raw)
    summary = build_dashboard(clean, calculate_rfm(clean))
    assert summary["total_orders"] == 2
    assert summary["total_sales"] == 10
    assert summary["repeat_purchase_rate"] == 100
