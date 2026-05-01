# -*- coding: utf-8 -*-
from PIL import Image
import os

def convert_png_to_ico():
    """将 PNG 图片转换为 ICO 格式"""
    
    # 图片路径
    png_path = os.path.join(os.path.dirname(__file__), '1776386627760.png')
    ico_path = os.path.join(os.path.dirname(__file__), 'media_scraper.ico')
    
    if not os.path.exists(png_path):
        print(f"✗ 找不到图片: {png_path}")
        return False
    
    try:
        # 打开图片
        img = Image.open(png_path)
        print(f"✓ 图片信息:")
        print(f"  尺寸: {img.size}")
        print(f"  模式: {img.mode}")
        
        # 转换为 RGBA 模式（如果需要）
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # 创建不同尺寸的图标
        sizes = [256, 128, 64, 48, 32, 16]
        icons = []
        
        for size in sizes:
            resized = img.resize((size, size), Image.Resampling.LANCZOS)
            icons.append(resized)
        
        # 保存为 ICO 文件
        # PIL 的 ICO 保存需要多个尺寸
        icons[0].save(
            ico_path,
            format='ICO',
            sizes=[(s, s) for s in sizes],
            append_images=icons[1:]
        )
        
        print(f"\n✓ ICO 图标已创建: {ico_path}")
        print(f"  包含尺寸: {', '.join([f'{s}x{s}' for s in sizes])}")
        return True
        
    except ImportError:
        print("✗ 需要安装 Pillow 库")
        print("  运行: pip install Pillow")
        return False
    except Exception as e:
        print(f"✗ 转换失败: {e}")
        return False

if __name__ == '__main__':
    success = convert_png_to_ico()
    if success:
        print("\n✓ 可以使用这个图标进行打包了！")
    input("\n按 Enter 键退出...")
