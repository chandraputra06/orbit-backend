import pandas as pd
from app.services.preprocessing import clean_transactions
from app.services.rfm import calculate_rfm

def test_frequency_counts_invoices_not_lines():
    raw = pd.DataFrame([
        {"InvoiceNo": "1", "InvoiceDate": "2011-01-01", "CustomerID": 7, "Quantity": 2, "UnitPrice": 3, "StockCode": "a"},
        {"InvoiceNo": "1", "InvoiceDate": "2011-01-01", "CustomerID": 7, "Quantity": 1, "UnitPrice": 4, "StockCode": "b"},
        {"InvoiceNo": "2", "InvoiceDate": "2011-01-03", "CustomerID": 7, "Quantity": 1, "UnitPrice": 2, "StockCode": "c"},
    ])
    rfm = calculate_rfm(clean_transactions(raw))
    assert rfm.iloc[0]["frequency"] == 2
    assert rfm.iloc[0]["monetary"] == 12
    assert rfm.iloc[0]["recency"] == 1
