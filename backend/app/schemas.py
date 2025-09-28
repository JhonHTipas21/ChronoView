from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from datetime import datetime
from uuid import UUID

class MetricIn(BaseModel):
    metric: str
    value: float
    ts: Optional[datetime] = None

class MetricOut(MetricIn):
    id: int

class SnapshotCreate(BaseModel):
    state: Dict[str, Any]

class SnapshotOut(BaseModel):
    id: UUID
    created_at: datetime

class AlertOut(BaseModel):
    metric: str
    value: float
    ts: datetime
    zscore: float
    threshold: float
    alert: bool
