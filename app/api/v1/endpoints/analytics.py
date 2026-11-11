from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Analysis
from app.db.repositories.analyses import require_analysis
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/analyses")

@router.get("")
def list_analyses(db: Session = Depends(get_db)):
    rows = db.scalars(select(Analysis).order_by(Analysis.created_at.desc())).all()
    return [{"analysis_id": a.id, "filename": a.filename, "created_at": a.created_at.isoformat()} for a in rows]

@router.get("/{analysis_id}/overview")
def overview(analysis_id: str, db: Session = Depends(get_db)):
    a = require_analysis(analysis_id, db)
    return {"analysis_id": a.id, "filename": a.filename, "raw_rows": a.raw_rows,
            "clean_rows": a.clean_rows, "removed_rows": a.raw_rows - a.clean_rows,
            "date_start": a.summary["date_start"], "date_end": a.summary["date_end"]}

@router.get("/{analysis_id}/eda")
def get_eda(
    analysis_id: str,
    db: Session = Depends(get_db)
):
    analysis = require_analysis(
        analysis_id, db
    )

    eda = analysis.summary.get("eda")

    if eda is None:
        raise HTTPException(
            status_code=409,
            detail=(
                "Hasil EDA belum tersedia. "
                "Silakan upload ulang dataset."
            )
        )

    return {
        "analysis_id": analysis.id,
        **eda
    }
