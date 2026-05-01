@echo off
chcp 65001 >nul
echo ========================================
echo  MediaScraper 完整版制作
echo ========================================
echo.

set PYTHON=C:\Pychram\Python云烟\python.exe

echo [1/4] 创建目录结构...
if exist dist rmdir /s /q dist
mkdir dist\MediaScraper
mkdir dist\MediaScraper\installer
mkdir dist\MediaScraper\data

echo.
echo [2/4] 复制主程序...
copy media_scraper.py dist\MediaScraper\
copy media_scraper.ico dist\MediaScraper\
copy requirements.txt dist\MediaScraper\

echo.
echo [3/4] 复制ffmpeg...
if exist ffmpeg.exe (
    copy ffmpeg.exe dist\MediaScraper\
    echo [OK] ffmpeg 已复制
)

echo.
echo [4/4] 创建启动脚本...
(
echo @echo off
echo chcp 65001 ^>nul
echo title MediaScraper
echo python media_scraper.py
echo pause
) > dist\MediaScraper\启动.bat

(
echo @echo off
echo chcp 65001 ^>nul
echo title MediaScraper 安装
echo echo 正在安装依赖...
echo pip install -r requirements.txt
echo echo.
echo echo ========================================
echo echo 安装完成！
echo echo 双击"启动.bat"来运行程序
echo echo ========================================
echo pause
) > dist\MediaScraper\安装.bat

echo.
echo ========================================
echo 制作完成！
echo ========================================
echo.
echo 文件位置：dist\MediaScraper\
echo.
echo 使用方法：
echo 1. 把整个 MediaScraper 文件夹复制给用户
echo 2. 用户双击"安装.bat"安装依赖
echo 3. 双击"启动.bat"运行程序
echo.
pause

