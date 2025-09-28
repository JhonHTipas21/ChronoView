import React from 'react'

export default function SingleStat({ label, value, alert }: { label: string; value: number; alert?: boolean }) {
  return (
    <div style={{
      padding: 16,
      borderRadius: 12,
      border: '1px solid #eee',
      background: alert ? '#ffecec' : '#f9f9f9'
    }}>
      <div style={{ fontSize: 12, color: '#888' }}>{label}</div>
      <div style={{ fontSize: 32, fontWeight: 700 }}>{value.toFixed(2)}</div>
      {alert && <div style={{ color: '#b00020', fontSize: 12, marginTop: 4 }}>⚠️ Alerta por desviación</div>}
    </div>
  )
}
