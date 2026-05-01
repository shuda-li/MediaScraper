# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import shutil

def build_perfect():
    print("=" * 60)
    print("MediaScraper 完美打包（含完整PyQt5）")
    print("=" * 60)

    app_dir = os.path.dirname(os.path.abspath(__file__))
    dist_dir = os.path.join(app_dir, 'dist')
    build_dir = os.path.join(app_dir, 'build')

    # 清理旧文件
    if os.path.exists(dist_dir):
        print(f"清理旧文件: {dist_dir}")
        shutil.rmtree(dist_dir)
    if os.path.exists(build_dir):
        print(f"清理旧文件: {build_dir}")
        shutil.rmtree(build_dir)

    os.makedirs(dist_dir, exist_ok=True)

    # 使用虚拟环境的Python
    venv_python = os.path.join(app_dir, '.venv', 'Scripts', 'python.exe')
    if not os.path.exists(venv_python):
        print(f"未找到虚拟环境Python: {venv_python}")
        print("请先运行: python -m venv .venv")
        print("然后: .venv\\Scripts\\activate")
        print("然后: pip install pyqt5 yt-dlp pyinstaller")
        return False

    print(f"使用Python: {venv_python}")

    # 检查依赖
    print("\n检查依赖...")
    try:
        result = subprocess.run([venv_python, '-c', 'import PyQt5; print("PyQt5 OK")'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ PyQt5 已安装")
        else:
            print("❌ PyQt5 未安装")
            return False
    except:
        print("❌ PyQt5 未安装")
        return False

    try:
        result = subprocess.run([venv_python, '-c', 'import yt_dlp; print("yt_dlp OK")'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ yt_dlp 已安装")
        else:
            print("❌ yt_dlp 未安装")
            return False
    except:
        print("❌ yt_dlp 未安装")
        return False

    # 创建临时spec文件
    print("\n创建打包配置...")
    spec_content = '''# -*- coding: utf-8 -*-
import sys
import os

block_cipher = None

a = Analysis(
    ['media_scraper.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'PyQt5',
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'PyQt5.sip',
        'yt_dlp',
        'sqlite3',
        'glob',
        'yt_dlp.compat',
        'yt_dlp.compat._legacy',
        'yt_dlp.compat._deprecated',
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
'''

    spec_file = os.path.join(app_dir, 'MediaScraper_perfect.spec')
    with open(spec_file, 'w', encoding='utf-8') as f:
        f.write(spec_content)

    # 开始打包
    print("\n开始打包（需要5-10分钟，请耐心等待）...")
    cmd = [
        venv_python, '-m', 'PyInstaller',
        '--collect-all=yt_dlp',
        '--noconfirm',
        f'--distpath={dist_dir}',
        f'--workpath={build_dir}',
        '--clean',
        spec_file
    ]

    print()
    try:
        result = subprocess.run(cmd, capture_output=False)
    except KeyboardInterrupt:
        print("\n\n用户中断")
        return False

    if result.returncode != 0:
        print("\n打包失败！")
        return False

    # 检查结果
    exe_file = os.path.join(dist_dir, 'MediaScraper.exe')
    if not os.path.exists(exe_file):
        print("\n错误：未找到生成的EXE！")
        return False

    size_mb = os.path.getsize(exe_file) / (1024 * 1024)
    print(f"\n生成文件: {exe_file}")
    print(f"文件大小: {size_mb:.2f} MB")

    # 整理到安装包目录
    print("\n整理安装包...")
    installer_dir = os.path.join(dist_dir, 'installer')
    os.makedirs(installer_dir, exist_ok=True)
    shutil.copy(exe_file, installer_dir)
    shutil.copy(os.path.join(app_dir, 'media_scraper.ico'), installer_dir)

    ffmpeg_path = os.path.join(app_dir, 'ffmpeg.exe')
    if os.path.exists(ffmpeg_path):
        shutil.copy(ffmpeg_path, installer_dir)
        print(f"✅ 已包含ffmpeg")

    print("\n" + "=" * 60)
    print("✅ 完美打包完成！")
    print("=" * 60)
    print(f"\n单EXE文件: {exe_file}")
    print(f"\n完整安装包目录: {installer_dir}")
    print("\n安装包目录内容:")
    for f in os.listdir(installer_dir):
        f_path = os.path.join(installer_dir, f)
        f_size = os.path.getsize(f_path) / (1024 * 1024)
        print(f"  - {f} ({f_size:.2f} MB)")

    print("\n" + "=" * 60)
    print("测试说明:")
    print("1. 双击运行 MediaScraper.exe 测试")
    print("2. 如果正常，就可以直接分享给用户")
    print("3. 或者用 Inno Setup 继续做安装包")
    print("=" * 60)

    return True

if __name__ == '__main__':
    success = build_perfect()
    if not success:
        print("\n提示：先试试 ZIP 方案吧！dist\\MediaScraper_完整版.zip")
    input("\n按 Enter 键退出...")
    sys.exit(0 if success else 1)
