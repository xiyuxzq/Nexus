#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Nexus Mini - 软件环境启动器（最小测试版本）
"""

import os
import sys
import subprocess
import platform
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QObject

class NexusMini(QObject):
    def __init__(self):
        super().__init__()
        
        # 获取应用目录
        self.app_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 预定义环境配置（在实际应用中，这些应该从配置文件加载）
        self.environments = [
            {
                "name": "Maya2019 [角色]",
                "software": "Maya",
                "department": "Character",
                "executable_path": "C:/Program Files/Autodesk/Maya2019/bin/maya.exe",
                "env_variables": {
                    "MAYA_SCRIPT_PATH": os.path.join(self.app_dir, "scripts/maya").replace("\\", "/"),
                }
            },
            {
                "name": "Maya2019 [武器]",
                "software": "Maya",
                "department": "Weapon",
                "executable_path": "C:/Program Files/Autodesk/Maya2019/bin/maya.exe",
                "env_variables": {
                    "MAYA_SCRIPT_PATH": os.path.join(self.app_dir, "scripts/maya").replace("\\", "/"),
                }
            },
            {
                "name": "3ds Max2019 [武器]",
                "software": "3dsMax",
                "department": "Weapon",
                "executable_path": "C:/Program Files/Autodesk/3ds Max 2019/3dsmax.exe",
                "env_variables": {
                    "MAX_SCRIPT_PATH": os.path.join(self.app_dir, "scripts/max").replace("\\", "/"),
                }
            }
        ]
        
        # 创建系统托盘图标
        self.setup_tray_icon()
    
    def setup_tray_icon(self):
        """设置系统托盘图标和菜单"""
        # 尝试加载图标文件，如果不存在则使用Qt内置图标
        icon_path = os.path.join(self.app_dir, "icons/nexus.ico")
        if os.path.exists(icon_path):
            self.app_icon = QIcon(icon_path)
        else:
            # 使用Qt内置的应用图标
            self.app_icon = QIcon.fromTheme("applications-system")
            # 如果系统没有提供主题图标，使用内置的信息图标
            if self.app_icon.isNull():
                self.app_icon = QApplication.style().standardIcon(QApplication.style().SP_ComputerIcon)
        
        # 创建系统托盘图标
        self.tray_icon = QSystemTrayIcon(self.app_icon)
        self.tray_icon.setToolTip("Nexus 环境启动器")
        
        # 创建右键菜单
        self.setup_tray_menu()
        
        # 显示图标
        self.tray_icon.show()
        
        # 显示启动通知
        self.tray_icon.showMessage(
            "Nexus Mini",
            "环境启动器已启动，右键点击图标选择要启动的环境",
            QSystemTrayIcon.Information,
            3000
        )
    
    def setup_tray_menu(self):
        """设置托盘图标的右键菜单"""
        menu = QMenu()
        
        # 按软件类型分组显示环境
        software_groups = {}
        for env in self.environments:
            software = env.get("software", "其他")
            if software not in software_groups:
                software_groups[software] = []
            software_groups[software].append(env)
        
        # 添加环境启动选项（按软件分组）
        for software, envs in software_groups.items():
            # 添加软件类型子菜单
            software_menu = QMenu(software, menu)
            
            # 添加该软件下的环境
            for env in envs:
                env_name = env.get("name", "未知环境")
                env_action = QAction(env_name, self)
                env_action.triggered.connect(lambda checked, e=env: self.launch_environment(e))
                software_menu.addAction(env_action)
            
            menu.addMenu(software_menu)
        
        # 添加分隔线和其他选项
        menu.addSeparator()
        
        # 关于选项
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about)
        menu.addAction(about_action)
        
        # 退出选项
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(QApplication.quit)
        menu.addAction(exit_action)
        
        # 设置菜单
        self.tray_icon.setContextMenu(menu)
    
    def launch_environment(self, environment):
        """启动指定环境的软件"""
        try:
            # 获取软件信息
            env_name = environment.get("name", "未知环境")
            executable = environment.get("executable_path")
            
            # 检查软件可执行文件是否存在
            if not executable or not os.path.exists(executable):
                self.tray_icon.showMessage(
                    "错误",
                    f"找不到软件: {executable}\n请检查配置中的路径是否正确。",
                    QSystemTrayIcon.Critical,
                    5000
                )
                return
            
            # 显示启动通知
            self.tray_icon.showMessage(
                "Nexus Mini",
                f"正在启动 {env_name}...",
                QSystemTrayIcon.Information,
                2000
            )
            
            # 设置环境变量
            env = os.environ.copy()
            for key, value in environment.get("env_variables", {}).items():
                env[key] = value
            
            # 启动软件
            subprocess.Popen([executable], env=env)
            
            print(f"已启动环境: {env_name}")
            
        except Exception as e:
            error_msg = str(e)
            self.tray_icon.showMessage(
                "启动失败",
                error_msg,
                QSystemTrayIcon.Critical,
                5000
            )
            print(f"启动失败: {error_msg}")
    
    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(
            None,
            "关于 Nexus Mini",
            "Nexus 环境启动器 (迷你版) v0.1.0\n\n"
            "一个用于启动不同软件环境的简单工具\n"
            "© 2023"
        )

def main():
    # 创建应用
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # 关闭窗口时不退出应用
    app.setApplicationName("Nexus Mini")
    
    # 检查系统托盘是否可用
    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(
            None,
            "Nexus Mini",
            "无法检测到系统托盘，程序无法启动。"
        )
        sys.exit(1)
    
    # 创建并运行Nexus Mini
    nexus_mini = NexusMini()
    
    # 运行应用
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()