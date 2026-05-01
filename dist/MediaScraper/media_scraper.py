# -*- coding: utf-8 -*-
import sys
import os
import glob
import sqlite3
import threading
from datetime import datetime
from contextlib import contextmanager
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLineEdit, QLabel, 
                             QTableWidget, QTableWidgetItem, QProgressBar, 
                             QFileDialog, QMessageBox, QTabWidget,
                             QCheckBox, QComboBox, QGroupBox, QStatusBar,
                             QHeaderView, QAbstractItemView, QSlider,
                             QMenuBar, QMenu, QAction, QToolBar, QDialog)
from PyQt5.QtCore import (Qt, QThread, pyqtSignal, QMutex, QUrl)
from PyQt5.QtGui import QDesktopServices

try:
    import yt_dlp
    YT_DLP_AVAILABLE = True
except ImportError:
    YT_DLP_AVAILABLE = False

import shutil

def find_ffmpeg():
    """智能查找 ffmpeg 可执行文件 - 优先当前目录"""
    print("正在查找ffmpeg...")
    
    # 1. 优先在程序目录找
    current_dir = os.path.dirname(os.path.abspath(__file__))
    ffmpeg_path = os.path.join(current_dir, 'ffmpeg.exe')
    if os.path.exists(ffmpeg_path):
        print(f"✅ 找到ffmpeg: {ffmpeg_path}")
        return ffmpeg_path
    
    # 2. 在PyInstaller临时目录找
    base_path = getattr(sys, '_MEIPASS', None)
    if base_path:
        ffmpeg_path = os.path.join(base_path, 'ffmpeg.exe')
        if os.path.exists(ffmpeg_path):
            print(f"✅ 找到ffmpeg(打包): {ffmpeg_path}")
            return ffmpeg_path
    
    # 3. 在系统PATH找
    ffmpeg_path = shutil.which('ffmpeg')
    if ffmpeg_path:
        print(f"✅ 找到ffmpeg(PATH): {ffmpeg_path}")
        return ffmpeg_path
    
    print("⚠️  未找到ffmpeg，视频可能没有声音")
    return None

FFMPEG_PATH = find_ffmpeg()
FFMPEG_AVAILABLE = FFMPEG_PATH is not None

THEMES = {
    'light': {
        'name': '浅色主题',
        'background': '#f8f9fa',
        'surface': '#ffffff',
        'primary': '#007bff',
        'primary_hover': '#0069d9',
        'primary_pressed': '#0056b3',
        'primary_text': '#ffffff',
        'text': '#212529',
        'text_secondary': '#6c757d',
        'border': '#dee2e6',
        'gridline': '#e9ecef',
        'disabled': '#adb5bd',
    },
    'dark': {
        'name': '深色主题',
        'background': '#1a1a2e',
        'surface': '#16213e',
        'primary': '#4a69bd',
        'primary_hover': '#3d5a9e',
        'primary_pressed': '#324a85',
        'primary_text': '#ffffff',
        'text': '#e8e8e8',
        'text_secondary': '#a0a0a0',
        'border': '#404040',
        'gridline': '#404040',
        'disabled': '#555555',
    },
    'green': {
        'name': '护眼绿色',
        'background': '#e8f5e9',
        'surface': '#ffffff',
        'primary': '#4caf50',
        'primary_hover': '#66bb6a',
        'primary_pressed': '#388e3c',
        'primary_text': '#ffffff',
        'text': '#2e7d32',
        'text_secondary': '#558b2f',
        'border': '#a5d6a7',
        'gridline': '#c8e6c9',
        'disabled': '#a5d6a7',
    },
    'purple': {
        'name': '优雅紫色',
        'background': '#f3e5f5',
        'surface': '#ffffff',
        'primary': '#9c27b0',
        'primary_hover': '#ab47bc',
        'primary_pressed': '#7b1fa2',
        'primary_text': '#ffffff',
        'text': '#4a148c',
        'text_secondary': '#6a1b9a',
        'border': '#ce93d8',
        'gridline': '#e1bee7',
        'disabled': '#ce93d8',
    },
    'orange': {
        'name': '活力橙色',
        'background': '#fff3e0',
        'surface': '#ffffff',
        'primary': '#ff9800',
        'primary_hover': '#ffa726',
        'primary_pressed': '#f57c00',
        'primary_text': '#ffffff',
        'text': '#e65100',
        'text_secondary': '#ef6c00',
        'border': '#ffcc80',
        'gridline': '#ffe0b2',
        'disabled': '#ffcc80',
    },
    'sakura': {
        'name': '樱花粉色',
        'background': '#fff5f8',
        'surface': '#ffffff',
        'primary': '#ff7eb3',
        'primary_hover': '#ff9fc4',
        'primary_pressed': '#ff66a3',
        'primary_text': '#ffffff',
        'text': '#8b3a5e',
        'text_secondary': '#c97a96',
        'border': '#ffcce6',
        'gridline': '#ffe6f0',
        'disabled': '#ffb3d1',
    },
}

class ThemeManager:
    def __init__(self):
        self.current_theme = 'sakura'
    
    def get_stylesheet(self, theme_name=None):
        if theme_name is None:
            theme_name = self.current_theme
        
        theme = THEMES.get(theme_name, THEMES['sakura'])
        
        return f"""
            QMainWindow {{ 
                background-color: {theme['background']}; 
            }}
            QWidget {{
                background-color: {theme['background']};
                color: {theme['text']};
                font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
            }}
            QGroupBox {{
                font-weight: bold;
                border: 2px solid {theme['border']};
                border-radius: 12px;
                margin-top: 12px;
                padding-top: 15px;
                padding-left: 12px;
                padding-right: 12px;
                padding-bottom: 12px;
                background-color: {theme['surface']};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 3px 12px;
                color: {theme['text']};
                background-color: {theme['background']};
                border-radius: 8px;
            }}
            QPushButton {{
                background-color: {theme['primary']};
                color: {theme['primary_text']};
                border: none;
                padding: 10px 24px;
                border-radius: 25px;
                min-width: 80px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {theme['primary_hover']};
            }}
            QPushButton:pressed {{
                background-color: {theme['primary_pressed']};
            }}
            QPushButton:disabled {{
                background-color: {theme['disabled']};
                color: {theme['text_secondary']};
            }}
            QTableWidget {{
                background-color: {theme['surface']};
                border: 1px solid {theme['border']};
                border-radius: 10px;
                gridline-color: {theme['gridline']};
                color: {theme['text']};
                alternate-background-color: {theme['background']};
            }}
            QHeaderView::section {{
                background-color: {theme['primary']};
                color: {theme['primary_text']};
                padding: 8px;
                border: none;
                border-radius: 5px;
            }}
            QLineEdit {{
                padding: 10px 14px;
                border: 1px solid {theme['border']};
                border-radius: 10px;
                background-color: {theme['surface']};
                color: {theme['text']};
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border-color: {theme['primary']};
                border-width: 2px;
            }}
            QProgressBar {{
                border: 1px solid {theme['border']};
                border-radius: 12px;
                text-align: center;
                background-color: {theme['surface']};
                height: 14px;
            }}
            QProgressBar::chunk {{
                background-color: {theme['primary']};
                border-radius: 12px;
            }}
            QComboBox {{
                padding: 8px 12px;
                border: 1px solid {theme['border']};
                border-radius: 10px;
                background-color: {theme['surface']};
                color: {theme['text']};
                font-size: 13px;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            QComboBox::down-arrow {{
                image: none;
            }}
            QComboBox::item {{
                background-color: {theme['surface']};
                color: {theme['text']};
                padding: 10px 14px;
            }}
            QComboBox::item:selected {{
                background-color: {theme['primary']};
                color: {theme['primary_text']};
            }}
            QLabel {{
                color: {theme['text']};
            }}
            QStatusBar {{
                background-color: {theme['surface']};
                color: {theme['text']};
                border-top: 1px solid {theme['border']};
            }}
            QTabWidget::pane {{
                border: 1px solid {theme['border']};
                border-radius: 10px;
                background-color: {theme['surface']};
            }}
            QTabBar::tab {{
                background-color: {theme['surface']};
                color: {theme['text_secondary']};
                padding: 10px 22px;
                border-radius: 10px 10px 0 0;
                margin-right: 4px;
                font-weight: 500;
            }}
            QTabBar::tab:selected {{
                background-color: {theme['primary']};
                color: {theme['primary_text']};
            }}
            QMenuBar {{
                background-color: {theme['surface']};
                color: {theme['text']};
                border-bottom: 1px solid {theme['border']};
            }}
            QMenuBar::item:selected {{
                background-color: {theme['primary']};
                color: {theme['primary_text']};
            }}
            QMenu {{
                background-color: {theme['surface']};
                color: {theme['text']};
                border: 1px solid {theme['border']};
                border-radius: 10px;
            }}
            QMenu::item:selected {{
                background-color: {theme['primary']};
                color: {theme['primary_text']};
            }}
            QScrollBar:vertical {{
                background-color: {theme['background']};
                width: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {theme['border']};
                border-radius: 6px;
            }}
            QScrollBar:horizontal {{
                background-color: {theme['background']};
                height: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:horizontal {{
                background-color: {theme['border']};
                border-radius: 6px;
            }}
            QCheckBox {{
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border-radius: 8px;
                border: 2px solid {theme['border']};
                background-color: {theme['surface']};
            }}
            QCheckBox::indicator:checked {{
                background-color: {theme['primary']};
                border-color: {theme['primary']};
            }}
            QCheckBox::indicator:hover {{
                border-color: {theme['primary']};
            }}
            QSlider::groove:horizontal {{
                height: 8px;
                background-color: {theme['border']};
                border-radius: 4px;
            }}
            QSlider::handle:horizontal {{
                width: 20px;
                height: 20px;
                background-color: {theme['primary']};
                border-radius: 10px;
                margin: -6px 0;
            }}
            QToolButton {{
                background-color: transparent;
                border: none;
            }}
            QToolButton:hover {{
                background-color: {theme['border']};
                border-radius: 5px;
            }}
        """
    
    def apply_theme(self, theme_name):
        self.current_theme = theme_name

class DatabaseManager:
    def __init__(self, db_path='download_history.db'):
        self.db_path = db_path
        self.local = threading.local()
        
        # 删除旧数据库重新创建
        if os.path.exists(self.db_path):
            print(f"删除旧数据库: {self.db_path}")
            os.remove(self.db_path)
        
        self._init_db()
    
    def _get_connection(self):
        if not hasattr(self.local, 'conn'):
            self.local.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        return self.local.conn
    
    @contextmanager
    def get_cursor(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception:
            conn.rollback()
            raise
    
    def _init_db(self):
        print("初始化数据库...")
        with self.get_cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS downloads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL,
                    title TEXT,
                    type TEXT,
                    format TEXT,
                    file_path TEXT,
                    file_size INTEGER,
                    status TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP,
                    retry_count INTEGER DEFAULT 0
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS download_resume (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL,
                    file_path TEXT,
                    downloaded_bytes INTEGER DEFAULT 0,
                    total_bytes INTEGER DEFAULT 0,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(url)
                )
            ''')
        print("数据库初始化完成")
    
    def add_download(self, url, title, type, format, file_path, file_size):
        with self.get_cursor() as cursor:
            cursor.execute('''
                INSERT INTO downloads (url, title, type, format, file_path, file_size, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (url, title, type, format, file_path, file_size, 'downloading'))
            return cursor.lastrowid
    
    def update_download_status(self, id, status):
        with self.get_cursor() as cursor:
            if status == 'completed':
                cursor.execute('''
                    UPDATE downloads SET status = ?, completed_at = CURRENT_TIMESTAMP WHERE id = ?
                ''', (status, id))
            else:
                cursor.execute('UPDATE downloads SET status = ? WHERE id = ?', (status, id))
    
    def update_retry_count(self, id, count):
        with self.get_cursor() as cursor:
            cursor.execute('UPDATE downloads SET retry_count = ? WHERE id = ?', (count, id))
    
    def get_all_downloads(self):
        with self.get_cursor() as cursor:
            cursor.execute('SELECT * FROM downloads ORDER BY created_at DESC')
            return cursor.fetchall()
    
    def get_resume_data(self, url):
        with self.get_cursor() as cursor:
            cursor.execute('SELECT * FROM download_resume WHERE url = ?', (url,))
            return cursor.fetchone()
    
    def save_resume_data(self, url, file_path, downloaded_bytes, total_bytes):
        with self.get_cursor() as cursor:
            cursor.execute('''
                INSERT OR REPLACE INTO download_resume 
                (url, file_path, downloaded_bytes, total_bytes, last_updated)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (url, file_path, downloaded_bytes, total_bytes))
    
    def delete_resume_data(self, url):
        with self.get_cursor() as cursor:
            cursor.execute('DELETE FROM download_resume WHERE url = ?', (url,))

class ResourceInfo:
    def __init__(self, url, title, type, formats, file_size=None):
        self.url = url
        self.title = title
        self.type = type
        self.formats = formats
        self.file_size = file_size

class DownloadTask:
    def __init__(self, resource_info, save_path, format_id=None):
        self.resource_info = resource_info
        self.url = resource_info.url
        self.title = resource_info.title
        self.type = resource_info.type
        self.save_path = save_path
        self.format_id = format_id
        self.status = 'waiting'
        self.progress = 0
        self.speed = 0
        self.retry_count = 0
        self.file_path = None

class AnalyzeThread(QThread):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)
    
    def __init__(self, url, use_generic_extractor=False):
        super().__init__()
        self.url = url
        self.use_generic_extractor = use_generic_extractor
    
    def run(self):
        if not YT_DLP_AVAILABLE:
            self.error.emit('yt-dlp 未安装，无法使用')
            return
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        if self.use_generic_extractor:
            ydl_opts['extractor_args'] = {'youtube': {'skip': ['dash', 'hls']}}
            ydl_opts['force_generic_extractor'] = True
        
        try:
            resources = []
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=False)
                
                formats = []
                if 'formats' in info:
                    for f in info['formats']:
                        if f.get('ext') in ['mp4', 'webm', 'm4a', 'mp3', 'webm', 'm4a']:
                            format_type = 'video' if f.get('vcodec', 'none') != 'none' else 'audio'
                            has_audio = f.get('acodec', 'none') != 'none'
                            
                            label = f"{f.get('height', 'N/A')}p" if format_type == 'video' else f"{f.get('abr', 'N/A')}kbps"
                            if format_type == 'video' and has_audio:
                                label += ' (有音频)'
                            
                            file_size = f.get('filesize', 0) or f.get('filesize_approx', 0)
                            if file_size:
                                label += f" - {self.format_size(file_size)}"
                            
                            formats.append({
                                'id': f['format_id'],
                                'type': format_type,
                                'label': label,
                                'has_audio': has_audio,
                                'file_size': file_size,
                                'ext': f.get('ext', 'mp4'),
                            })
                
                title = info.get('title', '未知标题')
                resource_type = 'video' if formats else 'video'
                
                resource = ResourceInfo(
                    url=self.url,
                    title=title,
                    type=resource_type,
                    formats=formats,
                    file_size=info.get('filesize', 0)
                )
                resources.append(resource)
            
            self.finished.emit(resources)
        
        except Exception as e:
            error_msg = str(e)
            if 'Unsupported URL' in error_msg:
                if not self.use_generic_extractor:
                    self.error.emit('unsupported_url')
                else:
                    self.error.emit(f'不支持的 URL: {self.url}')
            else:
                self.error.emit(error_msg)
    
    @staticmethod
    def format_size(size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

class DownloadThread(QThread):
    progress_updated = pyqtSignal(int, float, float)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, task, db_manager, max_retries=3):
        super().__init__()
        self.task = task
        self.db_manager = db_manager
        self.max_retries = max_retries
        self._is_cancelled = False
        self._is_paused = False
        self.mutex = QMutex()
    
    def cancel(self):
        self.mutex.lock()
        self._is_cancelled = True
        self.mutex.unlock()
    
    def pause(self):
        self.mutex.lock()
        self._is_paused = True
        self.mutex.unlock()
    
    def resume(self):
        self.mutex.lock()
        self._is_paused = False
        self.mutex.unlock()
    
    def is_paused(self):
        self.mutex.lock()
        result = self._is_paused
        self.mutex.unlock()
        return result
    
    def is_cancelled(self):
        self.mutex.lock()
        result = self._is_cancelled
        self.mutex.unlock()
        return result
    
    def run(self):
        while self.task.retry_count <= self.max_retries:
            if self.is_cancelled():
                self.error.emit('下载已取消')
                return
            
            try:
                self.download()
                self.finished.emit(self.task.title)
                return
            
            except Exception as e:
                self.task.retry_count += 1
                if self.task.retry_count <= self.max_retries:
                    self.task.status = f'重试 ({self.task.retry_count}/{self.max_retries})'
                    self.sleep(2)
                else:
                    self.error.emit(str(e))
    
    def download(self):
        if not YT_DLP_AVAILABLE:
            raise Exception('yt-dlp 未安装')
        
        print(f"开始下载: {self.task.url}")
        
        safe_title = self.sanitize_filename(self.task.title)
        output_path = os.path.join(self.task.save_path, safe_title)
        
        self.task.file_path = output_path
        print(f"保存路径: {output_path}")
        
        ydl_opts = {
            'outtmpl': f"{output_path}.%(ext)s",
            'progress_hooks': [self.progress_hook],
            'quiet': False,
            'no_warnings': False,
            'continuedl': False,
            'overwrites': True,
            'nocheckcertificate': True,
            'socket_timeout': 60,
            'retries': 3,
            'buffersize': 1024,
            'http_chunk_size': 10485760,
        }
        
        # 检查ffmpeg是否可用
        has_ffmpeg = False
        if FFMPEG_AVAILABLE:
            try:
                import subprocess
                test_result = subprocess.run(
                    [FFMPEG_PATH, '-version'], 
                    capture_output=True, 
                    text=True,
                    timeout=10
                )
                if test_result.returncode == 0:
                    has_ffmpeg = True
                    print(f"✅ ffmpeg可用: {FFMPEG_PATH}")
            except Exception as e:
                print(f"⚠️ ffmpeg不可用: {e}")
        
        if has_ffmpeg:
            # 使用ffmpeg合并模式（B站必需）
            print("🎯 使用方案：ffmpeg合并模式（视频+音频）")
            ydl_opts['ffmpeg_location'] = FFMPEG_PATH
            ydl_opts['ffmpeg_args'] = ['-hide_banner', '-loglevel', 'error']
            ydl_opts['format'] = 'bestvideo+bestaudio/best'
            ydl_opts['merge_output_format'] = 'mp4'
            print("使用视频+音频自动合并模式")
        else:
            # 没有ffmpeg时，优先选择已包含音频的完整视频流
            print("🎯 使用方案：优先选择已包含音频的完整视频流")
            
            format_spec = None
            
            # 1. 如果用户选择了格式，使用用户选择的
            if self.task.format_id:
                format_spec = self.task.format_id
                print(f"使用用户选择的格式: {format_spec}")
            
            # 2. 否则，尝试从分析结果中找已经包含音频的视频流
            elif self.task.resource_info.formats and len(self.task.resource_info.formats) > 0:
                # 找同时包含视频和音频的格式
                best_format = None
                for fmt in self.task.resource_info.formats:
                    # 检查是否有视频和音频
                    has_video = fmt.get('vcodec', 'none') != 'none'
                    has_audio = fmt.get('acodec', 'none') != 'none'
                    
                    if has_video and has_audio:
                        # 找质量最好的
                        if not best_format or fmt.get('height', 0) > best_format.get('height', 0):
                            best_format = fmt
                
                if best_format:
                    format_spec = best_format['id']
                    print(f"✅ 找到已包含音频的完整视频流: {best_format.get('height', 'unknown')}p")
                else:
                    # 如果没有找到，就用第一个
                    format_spec = self.task.resource_info.formats[0]['id']
                    print(f"⚠️ 未找到完整视频流，使用第一个可用格式: {format_spec}")
            
            # 3. 最后，用默认的 'best'（yt-dlp会自动选择最好的单一流）
            else:
                format_spec = 'best'
                print(f"使用默认格式: {format_spec}")
            
            ydl_opts['format'] = format_spec
            print(f"最终使用的格式: {format_spec}")
        
        print(f"下载选项: {ydl_opts}")
        
        try:
            # 删除已存在的文件（如果有），强制重新下载
            existing_files = glob.glob(f"{output_path}.*")
            for f in existing_files:
                try:
                    print(f"删除已存在的文件: {f}")
                    os.remove(f)
                except Exception as e:
                    print(f"删除文件失败: {e}")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print("调用 ytdl.download")
                result = ydl.download([self.task.url])
                print(f"下载结果: {result}")
                if result != 0:
                    raise Exception(f"下载失败，返回码: {result}")
        except Exception as e:
            print(f"下载异常: {str(e)}")
            import traceback
            print(traceback.format_exc())
            raise
    
    def progress_hook(self, d):
        print(f"进度更新: {d}")
        
        if self.is_cancelled():
            raise Exception('下载已取消')
        
        if d['status'] == 'downloading':
            percent = d.get('downloaded_bytes', 0) / d.get('total_bytes', 1) * 100
            speed = d.get('speed', 0) or 0
            total = d.get('total_bytes', 0)
            
            print(f"下载中: {percent:.1f}%, {speed/1024:.1f} KB/s")
            
            self.task.progress = percent
            self.task.speed = speed
            self.task.status = 'downloading'
            
            self.progress_updated.emit(int(percent), speed, total)
            
            self.db_manager.save_resume_data(
                self.task.url,
                self.task.file_path,
                d.get('downloaded_bytes', 0),
                total
            )
        
        elif d['status'] == 'finished':
            print("下载完成!")
            self.task.progress = 100
            self.task.speed = 0
            self.task.status = 'completed'
            self.progress_updated.emit(100, 0, 0)
            self.db_manager.delete_resume_data(self.task.url)
        
        elif d['status'] == 'error':
            print(f"下载错误: {d}")
            error_msg = d.get('error', '未知错误')
            raise Exception(f"下载过程出错: {error_msg}")
    
    @staticmethod
    def sanitize_filename(name):
        invalid_chars = '<>:"/\\|?*'
        for c in invalid_chars:
            name = name.replace(c, '_')
        return name

class MediaScraperWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.theme_manager = ThemeManager()
        self.resources = []
        self.download_queue = []
        self.download_threads = {}
        self.init_ui()
        self.load_history()
        self.apply_theme('sakura')
    
    def init_ui(self):
        self.setWindowTitle('MediaScraper - 媒体资源爬取工具')
        self.setMinimumSize(1000, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        self.init_download_tab()
        self.init_history_tab()
        self.init_settings_tab()
        
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        if FFMPEG_AVAILABLE:
            self.status_bar.showMessage(f'就绪 - ffmpeg 已检测到: {FFMPEG_PATH}')
        else:
            self.status_bar.showMessage('就绪 - ffmpeg 未找到，将使用单一流模式')
    
    def init_download_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        url_group = QGroupBox('URL 输入')
        url_layout = QHBoxLayout()
        url_group.setLayout(url_layout)
        
        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText('输入视频或音频网址...')
        self.url_edit.returnPressed.connect(self.analyze_url)
        
        self.analyze_btn = QPushButton('分析')
        self.analyze_btn.clicked.connect(self.analyze_url)
        
        url_layout.addWidget(QLabel('网址:'))
        url_layout.addWidget(self.url_edit, 1)
        url_layout.addWidget(self.analyze_btn)
        
        layout.addWidget(url_group)
        
        resource_group = QGroupBox('资源列表')
        resource_layout = QVBoxLayout()
        resource_group.setLayout(resource_layout)
        
        self.resource_table = QTableWidget()
        self.resource_table.setColumnCount(5)
        self.resource_table.setHorizontalHeaderLabels(['选择', '类型', '标题', '大小', '画质选项'])
        self.resource_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.resource_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.resource_table.setAlternatingRowColors(True)
        self.resource_table.verticalHeader().setVisible(False)
        
        resource_layout.addWidget(self.resource_table)
        
        btn_layout = QHBoxLayout()
        self.select_all_btn = QPushButton('全选')
        self.select_all_btn.clicked.connect(self.select_all_resources)
        self.download_btn = QPushButton('下载选中')
        self.download_btn.clicked.connect(self.download_selected)
        self.open_folder_btn = QPushButton('打开文件夹')
        self.open_folder_btn.clicked.connect(self.open_save_folder)
        
        btn_layout.addWidget(self.select_all_btn)
        btn_layout.addWidget(self.download_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.open_folder_btn)
        
        resource_layout.addLayout(btn_layout)
        layout.addWidget(resource_group)
        
        queue_group = QGroupBox('下载队列')
        queue_layout = QVBoxLayout()
        queue_group.setLayout(queue_layout)
        
        self.queue_table = QTableWidget()
        self.queue_table.setColumnCount(7)
        self.queue_table.setHorizontalHeaderLabels(['', '标题', '类型', '进度', '速度', '状态', '操作'])
        self.queue_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.queue_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.queue_table.setAlternatingRowColors(True)
        self.queue_table.verticalHeader().setVisible(False)
        
        queue_layout.addWidget(self.queue_table)
        
        queue_btn_layout = QHBoxLayout()
        self.pause_all_btn = QPushButton('暂停队列')
        self.pause_all_btn.clicked.connect(self.pause_all_downloads)
        self.resume_all_btn = QPushButton('继续队列')
        self.resume_all_btn.clicked.connect(self.resume_all_downloads)
        self.clear_queue_btn = QPushButton('清空队列')
        self.clear_queue_btn.clicked.connect(self.clear_queue)
        
        queue_btn_layout.addWidget(self.pause_all_btn)
        queue_btn_layout.addWidget(self.resume_all_btn)
        queue_btn_layout.addStretch()
        queue_btn_layout.addWidget(self.clear_queue_btn)
        
        queue_layout.addLayout(queue_btn_layout)
        layout.addWidget(queue_group)
        
        self.save_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'MediaScraper')
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        
        self.tab_widget.addTab(widget, '下载管理')
    
    def init_history_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        search_layout = QHBoxLayout()
        search_label = QLabel('搜索:')
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText('输入关键词搜索...')
        self.search_edit.textChanged.connect(self.filter_history)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_edit)
        layout.addLayout(search_layout)
        
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(7)
        self.history_table.setHorizontalHeaderLabels(['ID', '标题', '类型', '格式', '状态', '日期', '重试次数'])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.history_table.setAlternatingRowColors(True)
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.cellDoubleClicked.connect(self.open_downloaded_file)
        
        layout.addWidget(self.history_table)
        
        history_btn_layout = QHBoxLayout()
        self.refresh_history_btn = QPushButton('刷新历史')
        self.refresh_history_btn.clicked.connect(self.load_history)
        self.delete_history_btn = QPushButton('删除选中')
        self.delete_history_btn.clicked.connect(self.delete_history_item)
        
        history_btn_layout.addWidget(self.refresh_history_btn)
        history_btn_layout.addWidget(self.delete_history_btn)
        history_btn_layout.addStretch()
        
        layout.addLayout(history_btn_layout)
        
        self.tab_widget.addTab(widget, '下载历史')
    
    def init_settings_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        general_group = QGroupBox('通用设置')
        general_layout = QVBoxLayout()
        general_group.setLayout(general_layout)
        
        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel('保存路径:'))
        self.path_edit = QLineEdit(self.save_path)
        self.browse_btn = QPushButton('浏览...')
        self.browse_btn.clicked.connect(self.browse_path)
        path_layout.addWidget(self.path_edit, 1)
        path_layout.addWidget(self.browse_btn)
        
        general_layout.addLayout(path_layout)
        
        thread_layout = QHBoxLayout()
        thread_layout.addWidget(QLabel('并发下载数:'))
        self.thread_combo = QComboBox()
        self.thread_combo.addItems(['1', '2', '3', '4', '5'])
        self.thread_combo.setCurrentIndex(2)
        thread_layout.addWidget(self.thread_combo)
        thread_layout.addStretch()
        
        general_layout.addLayout(thread_layout)
        
        retry_layout = QHBoxLayout()
        retry_layout.addWidget(QLabel('自动重试次数:'))
        self.retry_combo = QComboBox()
        self.retry_combo.addItems(['0', '1', '2', '3', '4', '5'])
        self.retry_combo.setCurrentIndex(3)
        retry_layout.addWidget(self.retry_combo)
        retry_layout.addStretch()
        
        general_layout.addLayout(retry_layout)
        
        speed_layout = QHBoxLayout()
        speed_layout.addWidget(QLabel('下载速度限制:'))
        self.speed_combo = QComboBox()
        self.speed_combo.addItems(['无限制', '100 KB/s', '200 KB/s', '500 KB/s', '1 MB/s', '2 MB/s'])
        self.speed_combo.setCurrentIndex(0)
        speed_layout.addWidget(self.speed_combo)
        speed_layout.addStretch()
        
        general_layout.addLayout(speed_layout)
        
        layout.addWidget(general_group)
        
        theme_group = QGroupBox('界面主题')
        theme_layout = QVBoxLayout()
        theme_group.setLayout(theme_layout)
        
        theme_select_layout = QHBoxLayout()
        theme_select_layout.addWidget(QLabel('选择主题:'))
        self.theme_combo = QComboBox()
        for key, theme in THEMES.items():
            self.theme_combo.addItem(theme['name'], key)
        self.theme_combo.currentIndexChanged.connect(self.change_theme)
        theme_select_layout.addWidget(self.theme_combo)
        theme_select_layout.addStretch()
        
        theme_layout.addLayout(theme_select_layout)
        
        preview_btn = QPushButton('预览主题')
        preview_btn.clicked.connect(self.preview_theme)
        theme_layout.addWidget(preview_btn)
        
        layout.addWidget(theme_group)
        
        layout.addStretch()
        
        self.tab_widget.addTab(widget, '设置')
    
    def apply_theme(self, theme_name):
        self.theme_manager.apply_theme(theme_name)
        stylesheet = self.theme_manager.get_stylesheet()
        self.setStyleSheet(stylesheet)
    
    def change_theme(self, index):
        theme_name = self.theme_combo.itemData(index)
        self.apply_theme(theme_name)
    
    def preview_theme(self):
        index = self.theme_combo.currentIndex()
        theme_name = self.theme_combo.itemData(index)
        self.apply_theme(theme_name)
    
    def analyze_url(self):
        url = self.url_edit.text().strip()
        if not url:
            QMessageBox.warning(self, '警告', '请输入网址')
            return
        
        self.analyze_btn.setEnabled(False)
        self.status_bar.showMessage('正在分析...')
        
        self.analyze_thread = AnalyzeThread(url)
        self.analyze_thread.finished.connect(self.on_analyze_finished)
        self.analyze_thread.error.connect(self.on_analyze_error)
        self.analyze_thread.start()
    
    def on_analyze_finished(self, resources):
        self.resources = resources
        self.resource_table.setRowCount(len(resources))
        
        for i, resource in enumerate(resources):
            checkbox = QCheckBox()
            checkbox.setStyleSheet('QCheckBox::indicator { width: 20px; height: 20px; }')
            self.resource_table.setCellWidget(i, 0, checkbox)
            
            self.resource_table.setItem(i, 1, QTableWidgetItem('视频' if resource.type == 'video' else '音频'))
            self.resource_table.setItem(i, 2, QTableWidgetItem(resource.title))
            
            size_text = '未知'
            if resource.file_size:
                size_text = self.format_size(resource.file_size)
            self.resource_table.setItem(i, 3, QTableWidgetItem(size_text))
            
            combo = QComboBox()
            for fmt in resource.formats:
                combo.addItem(fmt['label'], fmt['id'])
            if resource.formats:
                combo.setCurrentIndex(0)
            self.resource_table.setCellWidget(i, 4, combo)
        
        self.analyze_btn.setEnabled(True)
        self.status_bar.showMessage(f'分析完成，找到 {len(resources)} 个资源')
    
    def on_analyze_error(self, error_msg):
        self.analyze_btn.setEnabled(True)
        
        if error_msg == 'unsupported_url':
            reply = QMessageBox.question(
                self,
                '不支持的 URL',
                '此网址暂不支持直接识别。是否尝试使用通用提取器模式？',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )
            if reply == QMessageBox.Yes:
                url = self.url_edit.text().strip()
                self.analyze_btn.setEnabled(False)
                self.status_bar.showMessage('正在使用通用提取器分析...')
                
                self.analyze_thread = AnalyzeThread(url, use_generic_extractor=True)
                self.analyze_thread.finished.connect(self.on_analyze_finished)
                self.analyze_thread.error.connect(self.on_analyze_error)
                self.analyze_thread.start()
        else:
            QMessageBox.critical(self, '分析失败', error_msg)
            self.status_bar.showMessage('分析失败')
    
    def select_all_resources(self):
        for i in range(self.resource_table.rowCount()):
            checkbox = self.resource_table.cellWidget(i, 0)
            if checkbox:
                checkbox.setChecked(True)
    
    def download_selected(self):
        selected = []
        for i in range(self.resource_table.rowCount()):
            checkbox = self.resource_table.cellWidget(i, 0)
            if checkbox and checkbox.isChecked():
                selected.append(i)
        
        if not selected:
            QMessageBox.warning(self, '警告', '请先选择要下载的资源')
            return
        
        if not YT_DLP_AVAILABLE:
            QMessageBox.critical(self, '错误', 'yt-dlp 未安装，无法下载！')
            return
        
        max_threads = int(self.thread_combo.currentText())
        max_retries = int(self.retry_combo.currentText())
        
        for i in selected:
            resource = self.resources[i]
            combo = self.resource_table.cellWidget(i, 4)
            format_id = combo.currentData() if combo else None
            
            task = DownloadTask(resource, self.save_path, format_id)
            self.download_queue.append(task)
            
            thread = DownloadThread(task, self.db_manager, max_retries=max_retries)
            self.download_threads[id(task)] = thread
            
            self.add_task_to_queue(task)
            
            thread.progress_updated.connect(
                lambda p, s, t, tid=id(task): self.update_progress(tid, p, s, t)
            )
            thread.finished.connect(
                lambda t, tid=id(task): self.on_download_finished(tid, t)
            )
            thread.error.connect(
                lambda e, tid=id(task): self.on_download_error(tid, e)
            )
        
        self.start_next_downloads(max_threads)
        
        QMessageBox.information(self, '开始下载', f'已添加 {len(selected)} 个任务到下载队列')
    
    def add_task_to_queue(self, task):
        row = self.queue_table.rowCount()
        self.queue_table.insertRow(row)
        
        self.queue_table.setItem(row, 1, QTableWidgetItem(task.title))
        self.queue_table.setItem(row, 2, QTableWidgetItem('视频' if task.type == 'video' else '音频'))
        
        progress = QProgressBar()
        progress.setValue(0)
        self.queue_table.setCellWidget(row, 3, progress)
        
        self.queue_table.setItem(row, 4, QTableWidgetItem('0 KB/s'))
        self.queue_table.setItem(row, 5, QTableWidgetItem('等待中'))
        
        cancel_btn = QPushButton('取消')
        cancel_btn.clicked.connect(lambda _, tid=id(task): self.cancel_download(tid))
        self.queue_table.setCellWidget(row, 6, cancel_btn)
    
    def start_next_downloads(self, max_threads):
        active_count = sum(
            1 for task in self.download_queue 
            if task.status in ['downloading', 'paused']
        )
        
        for task in self.download_queue:
            if task.status == 'waiting' and active_count < max_threads:
                task.status = 'downloading'
                thread = self.download_threads[id(task)]
                thread.start()
                active_count += 1
                self.update_task_status(task, '下载中')
    
    def update_progress(self, task_id, percent, speed, total):
        for row in range(self.queue_table.rowCount()):
            for i, task in enumerate(self.download_queue):
                if id(task) == task_id:
                    progress = self.queue_table.cellWidget(row, 3)
                    if progress:
                        progress.setValue(int(percent))
                    
                    speed_text = f'{speed/1024:.1f} KB/s' if speed else '0 KB/s'
                    self.queue_table.setItem(row, 4, QTableWidgetItem(speed_text))
                    
                    break
    
    def update_task_status(self, task, status):
        for row in range(self.queue_table.rowCount()):
            for i, t in enumerate(self.download_queue):
                if id(t) == id(task):
                    self.queue_table.setItem(row, 5, QTableWidgetItem(status))
                    break
    
    def on_download_finished(self, task_id, title):
        for row in range(self.queue_table.rowCount()):
            for i, task in enumerate(self.download_queue):
                if id(task) == task_id:
                    task.status = 'completed'
                    self.queue_table.setItem(row, 5, QTableWidgetItem('已完成'))
                    
                    self.db_manager.add_download(
                        task.url,
                        task.title,
                        task.type,
                        task.format_id or 'best',
                        task.file_path,
                        0
                    )
                    self.db_manager.update_download_status(
                        len(self.download_queue),
                        'completed'
                    )
                    
                    break
        
        max_threads = int(self.thread_combo.currentText())
        self.start_next_downloads(max_threads)
        
        self.load_history()
    
    def on_download_error(self, task_id, error_msg):
        for row in range(self.queue_table.rowCount()):
            for i, task in enumerate(self.download_queue):
                if id(task) == task_id:
                    task.status = 'failed'
                    self.queue_table.setItem(row, 5, QTableWidgetItem(f'失败: {error_msg}'))
                    
                    self.db_manager.update_download_status(
                        len(self.download_queue),
                        'failed'
                    )
                    
                    break
        
        QMessageBox.critical(self, '下载失败', f'下载失败: {error_msg}')
    
    def cancel_download(self, task_id):
        for row in range(self.queue_table.rowCount()):
            for i, task in enumerate(self.download_queue):
                if id(task) == task_id:
                    if task.status in ['downloading', 'waiting']:
                        thread = self.download_threads.get(task_id)
                        if thread:
                            thread.cancel()
                        
                        task.status = 'cancelled'
                        self.queue_table.setItem(row, 5, QTableWidgetItem('已取消'))
                        
                        self.db_manager.update_download_status(
                            len(self.download_queue),
                            'cancelled'
                        )
                    
                    break
    
    def pause_all_downloads(self):
        for task in self.download_queue:
            if task.status == 'downloading':
                thread = self.download_threads.get(id(task))
                if thread:
                    thread.pause()
                task.status = 'paused'
                self.update_task_status(task, '已暂停')
    
    def resume_all_downloads(self):
        for task in self.download_queue:
            if task.status == 'paused':
                thread = self.download_threads.get(id(task))
                if thread:
                    thread.resume()
                task.status = 'downloading'
                self.update_task_status(task, '下载中')
    
    def clear_queue(self):
        for task in self.download_queue:
            thread = self.download_threads.get(id(task))
            if thread:
                thread.cancel()
        
        self.download_queue.clear()
        self.download_threads.clear()
        self.queue_table.setRowCount(0)
    
    def load_history(self):
        self.history_table.setRowCount(0)
        
        downloads = self.db_manager.get_all_downloads()
        
        for d in downloads:
            row = self.history_table.rowCount()
            self.history_table.insertRow(row)
            
            self.history_table.setItem(row, 0, QTableWidgetItem(str(d[0])))
            self.history_table.setItem(row, 1, QTableWidgetItem(d[2]))
            self.history_table.setItem(row, 2, QTableWidgetItem('视频' if d[3] == 'video' else '音频'))
            self.history_table.setItem(row, 3, QTableWidgetItem(d[4]))
            self.history_table.setItem(row, 4, QTableWidgetItem(d[7]))
            self.history_table.setItem(row, 5, QTableWidgetItem(d[8]))
            self.history_table.setItem(row, 6, QTableWidgetItem(str(d[10])))
    
    def filter_history(self):
        text = self.search_edit.text().lower()
        for row in range(self.history_table.rowCount()):
            title_item = self.history_table.item(row, 1)
            if title_item:
                title = title_item.text().lower()
                self.history_table.setRowHidden(row, text not in title)
    
    def open_downloaded_file(self, row, column):
        url_item = self.history_table.item(row, 1)
        if not url_item:
            return
        
        QMessageBox.information(
            self,
            '提示',
            '打开文件功能需要实际文件路径。请在下载管理标签页中使用"打开文件夹"。'
        )
    
    def delete_history_item(self):
        selected_rows = set()
        for item in self.history_table.selectedItems():
            selected_rows.add(item.row())
        
        if not selected_rows:
            QMessageBox.warning(self, '警告', '请先选择要删除的历史记录')
            return
        
        reply = QMessageBox.question(
            self,
            '确认删除',
            f'确定要删除选中的 {len(selected_rows)} 条历史记录吗？',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            QMessageBox.information(self, '提示', '历史记录删除功能需要完善数据库操作。')
            self.load_history()
    
    def browse_path(self):
        path = QFileDialog.getExistingDirectory(self, '选择保存目录', self.save_path)
        if path:
            self.save_path = path
            self.path_edit.setText(path)
    
    def open_save_folder(self):
        if os.path.exists(self.save_path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(self.save_path))
        else:
            QMessageBox.warning(self, '警告', '目录不存在')
    
    @staticmethod
    def format_size(size):
        if not size:
            return '未知'
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

def main():
    app = QApplication(sys.argv)
    
    window = MediaScraperWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
