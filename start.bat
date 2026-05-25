@echo off
chcp 65001 >nul
title Aeromat AI

echo.
echo ====================================
echo   Aeromat AI
echo ====================================
echo.

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

if not exist "venv\Scripts\python.exe" (
    echo [ERROR] venv not found
    pause
    exit /b 1
)

echo [OK] Starting...
echo.
echo Open browser: http://localhost:8501
echo.

"%SCRIPT_DIR%venv\Scripts\python.exe" -m streamlit run "%SCRIPT_DIR%app.py" --server.port 8501 --browser.gatherUsageStats false

echo.
echo [STOPPED]
pause