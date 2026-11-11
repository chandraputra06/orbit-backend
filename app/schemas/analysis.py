from pydantic import BaseModel

class AnalysisCreated(BaseModel):
    analysis_id: str
    status: str
    raw_rows: int
    clean_rows: int
    total_customers: int
