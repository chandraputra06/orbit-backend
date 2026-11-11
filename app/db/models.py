from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base

class Analysis(Base):
    __tablename__ = "analyses"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    filename: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    raw_rows: Mapped[int] = mapped_column(Integer)
    clean_rows: Mapped[int] = mapped_column(Integer)
    summary: Mapped[dict] = mapped_column(JSON)

class CustomerRFM(Base):
    __tablename__ = "customer_rfm"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    analysis_id: Mapped[str] = mapped_column(ForeignKey("analyses.id", ondelete="CASCADE"), index=True)
    customer_id: Mapped[str] = mapped_column(String(100), index=True)
    recency: Mapped[int] = mapped_column(Integer)
    frequency: Mapped[int] = mapped_column(Integer)
    monetary: Mapped[float] = mapped_column(Float)
