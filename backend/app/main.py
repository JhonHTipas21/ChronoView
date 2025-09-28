from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
import json

from .config import settings
from .routers import health, metrics, export as export_router, snapshots
from .services.streamer import simulated_metric_stream
from .services.alerts import check_alert

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(metrics.router)
app.include_router(export_router.router)
app.include_router(snapshots.router)

@app.websocket("/ws/stream")
async def ws_stream(websocket: WebSocket, metric: str = "traffic"):
    await websocket.accept()
    try:
        async for item in simulated_metric_stream(metric):
            ts = datetime.now(timezone.utc)
            value = float(item["value"])
            alert, z = await check_alert(metric, value, ts)
            msg = {
                "type": "metric",
                "data": item,
                "alert": alert,
                "zscore": z
            }
            await websocket.send_text(json.dumps(msg))
    except WebSocketDisconnect:
        pass
