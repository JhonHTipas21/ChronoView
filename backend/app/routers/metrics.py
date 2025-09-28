from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from ..schemas import MetricIn
from ..db import SessionLocal

router = APIRouter(prefix="/metrics", tags=["metrics"])

async def get_db():
    async with SessionLocal() as s:
        yield s

@router.post("", status_code=201)
async def ingest_metric(payload: MetricIn, db: AsyncSession = Depends(get_db)):
    q = text("""
        INSERT INTO metrics (metric, value, ts)
        VALUES (:metric, :value, COALESCE(:ts, NOW()))
    """)
    await db.execute(q, {"metric": payload.metric, "value": payload.value, "ts": payload.ts})
    await db.commit()
    return {"ok": True}
