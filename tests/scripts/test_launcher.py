#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试启动脚本 - 模拟软件启动
"""

import os
import sys
import time
from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

def show_test_window(environment_name):
    """显示测试窗口，模拟软件启动"""
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = QMainWindow()
    window.setWindowTitle(f"Nexus 测试环境 - {environment_name}")
    window.resize(600, 400)
    
    # 创建中央控件
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    
    # 创建布局
    layout = QVBoxLayout(central_widget)
    
    # 添加标签
    label1 = QLabel(f"成功启动环境: {environment_name}")
    label1.setAlignment(Qt.AlignCenter)
    label1.setStyleSheet("font-size: 24px; margin-bottom: 20px;")
    
    label2 = QLabel("这是一个模拟的软件环境，用于测试Nexus启动器")
    label2.setAlignment(Qt.AlignCenter)
    label2.setStyleSheet("font-size: 16px; margin-bottom: 40px;")
    
    label3 = QLabel("环境变量:")
    label3.setStyleSheet("font-size: 14px; font-weight: bold;")
    
    # 显示环境变量
    env_text = ""
    for key, value in os.environ.items():
        if "NEXUS" in key or "MAYA" in key or "MAX" in key or "PATH" in key:
            env_text += f"{key} = {value}\n"
    
    env_label = QLabel(env_text)
    env_label.setStyleSheet("font-family: Consolas, monospace; font-size: 12px;")
    env_label.setAlignment(Qt.AlignLeft)
    env_label.setWordWrap(True)
    
    # 添加标签到布局
    layout.addWidget(label1)
    layout.addWidget(label2)
    layout.addWidget(label3)
    layout.addWidget(env_label)
    
    # 显示窗口
    window.show()
    
    return app.exec_()

if __name__ == "__main__":
    # 获取环境名称
    env_name = "测试环境"
    if len(sys.argv) > 1:
        env_name = sys.argv[1]
    
    # 显示测试窗口
    sys.exit(show_test_window(env_name))