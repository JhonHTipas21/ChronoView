import asyncio
import random
from datetime import datetime, timezone

async def simulated_metric_stream(metric: str):
    base = 100.0 if metric == "traffic" else 50.0
    while True:
        # pequeña caminata aleatoria
        jitter = random.uniform(-3, 3)
        value = max(0, base + jitter)
        yield {"metric": metric, "value": value, "ts": datetime.now(timezone.utc).isoformat()}
        await asyncio.sleep(1)  # 1 dato/segundo
