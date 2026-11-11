from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.repositories.analyses import require_analysis
from app.schemas.dashboard import DashboardSummary

router = APIRouter(prefix="/analyses")

@router.get("/{analysis_id}/dashboard", response_model=DashboardSummary)
def dashboard(analysis_id: str, db: Session = Depends(get_db)):
    return require_analysis(analysis_id, db).summary
