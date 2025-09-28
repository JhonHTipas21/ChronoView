import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Proxy útil en local si quieres evitar CORS en desarrollo
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:8000'
    }
  }
})
