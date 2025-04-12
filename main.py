#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Nexus - 3D软件环境管理和工具启动器
"""

import sys
import os
import yaml
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QObject

from core.config_manager import ConfigManager
from core.software_launcher import SoftwareLauncher
from core.plugin_manager import PluginManager

class NexusApp(QObject):
    def __init__(self):
        super().__init__()
        
        # 设置应用图标
        self.app_icon = QIcon("icons/nexus.ico")
        
        # 加载配置
        self.config_manager = ConfigManager()
        self.environments = self.config_manager.get_environments()
        
        # 创建插件管理器
        self.plugin_manager = PluginManager()
        
        # 创建启动器
        self.launcher = SoftwareLauncher()
        
        # 创建系统托盘图标
        self.tray_icon = QSystemTrayIcon(self.app_icon)
        self.tray_icon.setToolTip("Nexus 环境启动器")
        self.setup_tray_menu()
        self.tray_icon.show()
        
        # 显示启动通知
        self.tray_icon.showMessage(
            "Nexus",
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
            software_menu.setIcon(QIcon(f"icons/{software.lower()}.ico"))
            
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
            env_name = environment.get("name", "未知环境")
            self.tray_icon.showMessage(
                "Nexus",
                f"正在启动 {env_name}...",
                QSystemTrayIcon.Information,
                2000
            )
            
            self.launcher.launch(environment)
            print(f"启动环境: {env_name}")
        except Exception as e:
            error_msg = str(e)
            self.tray_icon.showMessage(
                "启动失败",
                error_msg,
                QSystemTrayIcon.Critical,
                3000
            )
            print(f"启动失败: {error_msg}")
    
    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(
            None,
            "关于 Nexus",
            "Nexus 环境启动器 v1.0.0\n\n"
            "一个用于管理3D软件环境和工具的应用\n"
            "© 2023 公司名称"
        )

def main():
    # 创建应用
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # 关闭窗口时不退出应用
    app.setApplicationName("Nexus")
    
    # 检查系统托盘是否可用
    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(
            None,
            "Nexus",
            "无法检测到系统托盘，程序无法启动。"
        )
        sys.exit(1)
    
    # 创建主应用
    nexus = NexusApp()
    
    # 运行应用
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()