# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import shutil
import site

def build_exe():
    print("=" * 60)
    print("开始打包 MediaScraper 应用...")
    print("=" * 60)

    app_dir = os.path.dirname(os.path.abspath(__file__))
    dist_dir = os.path.join(app_dir, 'dist')
    build_dir = os.path.join(app_dir, 'build')

    if os.path.exists(dist_dir):
        print(f"清理旧文件: {dist_dir}")
        shutil.rmtree(dist_dir)

    if os.path.exists(build_dir):
        print(f"清理旧文件: {build_dir}")
        shutil.rmtree(build_dir)

    os.makedirs(dist_dir, exist_ok=True)

    pyqt5_base = None
    for path in site.getsitepackages() + [site.getusersitepackages()]:
        qt_plugins = os.path.join(path, 'PyQt5', 'Qt5', 'plugins')
        if os.path.exists(qt_plugins):
            pyqt5_base = path
            print(f"✓ 找到 PyQt5: {pyqt5_base}")
            break

    if not pyqt5_base:
        print("✗ 未找到 PyQt5")
        return False

    print("正在执行 PyInstaller...")

    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--name=MediaScraper',
        '--windowed',
        '--onefile',
        '--icon=media_scraper.ico',
        '--paths', pyqt5_base,
        '--hidden-import=PyQt5',
        '--hidden-import=PyQt5.QtCore',
        '--hidden-import=PyQt5.QtGui',
        '--hidden-import=PyQt5.QtWidgets',
        '--hidden-import=yt_dlp',
        '--hidden-import=sqlite3',
        '--hidden-import=glob',
        '--collect-all=yt_dlp',
        '--noconfirm',
        f'--distpath={dist_dir}',
        f'--workpath={build_dir}',
        '--clean',
        'media_scraper.py'
    ]

    print()
    result = subprocess.run(cmd, capture_output=False)

    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("✓ PyInstaller 打包成功！")
        print("=" * 60)

        exe_path = os.path.join(dist_dir, 'MediaScraper.exe')
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"生成文件: {exe_path}")
            print(f"文件大小: {size_mb:.2f} MB")

            print("\n创建安装包目录...")
            installer_dir = os.path.join(dist_dir, 'installer')
            os.makedirs(installer_dir, exist_ok=True)
            shutil.copy(exe_path, installer_dir)

            print(f"\n✓ 所有文件已复制到: {installer_dir}")

            print("\n" + "=" * 60)
            print("✅ 打包完成！")
            print("\n📦 关于 ffmpeg:")
            print("  方案1 (推荐): 你手动下载 ffmpeg 并放一起打包")
            print("  方案2: 用户自己安装 ffmpeg，程序也能正常工作")
            print("\n下一步：")
            print("1. (可选) 下载 ffmpeg.exe 并放到 dist\\installer\\ 目录")
            print("2. 使用 Inno Setup 打开 media_scraper.iss")
            print("3. 点击 Compile 生成安装包")
            print("=" * 60)

    else:
        print("\n" + "=" * 60)
        print("✗ PyInstaller 打包失败！")
        print("=" * 60)
        return False

    return True

if __name__ == '__main__':
    success = build_exe()
    input("\n按 Enter 键退出...")
    sys.exit(0 if success else 1)
