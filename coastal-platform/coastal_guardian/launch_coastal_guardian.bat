@echo off
echo.
echo ================================================
echo    🌊 COASTAL GUARDIAN SYSTEM LAUNCHER 🌊
echo ================================================
echo.
echo Starting Coastal Guardian Unified System...
echo.

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Launch the unified system
python launch_system.py

echo.
echo Press any key to exit...
pause >nul
