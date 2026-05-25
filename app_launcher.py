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
    print("Aeromat AI - 材料科学智能教学助手")
    print("=" * 50)
    print()

    if getattr(sys, 'frozen', False):
        # 打包模式
        exe_dir = os.path.dirname(sys.executable)

        # app.py 在同目录或 _internal
        app_path = os.path.join(exe_dir, 'app.py')
        if not os.path.exists(app_path):
            app_path = os.path.join(sys._MEIPASS, 'app.py')

        # 设置环境
        os.makedirs(os.path.join(exe_dir, '.streamlit'), exist_ok=True)
        os.environ['STREAMLIT_CONFIG_DIR'] = exe_dir

        # 启动
        subprocess.Popen([
            sys.executable, '-m', 'streamlit', 'run', app_path,
            '--browser.gatherUsageStats', 'false',
            '--server.port', '8501'
        ])

        print("请在浏览器中打开: http://localhost:8501")
        print("按 Ctrl+C 停止服务")
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