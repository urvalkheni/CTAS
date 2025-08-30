#!/usr/bin/env node

import { execSync } from 'child_process';
import { rmSync, existsSync } from 'fs';
import { join } from 'path';

console.log('🔧 Starting Vercel-compatible build process...');

try {
  // Clean up problematic Rollup native modules
  const rollupPath = join(process.cwd(), 'node_modules', '@rollup');
  if (existsSync(rollupPath)) {
    console.log('🧹 Cleaning up Rollup native modules...');
    rmSync(rollupPath, { recursive: true, force: true });
  }

  // Clean up any other platform-specific modules
  const nativeModules = [
    join(process.cwd(), 'node_modules', '@rollup'),
    join(process.cwd(), 'node_modules', 'rollup', 'dist', 'native.js')
  ];

  nativeModules.forEach(path => {
    if (existsSync(path)) {
      console.log(`🧹 Removing: ${path}`);
      rmSync(path, { recursive: true, force: true });
    }
  });

  console.log('✅ Cleanup completed, starting Vite build...');

  // Run the actual Vite build
  execSync('npx vite build', { 
    stdio: 'inherit',
    env: {
      ...process.env,
      ROLLUP_SKIP_NATIVE: 'true',
      NODE_OPTIONS: '--no-experimental-fetch'
    }
  });

  console.log('✅ Build completed successfully!');

} catch (error) {
  console.error('❌ Build failed:', error.message);
  process.exit(1);
}
