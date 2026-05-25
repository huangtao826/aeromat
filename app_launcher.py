#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aeromat AI 启动器
用于 PyInstaller 打包 - v2.0 完整版
"""

import os
import sys
import time
import threading
import webbrowser
import urllib.request
import urllib.error

def open_browser_when_ready(url, max_wait=30):
    """后台线程等待服务器启动后打开浏览器"""
    print(f"[Browser] 等待服务器启动: {url}")
    start_time = time.time()
    while time.time() - start_time < max_wait:
        try:
            req = urllib.request.Request(url, method="HEAD")
            req.add_header("User-Agent", "AeromatAI-Launcher")
            urllib.request.urlopen(req, timeout=2)
            print(f"[Browser] 服务器就绪，正在打开浏览器...")
            webbrowser.open(url)
            print(f"[Browser] 已打开: {url}")
            return True
        except urllib.error.URLError:
            time.sleep(0.5)
        except Exception as e:
            print(f"[Browser] 检查出错: {e}")
            time.sleep(0.5)
    print(f"[Browser] 等待超时，请手动打开: {url}")
    return False

def main():
    # ===== 强制禁用 Streamlit 注册界面 =====
    os.environ["STREAMLIT_BROWSER_GATHERUSAGESTATS"] = "false"
    os.environ["STREAMLIT_GLOBAL_DEVELOPMENTMODE"] = "false"
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    os.environ["STREAMLIT_CLIENT_SHOW_ERROR_DETAILS"] = "false"
    # ======================================

    print("=" * 50)
    print("Aeromat AI - Material Science AI Assistant")
    print("=" * 50)
    print()

    if getattr(sys, "frozen", False):
        internal_dir = sys._MEIPASS
        exe_dir = os.path.dirname(sys.executable)
    else:
        internal_dir = os.path.dirname(os.path.abspath(__file__))
        exe_dir = internal_dir

    # 将 internal_dir 加入 Python 路径
    if internal_dir not in sys.path:
        sys.path.insert(0, internal_dir)

    # app.py 路径
    app_path = os.path.join(internal_dir, "app.py")
    if not os.path.exists(app_path):
        app_path = os.path.join(exe_dir, "app.py")

    print(f"App path: {app_path}")
    print(f"Working dir: {exe_dir}")
    print()

    if not os.path.exists(app_path):
        print("[错误] 找不到 app.py 文件！")
        print(f"查找路径: {app_path}")
        input("按 Enter 退出...")
        sys.exit(1)

    # 创建 Streamlit 配置目录
    config_dir = os.path.join(exe_dir, ".streamlit")
    os.makedirs(config_dir, exist_ok=True)
    os.environ["STREAMLIT_CONFIG_DIR"] = config_dir
    os.environ["HOME"] = exe_dir
    os.environ["USERPROFILE"] = exe_dir

    # 创建 config.toml 禁用统计
    config_file = os.path.join(config_dir, "config.toml")
    with open(config_file, "w", encoding="utf-8") as f:
        f.write("""
[browser]
gatherUsageStats = false

[server]
headless = true

[global]
developmentMode = false
""")

    server_url = "http://localhost:8501"

    # 后台线程打开浏览器
    browser_thread = threading.Thread(
        target=open_browser_when_ready,
        args=(server_url, 30),
        daemon=True
    )
    browser_thread.start()

    print("Starting Streamlit...")
    print(f"访问地址: {server_url}")
    print("浏览器即将自动打开...")
    print()

    try:
        import streamlit.web.cli as stcli

        sys.argv = [
            "streamlit",
            "run",
            app_path,
            "--global.developmentMode=false",
            "--server.port=8501",
            "--server.address=127.0.0.1",
            "--browser.gatherUsageStats=false",
            "--server.enableCORS=false",
            "--server.enableXsrfProtection=false"
        ]

        sys.exit(stcli.main())

    except Exception as e:
        print(f"[错误] 启动失败: {e}")
        import traceback
        traceback.print_exc()
        input("按 Enter 退出...")
        sys.exit(1)

if __name__ == "__main__":
    main()
