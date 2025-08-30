import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      // Disable native modules to prevent platform-specific issues
      external: [],
      output: {
        manualChunks: undefined
      }
    },
    // Ensure we don't have platform-specific issues
    target: 'es2020',
    minify: 'esbuild'
  },
  // Add environment variable handling
  define: {
    'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV || 'production')
  }
})
