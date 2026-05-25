#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aeromat AI 打包工具
"""

import os
import sys
import subprocess
import shutil


def main():
    print("=" * 50)
    print("Aeromat AI 打包工具")
    print("=" * 50)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    venv_dir = os.path.join(script_dir, "venv")
    dist_dir = os.path.join(script_dir, "dist")
    build_dir = os.path.join(script_dir, "build")

    # 检查 Python
    try:
        subprocess.run(["python", "--version"], capture_output=True, check=True)
    except:
        print("[错误] 未检测到 Python")
        input("按 Enter 退出...")
        sys.exit(1)

    # 创建虚拟环境
    if not os.path.exists(venv_dir):
        print("[创建] 虚拟环境...")
        subprocess.run(["python", "-m", "venv", venv_dir], check=True)

    # 安装依赖
    print("[安装] 依赖...")
    pip_exe = os.path.join(venv_dir, "Scripts", "pip.exe")
    subprocess.run([pip_exe, "install", "--upgrade", "pip"], check=True)
    subprocess.run([pip_exe, "install", "streamlit", "pyinstaller"], check=True)

    # 清理
    for d in ["dist", "build"]:
        p = os.path.join(script_dir, d)
        if os.path.exists(p):
            shutil.rmtree(p)

    # 创建简单的启动脚本
    exe_dir = os.path.join(dist_dir, "AeromatAI")
    os.makedirs(exe_dir, exist_ok=True)

    # 复制所有必要文件
    print("[复制] 文件...")
    for folder in ["knowledge", "ui", "config", "agents", "core"]:
        src = os.path.join(script_dir, folder)
        if os.path.exists(src):
            shutil.copytree(src, os.path.join(exe_dir, folder))

    shutil.copy(os.path.join(script_dir, "app.py"), exe_dir)
    shutil.copytree(venv_dir, os.path.join(exe_dir, "venv"), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))

    # 创建启动bat
    with open(os.path.join(exe_dir, "启动.bat"), "w", encoding="utf-8") as f:
        f.write("@echo off\n")
        f.write("cd /d \"%~dp0\"\n")
        f.write("call venv\\Scripts\\activate.bat\n")
        f.write("python -m streamlit run app.py --browser.gatherUsageStats false --server.port 8501\n")

    print()
    print("=" * 50)
    print("打包完成！")
    print(f"目录: {exe_dir}")
    print("运行: dist\\AeromatAI\\启动.bat")
    print("=" * 50)
    input("按 Enter 退出...")

if __name__ == "__main__":
    main()