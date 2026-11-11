from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.repositories.analyses import require_analysis

router = APIRouter(prefix="/analyses")

@router.get("/{analysis_id}/segments")
def segments(analysis_id: str, db: Session = Depends(get_db)):
    require_analysis(analysis_id, db)
    return {"status": "not_configured",
            "message": "Membership function dan rule base Mamdani belum ditetapkan",
            "items": []}
