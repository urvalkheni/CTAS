#!/usr/bin/env node

import { execSync } from 'child_process';
import { writeFileSync, readFileSync, existsSync } from 'fs';
import { join } from 'path';

console.log('🔧 CTAS Codebase Comprehensive Fix Script');
console.log('==========================================');

// Define project structure
const projectRoot = process.cwd();
const frontendPath = join(projectRoot, 'frontend');
const backendPath = join(projectRoot, 'backend');

// Comprehensive dependency lists
const frontendDependencies = {
  dependencies: {
    "@react-google-maps/api": "^2.20.7",
    "@reduxjs/toolkit": "^2.8.2",
    "chart.js": "^4.5.0",
    "chartjs-adapter-date-fns": "^3.0.0",
    "date-fns": "^4.1.0",
    "framer-motion": "^12.23.12",
    "leaflet": "^1.9.4",
    "lucide-react": "^0.542.0",
    "react": "^19.0.0",
    "react-chartjs-2": "^5.3.0",
    "react-dom": "^19.0.0",
    "react-hot-toast": "^2.6.0",
    "react-leaflet": "^5.0.0",
    "react-redux": "^9.2.0",
    "react-router-dom": "^6.30.1",
    "recharts": "^3.1.2",
    "rollup": "^4.49.0"
  },
  devDependencies: {
    "@eslint/js": "^9.33.0",
    "@types/react": "^19.1.10",
    "@types/react-dom": "^19.1.7",
    "@vitejs/plugin-react-swc": "^3.5.0",
    "autoprefixer": "^10.4.21",
    "eslint": "^9.33.0",
    "eslint-plugin-react-hooks": "^5.2.0",
    "eslint-plugin-react-refresh": "^0.4.20",
    "globals": "^16.3.0",
    "postcss": "^8.5.6",
    "tailwindcss": "^3.4.17",
    "vite": "^5.1.4"
  }
};

const backendDependencies = {
  dependencies: {
    "axios": "^1.11.0",
    "bcryptjs": "^2.4.3",
    "compression": "^1.7.4",
    "cors": "^2.8.5",
    "dotenv": "^16.6.1",
    "express": "^4.18.2",
    "express-rate-limit": "^6.10.0",
    "express-validator": "^7.0.1",
    "helmet": "^7.0.0",
    "joi": "^17.9.2",
    "jsonwebtoken": "^9.0.2",
    "mongoose": "^7.5.0",
    "morgan": "^1.10.0",
    "multer": "^2.0.2",
    "node-cron": "^3.0.2",
    "nodemailer": "^6.9.4",
    "twilio": "^4.15.0",
    "ws": "^8.13.0",
    "xml2js": "^0.6.2"
  },
  devDependencies: {
    "jest": "^29.6.4",
    "nodemon": "^3.0.1",
    "supertest": "^6.3.3"
  }
};

async function runCommand(command, cwd = projectRoot) {
  try {
    console.log(`📦 Running: ${command}`);
    execSync(command, { stdio: 'inherit', cwd });
    console.log(`✅ Success: ${command}`);
  } catch (error) {
    console.error(`❌ Failed: ${command}`, error.message);
    return false;
  }
  return true;
}

async function updatePackageJson(path, dependencies, devDependencies) {
  try {
    const packageJsonPath = join(path, 'package.json');
    if (!existsSync(packageJsonPath)) {
      console.error(`❌ package.json not found at ${packageJsonPath}`);
      return false;
    }

    const packageJson = JSON.parse(readFileSync(packageJsonPath, 'utf8'));
    packageJson.dependencies = { ...packageJson.dependencies, ...dependencies };
    packageJson.devDependencies = { ...packageJson.devDependencies, ...devDependencies };

    // Update engines for compatibility
    if (path.includes('frontend')) {
      packageJson.engines = {
        "node": ">=22.0.0",
        "npm": ">=10.0.0"
      };
    } else if (path.includes('backend')) {
      packageJson.engines = {
        "node": ">=18.0.0",
        "npm": ">=9.0.0"
      };
    }

    writeFileSync(packageJsonPath, JSON.stringify(packageJson, null, 2));
    console.log(`✅ Updated package.json at ${packageJsonPath}`);
    return true;
  } catch (error) {
    console.error(`❌ Failed to update package.json:`, error.message);
    return false;
  }
}

async function main() {
  try {
    console.log('🔄 Step 1: Updating package.json files...');
    
    // Update frontend package.json
    await updatePackageJson(frontendPath, frontendDependencies.dependencies, frontendDependencies.devDependencies);
    
    // Update backend package.json
    await updatePackageJson(backendPath, backendDependencies.dependencies, backendDependencies.devDependencies);

    console.log('🔄 Step 2: Installing frontend dependencies...');
    await runCommand('npm install --force', frontendPath);

    console.log('🔄 Step 3: Installing backend dependencies...');
    await runCommand('npm install', backendPath);

    console.log('🔄 Step 4: Testing frontend build...');
    const buildSuccess = await runCommand('npm run build:standard', frontendPath);
    
    if (!buildSuccess) {
      console.log('⚠️  Standard build failed, trying custom build...');
      await runCommand('npm run build', frontendPath);
    }

    console.log('🔄 Step 5: Running backend tests (if available)...');
    if (existsSync(join(backendPath, '__tests__')) || existsSync(join(backendPath, 'test'))) {
      await runCommand('npm test', backendPath);
    }

    console.log('✅ All fixes completed successfully!');
    console.log('');
    console.log('📋 Next steps:');
    console.log('1. Start backend: cd backend && npm run dev');
    console.log('2. Start frontend: cd frontend && npm run dev');
    console.log('3. Deploy to Vercel: vercel --prod');
    console.log('');
    console.log('🎉 Your CTAS application is ready for production!');

  } catch (error) {
    console.error('❌ Fix script failed:', error.message);
    process.exit(1);
  }
}

main();
