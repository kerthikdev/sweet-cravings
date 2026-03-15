import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  // Load env vars from .env / .env.production etc.
  // The third argument '' means load ALL vars (not just VITE_-prefixed ones)
  // so we can read VITE_API_GATEWAY_URL and VITE_DEV_PORT in config itself.
  const env = loadEnv(mode, process.cwd(), '')

  const apiGatewayUrl = env.VITE_API_GATEWAY_URL || 'http://localhost:5050'
  const devPort       = parseInt(env.VITE_DEV_PORT || '5173', 10)

  return {
    plugins: [react()],
    server: {
      port: devPort,
      proxy: {
        // All /api/* requests are forwarded to the api_gateway.
        // The target URL comes from VITE_API_GATEWAY_URL in frontend-react/.env
        // Eliminates CORS issues entirely in local development.
        '/api': {
          target:       apiGatewayUrl,
          changeOrigin: true,
        },
      },
    },
  }
})
