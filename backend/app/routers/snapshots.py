from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import SessionLocal
from ..schemas import SnapshotCreate, SnapshotOut
from ..services.snapshots import create_snapshot, get_snapshot

router = APIRouter(prefix="/snapshots", tags=["snapshots"])

async def get_db():
    async with SessionLocal() as s:
        yield s

@router.post("", response_model=SnapshotOut, status_code=201)
async def save_snapshot(payload: SnapshotCreate, db: AsyncSession = Depends(get_db)):
    row = await create_snapshot(db, payload.state)
    return SnapshotOut(id=row["id"], created_at=row["created_at"])

@router.get("/{sid}")
async def read_snapshot(sid: str, db: AsyncSession = Depends(get_db)):
    row = await get_snapshot(db, sid)
    if not row:
        raise HTTPException(status_code=404, detail="Snapshot not found")
    return row
