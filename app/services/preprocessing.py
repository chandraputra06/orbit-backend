import pandas as pd

REQUIRED_COLUMNS = {"InvoiceNo", "InvoiceDate", "CustomerID", "Quantity", "UnitPrice"}

def clean_transactions(raw: pd.DataFrame) -> pd.DataFrame:
    missing = REQUIRED_COLUMNS - set(raw.columns)
    if missing:
        raise ValueError(f"Kolom wajib tidak ditemukan: {', '.join(sorted(missing))}")
    df = raw.copy()
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")
    df = df.dropna(subset=["CustomerID", "InvoiceNo", "InvoiceDate", "Quantity", "UnitPrice"])
    df = df[~df["InvoiceNo"].astype(str).str.upper().str.startswith("C")]
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)].drop_duplicates().copy()
    if df.empty:
        raise ValueError("Tidak ada transaksi valid setelah cleaning")
    df["TotalAmount"] = df["Quantity"] * df["UnitPrice"]
    return df
