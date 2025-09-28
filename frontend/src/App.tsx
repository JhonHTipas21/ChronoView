import React from 'react'
import Dashboard from './components/Dashboard'

export default function App() {
  return (
    <div style={{ padding: 16, fontFamily: 'ui-sans-serif, system-ui' }}>
      <h1>Pulsar Metrics</h1>
      <p style={{ color: '#666' }}>Dashboard de análisis en tiempo real</p>
      <Dashboard />
    </div>
  )
}
