#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Nexus - 3D软件环境管理和工具启动器
修复版: 添加图标备用方案
"""

import sys
import os
import yaml
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from PyQt5.QtCore import QObject, Qt

try:
    from core.config_manager import ConfigManager
    from core.software_launcher import SoftwareLauncher
    from core.plugin_manager import PluginManager
except ImportError as e:
    print(f"错误: 无法导入核心模块: {str(e)}")
    print("请确保core目录存在且包含所有必要的模块文件。")
    sys.exit(1)

class NexusApp(QObject):
    def __init__(self):
        super().__init__()
        
        # 设置应用图标（添加备用方案）
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons", "nexus.ico")
        if not os.path.exists(icon_path):
            # 检查是否有PNG格式图标
            png_icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons", "nexus.png")
            if os.path.exists(png_icon_path):
                print(f"使用PNG图标: {png_icon_path}")
                self.app_icon = QIcon(png_icon_path)
            else:
                # 如果图标不存在，创建临时图标
                print(f"警告: 未找到图标文件，创建临时图标")
                pixmap = QPixmap(64, 64)
                pixmap.fill(QColor(0, 120, 215))
                painter = QPainter(pixmap)
                painter.setPen(QColor(255, 255, 255))
                painter.setFont(QFont("Arial", 20, QFont.Bold))
                painter.drawText(pixmap.rect(), Qt.AlignCenter, "N")
                painter.end()
                self.app_icon = QIcon(pixmap)
        else:
            self.app_icon = QIcon(icon_path)
        
        try:
            # 加载配置
            print("加载配置...")
            self.config_manager = ConfigManager()
            self.environments = self.config_manager.get_environments()
            
            # 创建插件管理器
            print("初始化插件管理器...")
            self.plugin_manager = PluginManager()
            
            # 创建启动器
            print("初始化软件启动器...")
            self.launcher = SoftwareLauncher()
            
            # 创建系统托盘图标
            print("创建系统托盘图标...")
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
        except Exception as e:
            print(f"初始化过程中出错: {str(e)}")
            QMessageBox.critical(
                None,
                "Nexus - 初始化错误",
                f"启动Nexus时出错:\n\n{str(e)}\n\n请检查配置文件和依赖项。"
            )
            raise
    
    def setup_tray_menu(self):
        """设置托盘图标的右键菜单"""
        try:
            menu = QMenu()
            
            # 检查是否有环境配置
            if not self.environments:
                no_env_action = QAction("未找到环境配置", self)
                no_env_action.setEnabled(False)
                menu.addAction(no_env_action)
                
                menu.addSeparator()
            else:
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
                    
                    # 尝试设置图标，如果失败则忽略
                    try:
                        icon_path = f"icons/{software.lower()}.ico"
                        if os.path.exists(icon_path):
                            software_menu.setIcon(QIcon(icon_path))
                        else:
                            # 检查PNG格式
                            png_path = f"icons/{software.lower()}.png"
                            if os.path.exists(png_path):
                                software_menu.setIcon(QIcon(png_path))
                    except:
                        pass
                    
                    # 添加该软件下的环境
                    for env in envs:
                        env_name = env.get("name", "未知环境")
                        env_action = QAction(env_name, self)
                        # Lambda中使用default参数确保正确捕获env变量
                        env_action.triggered.connect(lambda checked, e=env: self.launch_environment(e))
                        software_menu.addAction(env_action)
                    
                    menu.addMenu(software_menu)
                
                menu.addSeparator()
            
            # 配置选项
            config_action = QAction("配置...", self)
            config_action.triggered.connect(self.show_config)
            menu.addAction(config_action)
            
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
        except Exception as e:
            print(f"创建菜单时出错: {str(e)}")
            raise
    
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
            QMessageBox.warning(
                None,
                "启动失败",
                f"启动环境 '{env_name}' 失败:\n\n{error_msg}"
            )
    
    def show_config(self):
        """显示配置对话框"""
        try:
            # 尝试运行配置工具
            import subprocess
            config_bat = os.path.join(os.path.dirname(os.path.abspath(__file__)), "configure_maya.bat")
            if os.path.exists(config_bat):
                subprocess.Popen(config_bat)
            else:
                config_py = os.path.join(os.path.dirname(os.path.abspath(__file__)), "maya_path_config.py")
                if os.path.exists(config_py):
                    subprocess.Popen([sys.executable, config_py])
                else:
                    QMessageBox.warning(
                        None,
                        "配置工具",
                        "无法找到配置工具。"
                    )
        except Exception as e:
            QMessageBox.warning(
                None,
                "配置工具",
                f"启动配置工具时出错:\n\n{str(e)}"
            )
    
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
    try:
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
        print("初始化Nexus应用...")
        nexus = NexusApp()
        
        # 运行应用
        print("启动应用事件循环...")
        sys.exit(app.exec_())
    except Exception as e:
        print(f"程序启动失败: {str(e)}")
        if QApplication.instance():
            QMessageBox.critical(
                None,
                "Nexus - 严重错误",
                f"程序启动失败:\n\n{str(e)}"
            )
        sys.exit(1)

if __name__ == "__main__":
    main()