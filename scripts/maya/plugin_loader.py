#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Nexus插件加载器 - 为Maya加载Nexus插件
"""

import os
import sys
import json
import maya.cmds as cmds
from maya import OpenMayaUI as omui

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from shiboken2 import wrapInstance
except ImportError:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
    from shiboken2 import wrapInstance

def maya_main_window():
    """获取Maya主窗口"""
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QWidget)

class PluginLoaderUI(QDialog):
    def __init__(self, parent=maya_main_window()):
        super(PluginLoaderUI, self).__init__(parent)
        
        # 获取Nexus主目录
        self.nexus_home = os.environ.get("NEXUS_HOME", os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        
        # 插件目录
        self.plugins_dir = os.path.join(self.nexus_home, "plugins", "maya")
        
        # 初始化UI
        self.setWindowTitle("Nexus插件加载器")
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)
        
        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        
        # 加载插件列表
        self.refresh_plugin_list()
    
    def create_widgets(self):
        """创建控件"""
        # 插件列表
        self.plugin_list = QTableWidget()
        self.plugin_list.setColumnCount(4)
        self.plugin_list.setHorizontalHeaderLabels(["名称", "版本", "作者", "状态"])
        self.plugin_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.plugin_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.plugin_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.plugin_list.verticalHeader().setVisible(False)
        self.plugin_list.horizontalHeader().setStretchLastSection(True)
        
        # 按钮
        self.load_button = QPushButton("加载插件")
        self.unload_button = QPushButton("卸载插件")
        self.refresh_button = QPushButton("刷新列表")
        self.install_button = QPushButton("安装插件")
        self.close_button = QPushButton("关闭")
        
        # 插件详情
        self.plugin_details = QTextEdit()
        self.plugin_details.setReadOnly(True)
    
    def create_layouts(self):
        """创建布局"""
        # 主布局
        main_layout = QVBoxLayout(self)
        
        # 插件列表区域
        list_group = QGroupBox("可用插件")
        list_layout = QVBoxLayout(list_group)
        list_layout.addWidget(self.plugin_list)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.unload_button)
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.install_button)
        button_layout.addWidget(self.close_button)
        
        # 详情区域
        details_group = QGroupBox("插件详情")
        details_layout = QVBoxLayout(details_group)
        details_layout.addWidget(self.plugin_details)
        
        # 添加到主布局
        main_layout.addWidget(list_group)
        main_layout.addWidget(details_group)
        main_layout.addLayout(button_layout)
    
    def create_connections(self):
        """创建信号连接"""
        self.plugin_list.itemSelectionChanged.connect(self.update_plugin_details)
        self.load_button.clicked.connect(self.load_plugin)
        self.unload_button.clicked.connect(self.unload_plugin)
        self.refresh_button.clicked.connect(self.refresh_plugin_list)
        self.install_button.clicked.connect(self.install_plugin)
        self.close_button.clicked.connect(self.close)
    
    def refresh_plugin_list(self):
        """刷新插件列表"""
        self.plugin_list.setRowCount(0)
        
        # 检查插件目录是否存在
        if not os.path.exists(self.plugins_dir):
            return
        
        # 扫描插件目录
        row = 0
        for plugin_dir in os.listdir(self.plugins_dir):
            plugin_path = os.path.join(self.plugins_dir, plugin_dir)
            
            # 检查是否是目录
            if not os.path.isdir(plugin_path):
                continue
            
            # 检查是否有plugin.json文件
            config_file = os.path.join(plugin_path, "plugin.json")
            if not os.path.exists(config_file):
                continue
            
            # 读取配置
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # 检查是否是Maya插件
                if "software" in config and "Maya" not in config["software"]:
                    continue
                
                # 添加到列表
                self.plugin_list.insertRow(row)
                
                # 设置单元格内容
                self.plugin_list.setItem(row, 0, QTableWidgetItem(config.get("name", plugin_dir)))
                self.plugin_list.setItem(row, 1, QTableWidgetItem(config.get("version", "1.0.0")))
                self.plugin_list.setItem(row, 2, QTableWidgetItem(config.get("author", "未知")))
                
                # 检查插件状态
                status = "未加载"
                try:
                    # 检查初始化模块是否已导入
                    entry_point = config.get("entry_point", "")
                    if entry_point:
                        module_path = entry_point.split(".")[0]
                        if module_path in sys.modules:
                            status = "已加载"
                except:
                    pass
                
                self.plugin_list.setItem(row, 3, QTableWidgetItem(status))
                
                # 存储插件路径和配置
                for col in range(4):
                    item = self.plugin_list.item(row, col)
                    item.setData(Qt.UserRole, {"path": plugin_path, "config": config})
                
                row += 1
            except Exception as e:
                cmds.warning(f"读取插件配置失败: {config_file}, 错误: {str(e)}")
        
        # 调整列宽
        self.plugin_list.resizeColumnsToContents()
    
    def update_plugin_details(self):
        """更新插件详情"""
        selected_items = self.plugin_list.selectedItems()
        if not selected_items:
            self.plugin_details.clear()
            return
        
        # 获取选中行的第一个单元格
        item = selected_items[0]
        data = item.data(Qt.UserRole)
        
        if not data:
            self.plugin_details.clear()
            return
        
        config = data["config"]
        
        # 构建详情文本
        details = f"<h2>{config.get('name', '未知插件')}</h2>"
        details += f"<p><b>版本:</b> {config.get('version', '1.0.0')}</p>"
        details += f"<p><b>作者:</b> {config.get('author', '未知')}</p>"
        details += f"<p><b>描述:</b> {config.get('description', '无描述')}</p>"
        
        # 软件兼容性
        software = config.get("software", [])
        versions = config.get("software_versions", [])
        if software:
            details += f"<p><b>支持软件:</b> {', '.join(software)}</p>"
        if versions:
            details += f"<p><b>支持版本:</b> {', '.join(versions)}</p>"
        
        # 部门兼容性
        departments = config.get("departments", [])
        if departments:
            details += f"<p><b>适用部门:</b> {', '.join(departments)}</p>"
        
        # 菜单项
        menu = config.get("menu", {})
        if menu:
            details += f"<h3>菜单项</h3>"
            items = menu.get("items", [])
            if items:
                details += "<ul>"
                for item in items:
                    details += f"<li>{item.get('name', '未命名')}</li>"
                details += "</ul>"
        
        # 设置详情文本
        self.plugin_details.setHtml(details)
    
    def load_plugin(self):
        """加载选中的插件"""
        selected_items = self.plugin_list.selectedItems()
        if not selected_items:
            cmds.warning("请先选择要加载的插件")
            return
        
        # 获取选中行的第一个单元格
        item = selected_items[0]
        data = item.data(Qt.UserRole)
        
        if not data:
            cmds.warning("无法获取插件信息")
            return
        
        config = data["config"]
        plugin_path = data["path"]
        
        # 检查插件入口点
        entry_point = config.get("entry_point", "")
        if not entry_point:
            cmds.warning(f"插件没有指定入口点: {config.get('name', '未知插件')}")
            return
        
        try:
            # 添加插件目录到Python路径
            if plugin_path not in sys.path:
                sys.path.insert(0, plugin_path)
            
            # 解析入口点
            if "." in entry_point:
                module_path, function_name = entry_point.rsplit(".", 1)
            else:
                module_path, function_name = "", entry_point
            
            # 导入模块
            if module_path:
                module = __import__(module_path, fromlist=[function_name])
                init_func = getattr(module, function_name)
            else:
                # 如果没有指定模块路径，尝试导入__init__.py
                init_file = os.path.join(plugin_path, "__init__.py")
                if not os.path.exists(init_file):
                    cmds.warning(f"找不到插件入口文件: {init_file}")
                    return
                
                # 使用exec加载模块
                module_name = os.path.basename(plugin_path)
                spec = importlib.util.spec_from_file_location(module_name, init_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                init_func = getattr(module, function_name)
            
            # 初始化插件
            plugin_instance = init_func(config)
            
            # 调用初始化方法
            if hasattr(plugin_instance, "initialize") and callable(plugin_instance.initialize):
                plugin_instance.initialize()
            
            # 更新状态
            for i in range(len(selected_items)):
                row = selected_items[i].row()
                self.plugin_list.item(row, 3).setText("已加载")
            
            # 显示成功消息
            cmds.inViewMessage(
                amg=f"插件 '{config.get('name', '未知插件')}' 已成功加载",
                pos="midCenter",
                fade=True,
                fadeOutTime=2.0
            )
        except Exception as e:
            cmds.warning(f"加载插件失败: {str(e)}")
    
    def unload_plugin(self):
        """卸载选中的插件"""
        selected_items = self.plugin_list.selectedItems()
        if not selected_items:
            cmds.warning("请先选择要卸载的插件")
            return
        
        # 获取选中行的第一个单元格
        item = selected_items[0]
        data = item.data(Qt.UserRole)
        
        if not data:
            cmds.warning("无法获取插件信息")
            return
        
        config = data["config"]
        plugin_path = data["path"]
        
        # 检查插件入口点
        entry_point = config.get("entry_point", "")
        if not entry_point:
            cmds.warning(f"插件没有指定入口点: {config.get('name', '未知插件')}")
            return
        
        try:
            # 解析入口点
            if "." in entry_point:
                module_path, function_name = entry_point.rsplit(".", 1)
            else:
                module_path, function_name = "", entry_point
            
            # 检查模块是否已加载
            if module_path in sys.modules:
                module = sys.modules[module_path]
                
                # 检查是否有插件实例
                if hasattr(module, "plugin_instance"):
                    plugin_instance = module.plugin_instance
                    
                    # 调用卸载方法
                    if hasattr(plugin_instance, "unload") and callable(plugin_instance.unload):
                        plugin_instance.unload()
                
                # 删除模块
                del sys.modules[module_path]
            
            # 更新状态
            for i in range(len(selected_items)):
                row = selected_items[i].row()
                self.plugin_list.item(row, 3).setText("未加载")
            
            # 显示成功消息
            cmds.inViewMessage(
                amg=f"插件 '{config.get('name', '未知插件')}' 已成功卸载",
                pos="midCenter",
                fade=True,
                fadeOutTime=2.0
            )
        except Exception as e:
            cmds.warning(f"卸载插件失败: {str(e)}")
    
    def install_plugin(self):
        """安装插件"""
        # 获取安装包路径
        file_path = cmds.fileDialog2(
            fileFilter="插件包 (*.zip);;所有文件 (*.*)",
            dialogStyle=2,
            caption="选择插件安装包",
            fileMode=1
        )
        
        if not file_path:
            return
        
        file_path = file_path[0]
        
        # 确认安装
        result = cmds.confirmDialog(
            title="安装插件",
            message=f"确定要安装插件: {os.path.basename(file_path)}?",
            button=["确定", "取消"],
            defaultButton="确定",
            cancelButton="取消",
            dismissString="取消"
        )
        
        if result != "确定":
            return
        
        try:
            # 创建临时目录
            temp_dir = os.path.join(tempfile.gettempdir(), "nexus_plugin_temp")
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            os.makedirs(temp_dir)
            
            # 解压插件包
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # 查找plugin.json文件
            plugin_json = None
            for root, dirs, files in os.walk(temp_dir):
                if "plugin.json" in files:
                    plugin_json = os.path.join(root, "plugin.json")
                    break
            
            if not plugin_json:
                cmds.warning("无效的插件包: 找不到plugin.json文件")
                return
            
            # 读取插件信息
            with open(plugin_json, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 检查是否是Maya插件
            if "software" in config and "Maya" not in config["software"]:
                cmds.warning(f"插件不兼容: 此插件不支持Maya")
                return
            
            # 获取插件ID或名称
            plugin_id = config.get("id", "").lower()
            if not plugin_id:
                plugin_id = config.get("name", "unknown").lower().replace(" ", "_")
            
            # 目标目录
            target_dir = os.path.join(self.plugins_dir, plugin_id)
            
            # 如果目标目录已存在，先备份
            if os.path.exists(target_dir):
                backup_dir = f"{target_dir}.bak.{int(time.time())}"
                shutil.move(target_dir, backup_dir)
            
            # 创建插件目录
            if not os.path.exists(self.plugins_dir):
                os.makedirs(self.plugins_dir)
            
            # 复制插件文件
            plugin_root = os.path.dirname(plugin_json)
            shutil.copytree(plugin_root, target_dir)
            
            # 刷新插件列表
            self.refresh_plugin_list()
            
            # 显示成功消息
            cmds.inViewMessage(
                amg=f"插件 '{config.get('name', plugin_id)}' 已成功安装",
                pos="midCenter",
                fade=True,
                fadeOutTime=2.0
            )
        except Exception as e:
            cmds.warning(f"安装插件失败: {str(e)}")

def show_ui():
    """显示插件加载器UI"""
    # 关闭已存在的窗口
    for widget in QApplication.allWidgets():
        if isinstance(widget, PluginLoaderUI):
            widget.close()
    
    # 创建并显示新窗口
    ui = PluginLoaderUI()
    ui.show()
    return ui

# 当脚本被直接执行时
if __name__ == "__main__":
    show_ui()