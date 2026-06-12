import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react' // или @vitejs/config-react

export default defineConfig({
  plugins: [react()],
  server: {
    watch: {
      usePolling: true, // Наш рабочий поллинг для Windows
    },
    host: true,
    port: 5173,
    // Вот она, магия прокси:
    proxy: {
      '/api': {
        target: 'http://web:8000', // Имя сервиса бэкенда из твоего docker-compose
        changeOrigin: true,
        secure: false,
      }
    }
  }
})