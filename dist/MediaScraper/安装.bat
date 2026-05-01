@echo off
chcp 65001 ^>nul
title MediaScraper 安装向导
echo ========================================
echo    MediaScraper 安装
echo ========================================
echo.
echo [1/2] 正在检查Python...
python --version ^>nul 2^>^&1
if errorlevel 1 (
    echo [错误] 未找到Python！
    echo 请先安装Python 3.8或更高版本
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
python --version
echo [OK] Python已就绪
echo.
echo [2/2] 正在安装依赖...
pip install -r requirements.txt
echo.
echo ========================================
echo    安装完成！
echo ========================================
echo.
echo 现在双击"启动.bat"即可运行程序
echo.
echo ✅ 已包含ffmpeg，B站视频会有声音！
echo.
pause
