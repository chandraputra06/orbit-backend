from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models import Analysis

def require_analysis(analysis_id: str, db: Session) -> Analysis:
    analysis = db.get(Analysis, analysis_id)
    if analysis is None:
        raise HTTPException(status_code=404, detail="Analisis tidak ditemukan")
    return analysis
