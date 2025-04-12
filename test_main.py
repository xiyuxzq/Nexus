#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Nexus测试版本 - 3D软件环境管理和工具启动器
"""

import sys
import os
import yaml
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from PyQt5.QtCore import QObject, Qt

class SimpleConfigManager:
    """简化的配置管理器"""
    def __init__(self, config_path):
        self.config_path = config_path
        self.environments_file = os.path.join(self.config_path, "test_environments.yaml")
        self.environments = self._load_yaml(self.environments_file, [])
        
    def _load_yaml(self, file_path, default=None):
        """加载YAML文件，如果文件不存在则返回默认值"""
        if not os.path.exists(file_path):
            return default
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or default
        except Exception as e:
            print(f"加载配置文件失败: {file_path}, 错误: {str(e)}")
            return default
    
    def get_environments(self):
        """获取所有环境配置"""
        return self.environments

class SimpleLauncher:
    """简化的软件启动器"""
    def __init__(self):
        self.nexus_home = os.path.dirname(os.path.abspath(__file__))
    
    def _resolve_path(self, path):
        """解析路径中的变量"""
        if not path:
            return path
            
        # 替换环境变量
        path = os.path.expandvars(path)
        
        # 替换Nexus特殊变量
        path = path.replace("${NEXUS_HOME}", self.nexus_home)
        
        # 替换Python路径
        python_exe = sys.executable
        path = path.replace("${PYTHON_PATH}", python_exe)
        
        return path
    
    def launch(self, environment):
        """启动指定环境的软件"""
        import subprocess
        
        # 获取可执行文件路径
        executable = environment.get("executable_path")
        if not executable:
            raise ValueError("缺少软件可执行文件路径")
        
        executable = self._resolve_path(executable)
        
        # 处理启动脚本
        cmd_args = []
        startup_script = environment.get("startup_script")
        
        if startup_script:
            script_path = os.path.join(self.nexus_home, startup_script)
            script_path = self._resolve_path(script_path)
            
            if os.path.exists(script_path):
                cmd_args.append(script_path)
        
        # 添加命令行参数
        if "command_args" in environment:
            cmd_args.extend(environment["command_args"])
        
        # 设置环境变量
        env = os.environ.copy()
        for key, value in environment.get("env_variables", {}).items():
            env[key] = value
        
        # 构建完整的启动命令
        cmd = [executable] + cmd_args
        
        try:
            # 启动软件
            process = subprocess.Popen(cmd, env=env)
            print(f"已启动软件: {environment.get('name')}")
            print(f"命令: {' '.join(cmd)}")
            
            return process
        except Exception as e:
            raise RuntimeError(f"启动软件失败: {str(e)}")

class NexusTestApp(QObject):
    def __init__(self):
        super().__init__()
        
        # 设置应用图标
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons", "nexus.ico")
        if not os.path.exists(icon_path):
            # 如果图标不存在，使用备用的文本文件
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons", "nexus.ico.txt")
            print(f"警告: 未找到图标文件，使用备用文本文件: {icon_path}")
            # 创建临时图标
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
        
        # 加载配置
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config")
        self.config_manager = SimpleConfigManager(config_path)
        self.environments = self.config_manager.get_environments()
        
        # 创建启动器
        self.launcher = SimpleLauncher()
        
        # 创建系统托盘图标
        self.tray_icon = QSystemTrayIcon(self.app_icon)
        self.tray_icon.setToolTip("Nexus 测试版")
        self.setup_tray_menu()
        self.tray_icon.show()
        
        # 显示启动通知
        self.tray_icon.showMessage(
            "Nexus 测试版",
            "环境启动器测试版已启动，右键点击图标选择要启动的环境",
            QSystemTrayIcon.Information,
            3000
        )
    
    def setup_tray_menu(self):
        """设置托盘图标的右键菜单"""
        menu = QMenu()
        
        # 添加环境启动选项
        for env in self.environments:
            env_name = env.get("name", "未知环境")
            env_action = QAction(env_name, self)
            env_action.triggered.connect(lambda checked, e=env: self.launch_environment(e))
            menu.addAction(env_action)
        
        # 添加分隔线和退出选项
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
                "Nexus 测试版",
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
            "关于 Nexus 测试版",
            "Nexus 环境启动器 测试版 v0.1.0\n\n"
            "用于测试系统托盘和环境启动功能的简化版本\n"
            "© 2023 Nexus Team"
        )

def main():
    # 创建应用
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # 关闭窗口时不退出应用
    app.setApplicationName("Nexus Test")
    
    # 检查系统托盘是否可用
    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(
            None,
            "Nexus 测试版",
            "无法检测到系统托盘，程序无法启动。"
        )
        sys.exit(1)
    
    # 创建主应用
    nexus = NexusTestApp()
    
    # 运行应用
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()