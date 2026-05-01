@echo off
chcp 65001 ^>nul
title MediaScraper 启动
python media_scraper.py
if errorlevel 1 (
    echo.
    echo 程序异常退出，按任意键关闭...
    pause ^>nul
)
