from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.repositories.analyses import require_analysis

router = APIRouter(prefix="/analyses")

@router.get("/{analysis_id}/insights")
def insights(analysis_id: str, db: Session = Depends(get_db)):
    require_analysis(analysis_id, db)
    return {"status": "not_configured", "items": [],
            "message": "Rekomendasi tersedia setelah aturan segmentasi Mamdani selesai"}
