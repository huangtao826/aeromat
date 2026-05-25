#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aeromat AI 启动器
用于 PyInstaller 打包
"""

import os
import sys
import subprocess

def main():
    """启动 Streamlit 应用"""
    print("=" * 50)
    print("Aeromat AI")
    print("=" * 50)
    print()

    if getattr(sys, 'frozen', False):
        # 打包模式 - exe 在 dist\AeromatAI\AeromatAI.exe
        exe_dir = os.path.dirname(sys.executable)
        internal_dir = sys._MEIPASS

        # app.py 在打包的 _internal 目录或 exe 同目录
        app_path = os.path.join(internal_dir, 'app.py')
        if not os.path.exists(app_path):
            app_path = os.path.join(exe_dir, 'app.py')

        print(f"Exe dir: {exe_dir}")
        print(f"App path: {app_path}")
        print()

        # 创建 streamlit 配置目录
        config_dir = os.path.join(exe_dir, '.streamlit')
        os.makedirs(config_dir, exist_ok=True)
        os.environ['STREAMLIT_CONFIG_DIR'] = exe_dir

        # 启动 streamlit，使用打包的 Python
        python_exe = sys.executable

        print("Starting Streamlit...")
        print()

        # 使用 CREATE_NO_WINDOW 避免弹出黑窗口
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        proc = subprocess.Popen(
            [python_exe, '-m', 'streamlit', 'run', app_path,
             '--browser.gatherUsageStats', 'false',
             '--server.port', '8501',
             '--server.headless', 'true'],
            startupinfo=startupinfo
        )

        print("Please open browser: http://localhost:8501")
        print("Press Ctrl+C to stop")
        print()

        try:
            proc.wait()
        except KeyboardInterrupt:
            print("\nStopping...")

    else:
        # 开发模式
        script_dir = os.path.dirname(os.path.abspath(__file__))
        app_path = os.path.join(script_dir, 'app.py')

        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', app_path,
            '--browser.gatherUsageStats', 'false',
            '--server.port', '8501'
        ])

if __name__ == "__main__":
    main()