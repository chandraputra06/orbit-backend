from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.database import Base, engine
from app.db import models  # noqa: F401 -- register database tables
from app.api.v1.router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)  # Untuk starter; gunakan Alembic saat schema berkembang
    yield

app = FastAPI(title="ORBIT Backend API", version="0.2.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.allowed_origins,
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(api_router, prefix="/api/v1")
# Pertahankan URL health lama untuk pengecekan kompatibilitas starter.
@app.get("/health", tags=["Health"])
def legacy_health():
    return {"status": "ok", "service": "orbit-backend"}
