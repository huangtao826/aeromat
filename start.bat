@echo off
chcp 65001 >nul 2>&1
title Aeromat AI

echo.
echo  ======================================
echo    Aeromat AI - 材料科学智能教学助手
echo  ======================================
echo.

cd /d "%~dp0"

REM 检查虚拟环境
if not exist "venv" (
    echo [创建] 首次运行，正在创建环境...
    python -m venv venv
)

echo [安装] 安装依赖...
call venv\Scripts\pip.exe install --upgrade pip
call venv\Scripts\pip.exe install streamlit pandas plotly requests

echo.
echo ======================================
echo   启动中...
echo   请在浏览器中打开: http://localhost:8501
echo ======================================
echo.

REM 启动streamlit
call venv\Scripts\python.exe -m streamlit run app.py --server.port 8501 --browser.gatherUsageStats false

echo.
echo [错误] 程序已退出
pause