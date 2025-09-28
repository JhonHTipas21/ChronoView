import React, { useEffect, useMemo, useRef, useState } from 'react'
import { connectWS } from '../lib/ws'
import LineMetric from './charts/LineMetric'
import BarMetric from './charts/BarMetric'
import SingleStat from './charts/SingleStat'
import type { StreamMessage, SnapshotState } from '../types'

const WS_URL = import.meta.env.VITE_WS_URL as string
const API_URL = import.meta.env.VITE_API_URL as string

export default function Dashboard() {
  const [selectedMetric, setSelectedMetric] = useState('traffic')
  const [points, setPoints] = useState<Array<{ ts: string; value: number }>>([])
  const [last, setLast] = useState<number>(0)
  // ⬇️ renombrado para no sombrear window.alert()
  const [hasAlert, setHasAlert] = useState<boolean>(false)
  const wsRef = useRef<WebSocket | null>(null)

  // histograma simple para demo de barras
  const bars = useMemo(() => {
    const buckets: Record<string, number> = { low: 0, mid: 0, high: 0 }
    for (const p of points.slice(-60)) {
      if (p.value < 50) buckets.low++
      else if (p.value < 100) buckets.mid++
      else buckets.high++
    }
    return [
      { bucket: 'low', value: buckets.low },
      { bucket: 'mid', value: buckets.mid },
      { bucket: 'high', value: buckets.high },
    ]
  }, [points])

  useEffect(() => {
    // cerrar socket anterior si cambias métrica
    wsRef.current?.close()

    // construir URL de forma robusta (si falla, usa replace como fallback)
    const url = (() => {
      try {
        const u = new URL(WS_URL)
        u.searchParams.set('metric', selectedMetric)
        return u.toString()
      } catch {
        return WS_URL.replace(/metric=([^&]+)/, `metric=${selectedMetric}`)
      }
    })()

    const ws = connectWS(url, (msg: StreamMessage) => {
      if (msg.type === 'metric') {
        const v = msg.data.value
        setLast(v)
        setHasAlert(!!msg.alert)
        setPoints(prev => [
          ...prev.slice(-299),
          { ts: new Date(msg.data.ts).toLocaleTimeString(), value: v }
        ])
      }
    })

    wsRef.current = ws
    return () => ws.close()
  }, [selectedMetric])

  async function exportCsv(): Promise<void> {
    const q = new URLSearchParams({ metric: selectedMetric, hours: String(1) })
    window.open(`${API_URL}/export/csv?${q.toString()}`, '_blank')
  }

  async function saveSnapshot(): Promise<void> {
    const payload: SnapshotState = {
      selectedMetric,
      timeRangeHours: 1,
      layout: 'default'
    }
    const res = await fetch(`${API_URL}/snapshots`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ state: payload })
    })
    const json = await res.json()
    if (json.id) {
      const url = `${window.location.origin}/snapshot/${json.id}`
      // usar window.alert explícitamente
      window.alert(`Snapshot guardado.\nID: ${json.id}\nGuarda esta URL: ${url}`)
    }
  }

  return (
    <div style={{ display: 'grid', gap: 16 }}>
      <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
        <label>Métrica:</label>
        <select value={selectedMetric} onChange={e => setSelectedMetric(e.target.value)}>
          <option value="traffic">traffic</option>
          <option value="cpu">cpu</option>
          <option value="orders">orders</option>
        </select>

        <button onClick={saveSnapshot}>💾 Guardar snapshot</button>
        <button onClick={exportCsv}>⬇️ Exportar CSV</button>
      </div>

      <SingleStat label={`Valor actual (${selectedMetric})`} value={last || 0} alert={hasAlert} />

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
        <div>
          <h3>Evolución (últimos ~300s)</h3>
          <LineMetric data={points} />
        </div>
        <div>
          <h3>Distribución reciente</h3>
          <BarMetric data={bars} />
        </div>
      </div>
    </div>
  )
}
