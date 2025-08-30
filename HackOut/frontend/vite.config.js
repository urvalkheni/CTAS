import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      // Disable native modules and platform-specific optimizations
      external: [],
      output: {
        manualChunks: undefined,
        // Ensure consistent output across platforms
        format: 'es',
        entryFileNames: '[name].[hash].js',
        chunkFileNames: '[name].[hash].js',
        assetFileNames: '[name].[hash].[ext]'
      },
      // Disable platform-specific optimizations
      treeshake: {
        moduleSideEffects: false
      }
    },
    // Use esbuild for better compatibility
    target: 'es2015',
    minify: 'esbuild',
    // Disable source maps for production
    sourcemap: false,
    // Ensure consistent build output
    outDir: 'dist',
    assetsDir: 'assets'
  },
  // Add environment variable handling
  define: {
    'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV || 'production')
  },
  // Optimize for production builds
  optimizeDeps: {
    include: ['react', 'react-dom']
  }
})
