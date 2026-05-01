
@echo off
chcp 65001 >nul
echo ============================================================
echo MediaScraper 完整打包
echo ============================================================
echo.

echo [1/4] 清理旧文件...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

echo.
echo [2/4] 正在打包（请稍候，需要3-5分钟）...
pyinstaller --name=MediaScraper --windowed --onefile --icon=media_scraper.ico --hidden-import=PyQt5 --hidden-import=PyQt5.QtCore --hidden-import=PyQt5.QtGui --hidden-import=PyQt5.QtWidgets --hidden-import=yt_dlp --hidden-import=sqlite3 --hidden-import=glob --collect-all=yt_dlp --noconfirm media_scraper.py

if errorlevel 1 (
    echo.
    echo [错误] 打包失败！
    echo.
    echo 解决方案：
    echo 1. 重新安装 PyQt5: pip install --upgrade pyqt5
    echo 2. 或者使用绿色版方案（直接运行Python脚本）
    pause
    exit /b 1
)

echo.
echo [3/4] 整理安装包文件...
if not exist dist\installer mkdir dist\installer
copy dist\MediaScraper.exe dist\installer\MediaScraper.exe
copy media_scraper.ico dist\installer\media_scraper.ico

if exist ffmpeg.exe (
    copy ffmpeg.exe dist\installer\ffmpeg.exe
    echo [OK] 已包含 ffmpeg.exe
)

echo.
echo [4/4] 完成！
echo.
echo ============================================================
echo 文件位置: dist\installer\
echo.
dir dist\installer\ /b
echo.
echo ============================================================
echo 下一步：
echo 1. 安装 Inno Setup: https://jrsoftware.org/isdl.php
echo 2. 打开 media_scraper.iss
echo 3. 点击 Compile
echo ============================================================
echo.
pause

