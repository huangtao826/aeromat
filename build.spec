import os
import sys

# 获取 streamlit 包路径
import streamlit
streamlit_path = os.path.dirname(streamlit.__file__)

# 获取项目根目录（spec 文件所在目录）
project_root = os.path.dirname(os.path.abspath(sys.argv[0]))

block_cipher = None
cipher = None

a = Analysis(
    ['app_launcher.py'],
    pathex=[project_root],
    binaries=[],
    datas=[
        ('knowledge', 'aeromat/knowledge'),
        ('ui', 'aeromat/ui'),
        ('config', 'aeromat/config'),
        ('agents', 'aeromat/agents'),
        ('core', 'aeromat/core'),
        ('__init__.py', 'aeromat/__init__.py'),
        ('app.py', '.'),
        ('aeromat_banner.png', '.'),
        (os.path.join(streamlit_path, 'static'), 'streamlit/static'),
        (os.path.join(streamlit_path, 'runtime'), 'streamlit/runtime'),
    ],
    hiddenimports=[
        'aeromat',
        'aeromat.core',
        'aeromat.core.llm_client',
        'aeromat.agents',
        'aeromat.agents.core_agent',
        'aeromat.agents.theory_agent',
        'aeromat.agents.software_agent',
        'aeromat.agents.result_agent',
        'aeromat.ui',
        'aeromat.config',
        'aeromat.knowledge',
        'streamlit',
        'streamlit.web.cli',
        'streamlit.runtime.scriptrunner.script_runner',
        'streamlit.runtime.scriptrunner.script_requests',
        'streamlit.runtime.uploaded_file_manager',
        'streamlit.runtime.state.session_state_proxy',
        'streamlit.runtime.metrics_util',
        'streamlit.web.server.server',
        'plotly',
        'plotly.graph_objects',
        'plotly.express',
        'pandas',
        'pandas.core.arrays.integer',
        'pandas.core.arrays.floating',
        'pandas.core.arrays.boolean',
        'requests',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AeromatAI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AeromatAI',
)
