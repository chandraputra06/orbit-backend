from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import CustomerRFM
from app.db.repositories.analyses import require_analysis

router = APIRouter(prefix="/analyses")

@router.get("/{analysis_id}/rfm")
def list_rfm(analysis_id: str, limit: int = Query(100, ge=1, le=500),
             offset: int = Query(0, ge=0), db: Session = Depends(get_db)):
    require_analysis(analysis_id, db)
    total = db.scalar(select(func.count()).select_from(CustomerRFM).where(CustomerRFM.analysis_id == analysis_id))
    rows = db.scalars(select(CustomerRFM).where(CustomerRFM.analysis_id == analysis_id)
                      .order_by(CustomerRFM.id).offset(offset).limit(limit)).all()
    return {"total": total, "limit": limit, "offset": offset,
            "items": [{"customer_id": r.customer_id, "recency": r.recency,
                       "frequency": r.frequency, "monetary": round(r.monetary, 2)} for r in rows]}

@router.get("/{analysis_id}/customers/{customer_id}")
def customer_detail(analysis_id: str, customer_id: str, db: Session = Depends(get_db)):
    require_analysis(analysis_id, db)
    record = db.scalar(select(CustomerRFM).where(CustomerRFM.analysis_id == analysis_id,
                                                  CustomerRFM.customer_id == customer_id))
    if record is None:
        raise HTTPException(status_code=404, detail="Customer tidak ditemukan")
    return {"customer_id": record.customer_id, "recency": record.recency,
            "frequency": record.frequency, "monetary": round(record.monetary, 2),
            "segment": None, "note": "Fuzzy Mamdani belum dikonfigurasi"}
