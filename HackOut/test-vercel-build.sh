#!/bin/bash

echo "🧪 Testing Vercel build configuration locally..."

# Clean up any existing build artifacts
echo "🧹 Cleaning up previous builds..."
rm -rf frontend/dist
rm -rf frontend/node_modules
rm -rf node_modules

# Install dependencies
echo "📦 Installing root dependencies..."
npm install

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm ci --prefer-offline --no-audit
cd ..

# Test the build
echo "🔨 Testing build process..."
npm run vercel-build

if [ $? -eq 0 ]; then
    echo "✅ Build successful! Vercel deployment should work."
    echo "📁 Build output created at: frontend/dist/"
else
    echo "❌ Build failed. Please check the error messages above."
    exit 1
fi
