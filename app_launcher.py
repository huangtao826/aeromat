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
    print("Aeromat AI - Material Science AI Assistant")
    print("=" * 50)
    print()

    if getattr(sys, 'frozen', False):
        # 打包模式 - 使用打包的Python
        exe_dir = os.path.dirname(sys.executable)
        internal_dir = sys._MEIPASS

        # app.py 在 internal 目录
        app_path = os.path.join(internal_dir, 'app.py')
        if not os.path.exists(app_path):
            app_path = os.path.join(exe_dir, 'app.py')

        print(f"App path: {app_path}")
        print()

        # 创建配置目录
        config_dir = os.path.join(exe_dir, '.streamlit')
        os.makedirs(config_dir, exist_ok=True)
        os.environ['STREAMLIT_CONFIG_DIR'] = exe_dir

        # 启动streamlit
        print("Starting Streamlit...")
        print("Please open: http://localhost:8501")
        print()

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        subprocess.Popen(
            [sys.executable, '-m', 'streamlit', 'run', app_path,
             '--browser.gatherUsageStats', 'false',
             '--server.port', '8501',
             '--server.address', '0.0.0.0'],
            startupinfo=startupinfo
        )

        print("Running... Press Ctrl+C to stop.")
        input()

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