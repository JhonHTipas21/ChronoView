from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from io import StringIO
from ..db import SessionLocal

router = APIRouter(prefix="/export", tags=["export"])

async def get_db():
    async with SessionLocal() as s:
        yield s

@router.get("/csv")
async def export_csv(metric: str, hours: int = 1, db: AsyncSession = Depends(get_db)):
    q = text("""
        SELECT metric, value, ts
        FROM metrics
        WHERE metric = :m AND ts >= NOW() - (:h || ' hours')::interval
        ORDER BY ts ASC
    """)
    res = await db.execute(q, {"m": metric, "h": hours})
    rows = res.fetchall()
    buff = StringIO()
    buff.write("metric,value,ts\n")
    for r in rows:
        buff.write(f"{r[0]},{r[1]},{r[2].isoformat()}\n")
    buff.seek(0)
    return StreamingResponse(buff, media_type="text/csv", headers={
        "Content-Disposition": f'attachment; filename="{metric}_{hours}h.csv"'
    })
