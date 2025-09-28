# ⚡️ ChronoView — Pulsar Metrics
**Dashboard de Análisis en Tiempo Real** (FastAPI + WebSockets + Redis + Supabase + React/Recharts)

[![Made with FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![WebSockets](https://img.shields.io/badge/WebSockets-WS-02569B?logo=websocket&logoColor=white)](#)
[![Redis](https://img.shields.io/badge/Redis-Cache%20%2F%20Stream-DC382D?logo=redis&logoColor=white)](https://redis.io/)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E?logo=supabase&logoColor=white)](https://supabase.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-5-646CFF?logo=vite&logoColor=white)](https://vitejs.dev/)
[![Recharts](https://img.shields.io/badge/Recharts-2-0088CC)](https://recharts.org/en-US)

> **Pulsar Metrics** permite visualizar métricas en vivo (IoT, tráfico de apps, finanzas) con notificaciones inteligentes por desviación, snapshots compartibles y exportación a CSV, cuidando consumo y latencia.

---

## 🧭 Índice
- [Arquitectura (gráfico)](#arquitectura-gráfico)
- [Tecnologías (tabla + gráfico)](#tecnologías-tabla--gráfico)
- [Características clave](#características-clave)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Instalación y ejecución (Dev)](#instalación-y-ejecución-dev)
- [Variables de entorno](#variables-de-entorno)
- [API y WebSocket](#api-y-websocket)
- [Smart Alerts (cómo funciona)](#smart-alerts-cómo-funciona)
- [Snapshots y Export a CSV](#snapshots-y-export-a-csv)
- [Despliegue](#despliegue)
- [FAQ rápida](#faq-rápida)
- [Licencia](#licencia)

---

## Arquitectura (gráfico)
```mermaid
flowchart LR
  subgraph Frontend [Frontend (Vite/React)]
    UI[Dashboard<br/>Recharts] -- WS: metric --> WSClient
    UI -- REST --> RESTClient
  end

  subgraph Backend [Backend (FastAPI)]
    WSClient[[/ws/stream]] -- push --> Alerts[Smart Alerts<br/>2.5σ / 5min / Redis]
    RESTClient[[/metrics, /snapshots, /export]]
    DB[(Supabase<br/>PostgreSQL)]
    Cache[(Redis)]
  end

  RESTClient -- INSERT/SELECT --> DB
  Alerts <-- window/values --> Cache
  Alerts -- flag+zscore --> WSClient




Tecnologías (tabla + gráfico)

Tabla del stack
| Componente     | Tecnología                | Motivo                             |
| -------------- | ------------------------- | ---------------------------------- |
| Frontend       | **React 18 + Vite**       | DX rápida, módulos ES, HMR         |
| Gráficas       | **Recharts**              | Ligero, intuitivo, SSR friendly    |
| Backend API/WS | **FastAPI**               | Alto rendimiento, tipado Pydantic  |
| Realtime       | **WebSockets nativos**    | Push 1s sin polling                |
| Persistencia   | **PostgreSQL (Supabase)** | SQL, JSONB, índices por métrica/ts |
| Cache/ventanas | **Redis**                 | Sorted sets para rolling windows   |
| Export         | CSV                       | Compatible con Excel/Sheets        |

Características clave

⚡ Streaming 1s por WebSocket (métricas simuladas o reales).

🧠 Smart Alerts: alerta si |x-μ|/σ ≥ 2.5 en ventana móvil de 5 min (Redis).

📸 Snapshots del estado del dashboard (UUID compartible).

📤 Export CSV listo para Excel/Google Sheets.

🧩 Módulos desacoplados: streamer, alerts, snapshots.

🔐 CORS configurable y envs separados por entorno.

ChronoView/
├─ backend/
│  ├─ app/
│  │  ├─ main.py                # Enrutado, CORS, WS
│  │  ├─ config.py              # Settings (.env)
│  │  ├─ db.py                  # Engine SQLAlchemy (asyncpg + TLS)
│  │  ├─ redis_client.py        # Cliente Redis (async)
│  │  ├─ schemas.py             # Pydantic
│  │  ├─ services/
│  │  │  ├─ streamer.py         # Simulador de métricas
│  │  │  ├─ alerts.py           # 2.5σ/5min con Redis
│  │  │  └─ snapshots.py        # Insert/Select snapshots
│  │  └─ routers/
│  │     ├─ health.py
│  │     ├─ metrics.py          # POST /metrics
│  │     ├─ export.py           # GET /export/csv
│  │     └─ snapshots.py        # POST/GET /snapshots
│  ├─ requirements.txt
│  └─ .env.example
└─ frontend/
   ├─ src/
   │  ├─ main.tsx, App.tsx
   │  ├─ types.ts
   │  ├─ vite-env.d.ts
   │  ├─ lib/ws.ts              # Cliente WS
   │  └─ components/
   │     ├─ Dashboard.tsx
   │     └─ charts/{LineMetric,BarMetric,SingleStat}.tsx
   ├─ vite.config.ts
   ├─ package.json
   └─ .env.example

Instalación y ejecución (Dev)
1) Backend

# Requisitos: Python 3.11+, Redis en :6379, Supabase listo
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

# Copia y ajusta tus envs
copy .env.example .env
# Edita .env con tus valores

# Arranca
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# Health: http://localhost:8000/health
2) Frontend
cd frontend
npm install
copy .env.example .env
# Edita .env (VITE_WS_URL / VITE_API_URL) si cambiaste puertos

npm run dev
# http://localhost:5173

Variables de entorno

Backend (backend/.env)
| Clave          | Ejemplo                                                                              | Descripción                         |
| -------------- | ------------------------------------------------------------------------------------ | ----------------------------------- |
| `APP_PORT`     | `8000`                                                                               | Puerto FastAPI                      |
| `CORS_ORIGINS` | `http://localhost:5173`                                                              | Comas para múltiples orígenes       |
| `DATABASE_URL` | `postgresql+asyncpg://postgres:***@db.xxx.supabase.co:5432/postgres?sslmode=require` | Supabase con `+asyncpg` y TLS       |
| `REDIS_URL`    | `redis://localhost:6379/0`                                                           | Cache/ventana para alerts           |
| `SECRET_KEY`   | `change_me`                                                                          | Clave para futuras features seguras |

Frontend (frontend/.env)

| Clave          | Ejemplo                                        |
| -------------- | ---------------------------------------------- |
| `VITE_WS_URL`  | `ws://localhost:8000/ws/stream?metric=traffic` |
| `VITE_API_URL` | `http://localhost:8000`                        |


API y WebSocket

REST (principales)

| Método | Ruta                                 | Descripción                                   |
| ------ | ------------------------------------ | --------------------------------------------- |
| `GET`  | `/health`                            | Liveness                                      |
| `POST` | `/metrics`                           | Inserta dato histórico `{metric, value, ts?}` |
| `GET`  | `/export/csv?metric=traffic&hours=1` | CSV para hojas de cálculo                     |
| `POST` | `/snapshots`                         | Guarda snapshot `{ state: JSON }`             |
| `GET`  | `/snapshots/{id}`                    | Recupera snapshot por UUID                    |

WebSocket

Ruta: /ws/stream?metric=<name>

Periodo: ~1s

Mensaje:

{
  "type": "metric",
  "data": { "metric": "traffic", "value": 101.2, "ts": "2025-09-27T02:33:11Z" },
  "alert": true,
  "zscore": 3.01
}
Secuencia (gráfico)

sequenceDiagram
  autonumber
  participant UI as React (Dashboard)
  participant WS as FastAPI /ws/stream
  participant R as Redis (ventana)
  UI->>WS: Open socket (metric=traffic)
  loop cada 1s
    WS->>WS: Simula/recibe valor
    WS->>R: push_value(metric, ts, value)
    R-->>WS: mean, std, n
    WS->>UI: { value, alert, zscore }
    UI->>UI: Actualiza Recharts + SingleStat
  end

Smart Alerts (cómo funciona)

Ventana deslizante de 5 min por métrica (Redis ZSET con timestamp como score).

Cálculo incremental de μ y σ de los últimos 5 minutos.

Dispara alerta si |x - μ| / σ ≥ 2.5 y n ≥ 5.

Esto se implementa en backend/app/services/alerts.py.

Snapshots y Export a CSV

Snapshots: guarda el estado del dashboard (selectedMetric, timeRangeHours, layout) como JSONB en snapshots. Devuelve UUID compartible.

CSV: GET /export/csv?metric=X&hours=H devuelve metric,value,ts ordenado por tiempo.
