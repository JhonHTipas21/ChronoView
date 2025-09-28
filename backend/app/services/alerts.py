from datetime import datetime, timedelta, timezone
from math import sqrt
from typing import Tuple, Optional
from ..redis_client import redis_client

WINDOW_SECONDS = 300       # 5 minutos
ALERT_SIGMA = 2.5

def _key(metric: str) -> str:
    return f"pm:win:{metric}"

async def push_value(metric: str, ts: datetime, value: float) -> None:
    k = _key(metric)
    score = ts.timestamp()
    await redis_client.zadd(k, {str(value): score})
    # purge viejo
    min_score = (ts - timedelta(seconds=WINDOW_SECONDS)).timestamp()
    await redis_client.zremrangebyscore(k, 0, min_score)

async def stats(metric: str, now: datetime) -> Tuple[Optional[float], Optional[float], int]:
    k = _key(metric)
    min_score = (now - timedelta(seconds=WINDOW_SECONDS)).timestamp()
    vals = await redis_client.zrangebyscore(k, min_score, now.timestamp())
    xs = [float(v) for v in vals]
    n = len(xs)
    if n == 0:
        return None, None, 0
    mean = sum(xs)/n
    if n == 1:
        return mean, 0.0, n
    var = sum((x-mean)**2 for x in xs)/(n-1)
    return mean, sqrt(var), n

async def check_alert(metric: str, value: float, ts: datetime):
    await push_value(metric, ts, value)
    mean, std, n = await stats(metric, ts)
    if mean is None or std is None or n < 5:  # espera algo de ventana
        return False, 0.0
    if std == 0:
        return False, 0.0
    z = abs(value - mean) / std
    return (z >= ALERT_SIGMA), z
