@echo off
chcp 65001 >nul 2>&1
title Aeromat AI

echo.
echo  ======================================
echo    Aeromat AI - 材料科学智能教学助手
echo  ======================================
echo.

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM 检查虚拟环境
if not exist "venv\Scripts\python.exe" (
    echo [错误] 未找到虚拟环境
    pause
    exit /b 1
)

REM 直接使用venv中的python，不激活
echo [启动] 启动Python环境...
echo.

echo ======================================
echo   启动中...
echo   请在浏览器中打开: http://localhost:8501
echo ======================================
echo.

REM 直接运行python
"%SCRIPT_DIR%venv\Scripts\python.exe" -m streamlit run "%SCRIPT_DIR%app.py" --server.port 8501 --browser.gatherUsageStats false

echo.
echo [退出] 程序已停止
pause