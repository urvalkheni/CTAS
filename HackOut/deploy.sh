#!/bin/bash
# Vercel deployment fix script for CTAS

echo "🚀 CTAS Vercel Deployment Fix"
echo "============================="

# Navigate to project root
cd "$(dirname "$0")"

# Check if we're in the right directory
if [ ! -f "vercel.json" ]; then
    echo "❌ Error: vercel.json not found. Make sure you're in the project root."
    exit 1
fi

# Navigate to frontend directory
cd frontend

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Build the project
echo "🔨 Building project..."
npm run build

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo ""
    echo "📋 Deployment Steps:"
    echo "1. Install Vercel CLI: npm install -g vercel"
    echo "2. Login to Vercel: vercel login"
    echo "3. Navigate to project root: cd .."
    echo "4. Deploy: vercel"
    echo ""
    echo "🌐 Your project is ready for deployment!"
else
    echo "❌ Build failed. Please check the errors above."
    exit 1
fi
