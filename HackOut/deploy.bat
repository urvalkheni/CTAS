@echo off
REM Vercel deployment fix script for CTAS (Windows)

echo 🚀 CTAS Vercel Deployment Fix
echo =============================

REM Check if we're in the right directory
if not exist "vercel.json" (
    echo ❌ Error: vercel.json not found. Make sure you're in the project root.
    pause
    exit /b 1
)

REM Navigate to frontend directory
cd frontend

REM Install dependencies
echo 📦 Installing dependencies...
call npm install

REM Build the project
echo 🔨 Building project...
call npm run build

if %ERRORLEVEL% EQU 0 (
    echo ✅ Build successful!
    echo.
    echo 📋 Deployment Steps:
    echo 1. Install Vercel CLI: npm install -g vercel
    echo 2. Login to Vercel: vercel login
    echo 3. Navigate to project root: cd ..
    echo 4. Deploy: vercel
    echo.
    echo 🌐 Your project is ready for deployment!
) else (
    echo ❌ Build failed. Please check the errors above.
    pause
    exit /b 1
)

pause
