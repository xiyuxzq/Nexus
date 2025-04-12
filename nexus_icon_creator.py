#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Nexus图标创建工具 - 创建简单的图标文件
"""

import os
import sys
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont, QImage
from PyQt5.QtCore import Qt, QSize

def create_icon_file(output_path, text="N", size=64, bg_color="#0078D7", text_color="#FFFFFF"):
    """创建一个简单的图标文件"""
    # 创建pixmap
    pixmap = QPixmap(size, size)
    pixmap.fill(QColor(bg_color))
    
    # 绘制文本
    painter = QPainter(pixmap)
    painter.setPen(QColor(text_color))
    font = QFont("Arial", int(size * 0.6), QFont.Bold)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), Qt.AlignCenter, text)
    painter.end()
    
    # 保存为png
    pixmap.save(output_path)
    
    print(f"图标已保存至: {output_path}")
    return output_path

def create_nexus_icons():
    """创建Nexus所需的各种图标"""
    # 获取Nexus主目录
    nexus_home = os.path.dirname(os.path.abspath(__file__))
    icons_dir = os.path.join(nexus_home, "icons")
    
    # 确保图标目录存在
    if not os.path.exists(icons_dir):
        os.makedirs(icons_dir)
    
    # 创建Nexus主图标
    nexus_icon = os.path.join(icons_dir, "nexus.png")
    create_icon_file(nexus_icon, "N", 64, "#0078D7", "#FFFFFF")
    
    # 创建Maya图标
    maya_icon = os.path.join(icons_dir, "maya.png")
    create_icon_file(maya_icon, "M", 64, "#21A37C", "#FFFFFF")
    
    # 创建3dsMax图标
    max_icon = os.path.join(icons_dir, "3dsmax.png")
    create_icon_file(max_icon, "3", 64, "#061B49", "#FFFFFF")
    
    print(f"所有图标已创建完成。")
    return [nexus_icon, maya_icon, max_icon]

if __name__ == "__main__":
    try:
        created_icons = create_nexus_icons()
        
        print("\n图标创建成功!")
        print("由于Windows需要.ico格式图标，请考虑将.png转换为.ico格式:")
        print("1. 使用在线转换工具 (如https://convertico.com/)")
        print("2. 使用图像编辑软件 (如Photoshop或GIMP)")
        print("3. 使用Python的PIL/Pillow库转换")
    
    except Exception as e:
        print(f"创建图标时出错: {str(e)}")
    
    input("\n按Enter键退出...")