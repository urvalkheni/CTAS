@echo off
echo 🧪 Testing Vercel build configuration locally...

REM Clean up any existing build artifacts
echo 🧹 Cleaning up previous builds...
if exist frontend\dist rmdir /s /q frontend\dist
if exist frontend\node_modules rmdir /s /q frontend\node_modules
if exist node_modules rmdir /s /q node_modules

REM Install dependencies
echo 📦 Installing root dependencies...
npm install

REM Install frontend dependencies
echo 📦 Installing frontend dependencies...
cd frontend
npm ci --prefer-offline --no-audit
cd ..

REM Test the build
echo 🔨 Testing build process...
npm run vercel-build

if %ERRORLEVEL% EQU 0 (
    echo ✅ Build successful! Vercel deployment should work.
    echo 📁 Build output created at: frontend\dist\
) else (
    echo ❌ Build failed. Please check the error messages above.
    pause
    exit /b 1
)

pause
