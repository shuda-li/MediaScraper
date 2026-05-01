# -*- coding: utf-8 -*-
import struct
import os

def create_media_scraper_icon():
    """创建一个樱花风格的图标"""
    
    # 尺寸
    width = 32
    height = 32
    
    # 颜色 (BGRA format)
    primary = (179, 126, 255, 255)    # 樱花粉 #ff7eb3
    secondary = (94, 58, 139, 255)    # 深粉 #8b3a5e  
    background = (248, 245, 255, 255)  # 淡粉白 #fff5f8
    white = (255, 255, 255, 255)
    
    # 创建像素数据
    pixels = []
    for y in range(height):
        row = []
        for x in range(width):
            cx, cy = width // 2, height // 2
            dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            
            # 创建圆形渐变图标
            if dist < 13:
                if dist < 9:
                    # 中心 - 主色
                    row.append(primary)
                elif dist < 13:
                    # 边缘 - 深色
                    row.append(secondary)
                else:
                    # 边框
                    row.append(secondary)
            else:
                # 透明
                row.append((0, 0, 0, 0))
        pixels.append(row)
    
    # 转换为 bytes (BGRA, bottom-up)
    pixel_data = b''
    for row in reversed(pixels):  # bottom-up
        for pixel in row:
            pixel_data += struct.pack('<BBBB', pixel[0], pixel[1], pixel[2], pixel[3])
    
    # ICO 文件结构
    ico_path = os.path.join(os.path.dirname(__file__), 'media_scraper.ico')
    
    # ICO Header
    header = struct.pack('<HHH', 0, 1, 1)  # Reserved, Type=ICO, Count=1
    
    # Image Entry (16 bytes)
    bmp_size = 40 + len(pixel_data)  # BITMAPINFOHEADER + pixels
    entry = struct.pack('<BBBBHHII',
        width,      # Width
        height,     # Height  
        0,          # Color count
        0,          # Reserved
        1,          # Color planes
        32,         # Bits per pixel
        bmp_size,   # Size of image data
        22          # Offset to image data
    )
    
    # BITMAPINFOHEADER (40 bytes)
    bmp_header = struct.pack('<IIIHHIIIIII',
        40,             # Header size
        width,          # Width
        height * 2,     # Height (ICO需要双倍)
        1,              # Planes
        32,             # Bits per pixel
        0,              # Compression
        len(pixel_data),# Image size
        0, 0,           # X/Y resolution
        0, 0            # Colors
    )
    
    # AND mask (全部透明)
    and_mask_size = ((width + 31) // 32) * 4 * height
    and_mask = bytes(and_mask_size)
    
    # 写入文件
    with open(ico_path, 'wb') as f:
        f.write(header)
        f.write(entry)
        f.write(bmp_header)
        f.write(pixel_data)
        f.write(and_mask)
    
    print(f"✓ 图标已创建: {ico_path}")
    print(f"  尺寸: {width}x{height}")
    print(f"  颜色: 樱花粉色主题")
    return ico_path

if __name__ == '__main__':
    create_media_scraper_icon()
    input("\n按 Enter 键退出...")
