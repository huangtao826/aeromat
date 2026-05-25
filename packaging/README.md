# Aeromat AI Windows 打包指南

## 方案一：使用打包脚本（一键）

1. 将整个 `aeromat` 文件夹复制到 Windows 电脑

2. 双击运行 `packaging/build_windows.bat`

3. 等待打包完成（约5-10分钟）

4. 在 `dist\AeromatAI.exe` 找到生成的可执行文件

## 方案二：手动打包

### 1. 安装依赖
```bash
pip install pyinstaller streamlit
```

### 2. 创建 spec 文件（build.spec）
```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app_launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('knowledge', 'knowledge'),
        ('ui', 'ui'),
        ('config', 'config'),
        ('agents', 'agents'),
        ('core', 'core'),
    ],
    hiddenimports=['streamlit', 'plotly'],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AeromatAI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)
```

### 3. 执行打包
```bash
pyinstaller build.spec
```

## 打包后目录结构

```
dist/
└── AeromatAI.exe    # 可直接双击运行的主程序
```

## 配置 API Key

打包后首次运行会提示配置 API Key，也可在运行前设置环境变量：

```bash
set DASHSCOPE_API_KEY=your-api-key
AeromatAI.exe
```

或将 `env.template` 复制为 `.env` 放在同一目录。

## 注意事项

1. **依赖较大**：PyTorch + Transformers 约 2-4GB，打包后文件约 1-2GB
2. **首次运行**：需要约 1-2 分钟初始化
3. **离线使用**：无 API Key 时只能使用内置知识库回答
4. **杀毒软件**：部分杀毒软件可能误报，添加信任即可