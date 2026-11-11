from io import BytesIO
import pandas as pd

def read_dataset(filename: str, content: bytes) -> pd.DataFrame:
    if filename.lower().endswith(".csv"):
        return pd.read_csv(BytesIO(content))
    if filename.lower().endswith(".xlsx"):
        return pd.read_excel(BytesIO(content), engine="openpyxl")
    raise ValueError("Format file harus CSV atau XLSX")
