from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.database import get_db
from app.db.models import Analysis, CustomerRFM
from app.schemas.analysis import AnalysisCreated
from app.utils.file_handler import read_dataset
from app.services.preprocessing import clean_transactions
from app.services.rfm import calculate_rfm
from app.services.dashboard import build_dashboard
from app.services.eda import build_eda

router = APIRouter(prefix="/analyses")

@router.post("", status_code=201, response_model=AnalysisCreated)
def upload_analysis(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename or not file.filename.lower().endswith((".csv", ".xlsx")):
        raise HTTPException(status_code=400, detail="Format file harus CSV atau XLSX")
    content = file.file.read(settings.max_upload_mb * 1024 * 1024 + 1)
    if len(content) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File terlalu besar")
    try:
        raw = read_dataset(file.filename, content)
        clean = clean_transactions(raw)
        rfm = calculate_rfm(clean)
        summary = build_dashboard(clean, rfm)
        summary["eda"] = build_eda(clean, rfm)
    except (ValueError, KeyError, TypeError, UnicodeError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=422, detail="File gagal dibaca atau diproses") from exc

    record = Analysis(filename=file.filename[:255], raw_rows=len(raw), clean_rows=len(clean), summary=summary)
    try:
        db.add(record)
        db.flush()
        db.add_all([
            CustomerRFM(analysis_id=record.id, customer_id=row.customer_id,
                        recency=int(row.recency), frequency=int(row.frequency),
                        monetary=float(row.monetary))
            for row in rfm.itertuples(index=False)
        ])
        db.commit()
    except Exception:
        db.rollback()
        raise
    return AnalysisCreated(analysis_id=record.id, status="completed", raw_rows=len(raw),
                           clean_rows=len(clean), total_customers=len(rfm))
