import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import type { UserConfig, ConfigEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'

export default defineConfig(({ mode }: ConfigEnv): UserConfig => {
  const isProduction = mode === 'production'

  return {
    plugins: [
      vue(),
      vueJsx(),
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      },
    },
    build: {
      target: 'es2020',
      sourcemap: !isProduction,
      rollupOptions: {
        output: {
          manualChunks(id) {
            if (id.includes('node_modules/vue') || id.includes('node_modules/vue-router')) {
              return 'vue'
            }
            if (id.includes('node_modules/axios')) {
              return 'axios'
            }
          },
        },
      },
      chunkSizeWarningLimit: 600,
    },
  }
})
