# -*- coding: utf-8 -*-
import sys
import os

block_cipher = None

# 手动收集PyQt5文件
pyqt5_path = r'C:\Pychram\Python云烟\Lib\site-packages'

# PyQt5 DLLs
binaries = []
pyqt5_bin = os.path.join(pyqt5_path, 'PyQt5', 'Qt5', 'bin')
if os.path.exists(pyqt5_bin):
    for dll in ['Qt5Core.dll', 'Qt5Gui.dll', 'Qt5Widgets.dll']:
        dll_path = os.path.join(pyqt5_bin, dll)
        if os.path.exists(dll_path):
            binaries.append((dll_path, '.'))

# PyQt5 plugins
datas = []
pyqt5_plugins = os.path.join(pyqt5_path, 'PyQt5', 'Qt5', 'plugins')
if os.path.exists(pyqt5_plugins):
    for plugin_type in ['platforms', 'styles']:
        plugin_dir = os.path.join(pyqt5_plugins, plugin_type)
        if os.path.exists(plugin_dir):
            datas.append((plugin_dir, plugin_type))

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
    excludes=[],
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

