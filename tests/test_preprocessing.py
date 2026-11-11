import pandas as pd
import pytest
from app.services.preprocessing import clean_transactions

def test_cleaning_removes_invalid_rows():
    df = pd.DataFrame([
        {"InvoiceNo": "1", "InvoiceDate": "2011-01-01", "CustomerID": 10, "Quantity": 2, "UnitPrice": 3},
        {"InvoiceNo": "C2", "InvoiceDate": "2011-01-01", "CustomerID": 10, "Quantity": -1, "UnitPrice": 3},
        {"InvoiceNo": "3", "InvoiceDate": "2011-01-01", "CustomerID": None, "Quantity": 1, "UnitPrice": 3},
    ])
    clean = clean_transactions(df)
    assert len(clean) == 1
    assert clean.iloc[0]["TotalAmount"] == 6

def test_missing_columns_rejected():
    with pytest.raises(ValueError):
        clean_transactions(pd.DataFrame({"InvoiceNo": [1]}))
