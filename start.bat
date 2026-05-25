@echo off
chcp 65001 >nul 2>&1
title Aeromat AI

echo.
echo  AEROMAT AI 启动中...
echo.

cd /d "%~dp0"

call venv\Scripts\activate.bat

python -m streamlit run app.py --browser.gatherUsageStats false --server.port 8501