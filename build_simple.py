
# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import shutil

def build_simple():
    print("=" * 60)
    print("MediaScraper 简化打包程序")
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

    # 检查 ffmpeg
    ffmpeg_path = os.path.join(app_dir, 'ffmpeg.exe')
    has_ffmpeg = os.path.exists(ffmpeg_path)
    if has_ffmpeg:
        print(f"✓ 找到 ffmpeg.exe")
    else:
        print("⚠ 未找到 ffmpeg.exe (程序仍可工作)")

    print("正在执行 PyInstaller...")

    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--name=MediaScraper',
        '--windowed',
        '--onefile',
        '--icon=media_scraper.ico',
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
    try:
        result = subprocess.run(cmd, capture_output=False)
    except KeyboardInterrupt:
        print("\n\n用户中断打包")
        return False

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
            shutil.copy(os.path.join(app_dir, 'media_scraper.ico'), installer_dir)

            if has_ffmpeg:
                shutil.copy(ffmpeg_path, installer_dir)
                print(f"✓ 已包含 ffmpeg.exe")

            print(f"\n✓ 所有文件已复制到: {installer_dir}")
            print("\n目录内容:")
            for f in os.listdir(installer_dir):
                f_path = os.path.join(installer_dir, f)
                f_size = os.path.getsize(f_path) / (1024 * 1024)
                print(f"  - {f} ({f_size:.2f} MB)")

            print("\n" + "=" * 60)
            print("✅ 打包完成！")
            print("\n📦 下一步：")
            print("1. 安装 Inno Setup: https://jrsoftware.org/isdl.php")
            print("2. 用 Inno Setup 打开 media_scraper.iss")
            print("3. 点击 Compile 生成安装包")
            print("=" * 60)

    else:
        print("\n" + "=" * 60)
        print("✗ PyInstaller 打包失败！")
        print("=" * 60)
        print("\n💡 替代方案：")
        print("直接分享源代码 + requirements.txt，")
        print("用户安装 Python 后运行: pip install -r requirements.txt")
        return False

    return True

if __name__ == '__main__':
    success = build_simple()
    input("\n按 Enter 键退出...")
    sys.exit(0 if success else 1)

