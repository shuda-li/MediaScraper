# -*- coding: utf-8 -*-
import sys
import os

block_cipher = None

# 手动收集所有PyQt5相关文件
pyqt5_path = r'C:\Pychram\Python云烟\Lib\site-packages'

# PyQt5 DLLs
binaries = []
pyqt5_bin = os.path.join(pyqt5_path, 'PyQt5', 'Qt5', 'bin')
if os.path.exists(pyqt5_bin):
    for f in os.listdir(pyqt5_bin):
        if f.endswith('.dll'):
            binaries.append((os.path.join(pyqt5_bin, f), '.'))

# PyQt5 plugins
datas = []
pyqt5_plugins = os.path.join(pyqt5_path, 'PyQt5', 'Qt5', 'plugins')
if os.path.exists(pyqt5_plugins):
    for plugin_type in os.listdir(pyqt5_plugins):
        plugin_dir = os.path.join(pyqt5_plugins, plugin_type)
        if os.path.isdir(plugin_dir):
            datas.append((plugin_dir, plugin_type))

# PyQt5 Python files
pyqt5_py = os.path.join(pyqt5_path, 'PyQt5')
if os.path.exists(pyqt5_py):
    for f in os.listdir(pyqt5_py):
        if f.endswith('.py'):
            binaries.append((os.path.join(pyqt5_py, f), 'PyQt5'))

a = Analysis(
    ['media_scraper.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=[
        'PyQt5',
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'PyQt5.sip',
        'yt_dlp',
        'sqlite3',
        'glob',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PyQt5.Qt', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MediaScraper',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='media_scraper.ico',
)

