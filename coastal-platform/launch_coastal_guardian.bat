@echo off
echo.
echo ================================================
echo    🌊 COASTAL GUARDIAN DIRECT LAUNCH 🌊
echo ================================================
echo.
echo Starting Coastal Guardian System...
echo.

REM Navigate to coastal_guardian directory
cd coastal_guardian

REM Launch Streamlit directly
echo Launching Streamlit Dashboard...
python -m streamlit run app.py --server.port 8501

echo.
echo Press any key to exit...
pause >nul
