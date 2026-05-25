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
    echo [错误] 未找到虚拟环境
    echo 请重新解压程序
    pause
    exit /b 1
)

REM 激活虚拟环境
echo [启动] 激活Python环境...
call venv\Scripts\activate.bat

REM 检查streamlit
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo [安装] 正在安装依赖...
    pip install streamlit pandas plotly requests
)

echo.
echo ======================================
echo   启动中...
echo   请在浏览器中打开: http://localhost:8501
echo ======================================
echo.

REM 启动streamlit
python -m streamlit run app.py --server.port 8501 --browser.gatherUsageStats false

echo.
echo [错误] 程序已退出
pause