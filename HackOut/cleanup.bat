@echo off
echo Cleaning up unnecessary files...

REM Change to HackOut directory
cd /d "e:\DAIICT_Unstop_Hackout\HackOut"

REM Remove documentation files
if exist "AUTHENTICATION_TESTING_GUIDE.md" del /f /q "AUTHENTICATION_TESTING_GUIDE.md" >nul 2>&1
if exist "AUTH_API_COMPLETE_GUIDE.md" del /f /q "AUTH_API_COMPLETE_GUIDE.md" >nul 2>&1
if exist "Complete_Auth_Tests.json" del /f /q "Complete_Auth_Tests.json" >nul 2>&1
if exist "CTAS_Authentication_API.json" del /f /q "CTAS_Authentication_API.json" >nul 2>&1
if exist "LOGIN_DEBUG.md" del /f /q "LOGIN_DEBUG.md" >nul 2>&1
if exist "Register_API_Tests.json" del /f /q "Register_API_Tests.json" >nul 2>&1
if exist "VERCEL_FIX.md" del /f /q "VERCEL_FIX.md" >nul 2>&1
if exist "VERCEL_FIX_SUMMARY.md" del /f /q "VERCEL_FIX_SUMMARY.md" >nul 2>&1
if exist "DEPLOYMENT_COMPLETE.md" del /f /q "DEPLOYMENT_COMPLETE.md" >nul 2>&1
if exist "DEPLOYMENT_STATUS.md" del /f /q "DEPLOYMENT_STATUS.md" >nul 2>&1
if exist "NOAA_INTEGRATION_SUMMARY.md" del /f /q "NOAA_INTEGRATION_SUMMARY.md" >nul 2>&1

REM Remove deployment scripts
if exist "deploy.bat" del /f /q "deploy.bat" >nul 2>&1
if exist "deploy.sh" del /f /q "deploy.sh" >nul 2>&1
if exist "test-vercel-build.bat" del /f /q "test-vercel-build.bat" >nul 2>&1
if exist "test-vercel-build.sh" del /f /q "test-vercel-build.sh" >nul 2>&1

REM Remove alternative deployment configs
if exist "netlify.toml" del /f /q "netlify.toml" >nul 2>&1
if exist "railway.json" del /f /q "railway.json" >nul 2>&1
if exist "docker-compose.yml" del /f /q "docker-compose.yml" >nul 2>&1

REM Remove temporary files
if exist "fix-codebase.js" del /f /q "fix-codebase.js" >nul 2>&1
if exist ".nvmrc" del /f /q ".nvmrc" >nul 2>&1

REM Remove root package files
if exist "package.json" del /f /q "package.json" >nul 2>&1
if exist "package-lock.json" del /f /q "package-lock.json" >nul 2>&1

REM Remove node_modules
if exist "node_modules" rmdir /s /q "node_modules" >nul 2>&1

echo Cleanup complete!
pause
