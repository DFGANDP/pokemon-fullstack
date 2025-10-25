// vite.config.ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)), // ← kluczowe
    },
  },
  server: {
    proxy: {
      '/api': { target: 'https://pokemon-backend-api-gkghfqc8h4f4aua6.polandcentral-01.azurewebsites.net', changeOrigin: true },
    },
  },
})
