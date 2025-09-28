from typing import Any, Dict
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

async def create_snapshot(db: AsyncSession, state: Dict[str, Any]):
    q = text("INSERT INTO snapshots (state_json) VALUES (:state) RETURNING id, created_at")
    res = await db.execute(q, {"state": state})
    row = res.first()
    await db.commit()
    return {"id": row[0], "created_at": row[1]}

async def get_snapshot(db: AsyncSession, sid: str):
    q = text("SELECT id, state_json, created_at FROM snapshots WHERE id = :sid")
    res = await db.execute(q, {"sid": sid})
    row = res.first()
    if not row: return None
    return {"id": row[0], "state": row[1], "created_at": row[2]}
