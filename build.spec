import os
import sys
import glob

# 获取 streamlit 包路径
import streamlit
streamlit_path = os.path.dirname(streamlit.__file__)

# 获取项目根目录
project_root = os.path.dirname(os.path.abspath(sys.argv[0]))

block_cipher = None
cipher = None

a = Analysis(
    ['app_launcher.py'],
    pathex=[project_root],
    binaries=[],
    # ===== 修复：datas 使用 2元组 (src, dest) =====
    datas=[
        ('knowledge', 'aeromat/knowledge'),
        ('ui', 'aeromat/ui'),
        ('config', 'aeromat/config'),
        ('agents', 'aeromat/agents'),
        ('core', 'aeromat/core'),
        ('__init__.py', 'aeromat/__init__.py'),
        ('app.py', '.'),
        ('aeromat_banner.png', '.'),
        # Streamlit 静态资源
        (os.path.join(streamlit_path, 'static'), 'streamlit/static'),
        (os.path.join(streamlit_path, 'runtime'), 'streamlit/runtime'),
    ],
    hiddenimports=[
        'importlib.metadata',
        'importlib_metadata',
        'importlib_metadata.distributions',
        'importlib_metadata._itertools',
        'importlib_metadata._functools',
        'importlib_metadata._collections',
        'importlib_metadata._text',
        'importlib_metadata._meta',
        'importlib_metadata._adapters',
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
        'streamlit.version',
        'streamlit.config',
        'streamlit.config_option',
        'streamlit.config_util',
        'streamlit.development',
        'streamlit.env_util',
        'streamlit.file_util',
        'streamlit.git_util',
        'streamlit.logger',
        'streamlit.net_util',
        'streamlit.platform',
        'streamlit.string_util',
        'streamlit.type_util',
        'streamlit.url_util',
        'streamlit.user_info',
        'streamlit.util',
        'streamlit.watcher',
        'streamlit.source_util',
        'streamlit.proto',
        'streamlit.proto.BackMsg_pb2',
        'streamlit.proto.ForwardMsg_pb2',
        'streamlit.proto.Common_pb2',
        'streamlit.proto.Delta_pb2',
        'streamlit.proto.Element_pb2',
        'streamlit.proto.NewSession_pb2',
        'streamlit.proto.SessionEvent_pb2',
        'streamlit.proto.SessionStatus_pb2',
        'streamlit.proto.WidgetStates_pb2',
        'streamlit.proto.openmetrics_data_model_pb2',
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

# ===== 修复：动态添加 streamlit dist-info（使用2元组格式）=====
# 查找实际的 dist-info 目录
dist_info_pattern = os.path.join(streamlit_path, '..', 'streamlit-*.dist-info')
dist_info_paths = glob.glob(dist_info_pattern)

for dist_info_path in dist_info_paths:
    if os.path.isdir(dist_info_path):
        # 获取实际的目录名（不含通配符）
        dist_info_name = os.path.basename(dist_info_path)
        # 使用2元组格式：(src_path, dest_name)
        a.datas.append((dist_info_path, dist_info_name))

# 同时查找并添加 streamlit 的其他元数据目录
site_packages = os.path.dirname(streamlit_path)
if os.path.exists(site_packages):
    for item in os.listdir(site_packages):
        if item.startswith('streamlit-') and item.endswith('.dist-info'):
            full_path = os.path.join(site_packages, item)
            if os.path.isdir(full_path):
                # 检查是否已添加（比较 src_path）
                already_added = any(d[0] == full_path for d in a.datas)
                if not already_added:
                    a.datas.append((full_path, item))

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
