#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
插件管理器 - 负责加载和管理插件
"""

import os
import sys
import json
import importlib.util
import shutil
import zipfile
import tempfile
import requests
from urllib.parse import urlparse
from PyQt5.QtCore import QObject, pyqtSignal

class PluginManager(QObject):
    # 信号
    plugin_loaded = pyqtSignal(str)  # 插件加载成功
    plugin_unloaded = pyqtSignal(str)  # 插件卸载成功
    plugin_error = pyqtSignal(str, str)  # 插件错误 (plugin_id, error_message)
    
    def __init__(self, plugins_dir=None):
        super().__init__()
        self.plugins_dir = plugins_dir or os.path.join(os.path.dirname(os.path.dirname(__file__)), "plugins")
        self.plugins = {}  # 存储插件信息: plugin_id -> {config, path}
        self.loaded_plugins = {}  # 存储已加载的插件实例: plugin_id -> instance
        
        # 确保插件目录存在
        os.makedirs(self.plugins_dir, exist_ok=True)
        
        # 扫描插件
        self.scan_plugins()
    
    def scan_plugins(self):
        """扫描所有可用插件"""
        self.plugins = {}
        
        for root, dirs, files in os.walk(self.plugins_dir):
            if "plugin.json" in files:
                plugin_config_path = os.path.join(root, "plugin.json")
                try:
                    with open(plugin_config_path, 'r', encoding='utf-8') as f:
                        plugin_config = json.load(f)
                    
                    # 生成插件ID: 相对于插件目录的路径
                    plugin_id = os.path.relpath(root, self.plugins_dir).replace('\\', '/')
                    
                    # 添加插件信息
                    self.plugins[plugin_id] = {
                        "config": plugin_config,
                        "path": root,
                        "active": True  # 默认启用
                    }
                    
                    # 可选: 检查是否有禁用标记文件
                    if os.path.exists(os.path.join(root, "disabled")):
                        self.plugins[plugin_id]["active"] = False
                    
                except Exception as e:
                    print(f"加载插件配置失败: {plugin_config_path}, 错误: {str(e)}")
        
        return len(self.plugins)
    
    def get_all_plugins(self):
        """获取所有插件信息"""
        result = []
        for plugin_id, info in self.plugins.items():
            plugin_info = info["config"].copy()
            plugin_info["id"] = plugin_id
            plugin_info["path"] = info["path"]
            plugin_info["active"] = info["active"]
            plugin_info["loaded"] = plugin_id in self.loaded_plugins
            result.append(plugin_info)
        return result
    
    def get_plugin_info(self, plugin_id):
        """获取特定插件的信息"""
        if plugin_id not in self.plugins:
            return None
        
        info = self.plugins[plugin_id]
        result = info["config"].copy()
        result["id"] = plugin_id
        result["path"] = info["path"]
        result["active"] = info["active"]
        result["loaded"] = plugin_id in self.loaded_plugins
        return result
    
    def get_compatible_plugins(self, software, version, department):
        """获取与指定环境兼容的插件"""
        compatible_plugins = []
        
        for plugin_id, plugin_info in self.plugins.items():
            if not plugin_info["active"]:
                continue
                
            config = plugin_info["config"]
            
            # 检查兼容性
            softwares = config.get("software", [])
            versions = config.get("software_versions", [])
            departments = config.get("departments", [])
            
            if (not softwares or software in softwares) and \
               (not versions or version in versions) and \
               (not departments or department in departments):
                compatible_plugins.append(plugin_id)
        
        return compatible_plugins
    
    def load_plugin(self, plugin_id, reload=False):
        """加载指定插件"""
        # 如果已加载且不是强制重新加载，则直接返回
        if plugin_id in self.loaded_plugins and not reload:
            return self.loaded_plugins[plugin_id]
        
        # 如果需要重新加载，先卸载
        if plugin_id in self.loaded_plugins:
            self.unload_plugin(plugin_id)
        
        if plugin_id not in self.plugins:
            error_msg = f"插件不存在: {plugin_id}"
            self.plugin_error.emit(plugin_id, error_msg)
            raise ValueError(error_msg)
        
        plugin_info = self.plugins[plugin_id]
        
        # 检查插件是否启用
        if not plugin_info["active"]:
            error_msg = f"插件已禁用: {plugin_id}"
            self.plugin_error.emit(plugin_id, error_msg)
            raise ValueError(error_msg)
        
        plugin_path = plugin_info["path"]
        config = plugin_info["config"]
        
        # 获取入口点
        entry_point = config.get("entry_point", "")
        if not entry_point:
            error_msg = f"插件没有指定入口点: {plugin_id}"
            self.plugin_error.emit(plugin_id, error_msg)
            raise ValueError(error_msg)
        
        # 解析入口点，格式为: "module.submodule.function"
        try:
            if "." in entry_point:
                module_path, function_name = entry_point.rsplit(".", 1)
            else:
                module_path, function_name = "", entry_point
            
            # 将插件目录添加到系统路径
            if plugin_path not in sys.path:
                sys.path.insert(0, plugin_path)
            
            # 导入插件模块
            if module_path:
                # 如果是相对导入，处理模块路径
                if module_path.startswith("."):
                    base_module = os.path.basename(plugin_path)
                    module_path = f"{base_module}{module_path}"
                
                module = importlib.import_module(module_path)
            else:
                # 如果没有指定模块路径，尝试导入__init__.py
                module_spec = importlib.util.spec_from_file_location(
                    "__init__", os.path.join(plugin_path, "__init__.py"))
                module = importlib.util.module_from_spec(module_spec)
                module_spec.loader.exec_module(module)
            
            # 获取初始化函数
            init_func = getattr(module, function_name)
            
            # 初始化插件
            plugin_instance = init_func(config)
            self.loaded_plugins[plugin_id] = plugin_instance
            
            # 发送信号
            self.plugin_loaded.emit(plugin_id)
            
            return plugin_instance
            
        except Exception as e:
            error_msg = f"加载插件失败: {plugin_id}, 错误: {str(e)}"
            self.plugin_error.emit(plugin_id, error_msg)
            raise ImportError(error_msg)
    
    def unload_plugin(self, plugin_id):
        """卸载指定插件"""
        if plugin_id in self.loaded_plugins:
            try:
                plugin = self.loaded_plugins[plugin_id]
                # 调用插件的卸载方法（如果存在）
                if hasattr(plugin, "unload") and callable(plugin.unload):
                    plugin.unload()
                
                # 从已加载插件中移除
                del self.loaded_plugins[plugin_id]
                
                # 发送信号
                self.plugin_unloaded.emit(plugin_id)
                
                return True
            except Exception as e:
                error_msg = f"卸载插件失败: {plugin_id}, 错误: {str(e)}"
                self.plugin_error.emit(plugin_id, error_msg)
                raise Exception(error_msg)
        
        return False
    
    def enable_plugin(self, plugin_id):
        """启用插件"""
        if plugin_id in self.plugins:
            # 更新状态
            self.plugins[plugin_id]["active"] = True
            
            # 删除禁用标记文件
            disabled_file = os.path.join(self.plugins[plugin_id]["path"], "disabled")
            if os.path.exists(disabled_file):
                os.remove(disabled_file)
            
            return True
        return False
    
    def disable_plugin(self, plugin_id):
        """禁用插件"""
        if plugin_id in self.plugins:
            # 如果已加载，先卸载
            if plugin_id in self.loaded_plugins:
                self.unload_plugin(plugin_id)
            
            # 更新状态
            self.plugins[plugin_id]["active"] = False
            
            # 创建禁用标记文件
            with open(os.path.join(self.plugins[plugin_id]["path"], "disabled"), 'w') as f:
                f.write("Plugin disabled")
            
            return True
        return False
    
    def install_plugin(self, plugin_package_path):
        """安装插件包（ZIP文件）"""
        # 检查文件是否存在
        if not os.path.exists(plugin_package_path):
            raise FileNotFoundError(f"插件包不存在: {plugin_package_path}")
        
        # 检查是否是ZIP文件
        if not zipfile.is_zipfile(plugin_package_path):
            raise ValueError(f"插件包不是有效的ZIP文件: {plugin_package_path}")
        
        # 创建临时目录解压插件
        with tempfile.TemporaryDirectory() as temp_dir:
            # 解压插件包
            with zipfile.ZipFile(plugin_package_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # 查找plugin.json文件
            plugin_json_path = None
            for root, _, files in os.walk(temp_dir):
                if "plugin.json" in files:
                    plugin_json_path = os.path.join(root, "plugin.json")
                    break
            
            if not plugin_json_path:
                raise ValueError(f"插件包中未找到plugin.json文件")
            
            # 读取插件配置
            with open(plugin_json_path, 'r', encoding='utf-8') as f:
                plugin_config = json.load(f)
            
            # 获取插件ID
            plugin_id = plugin_config.get("id")
            if not plugin_id:
                # 如果没有指定ID，使用插件名称作为ID
                plugin_id = plugin_config.get("name", "unknown").lower().replace(" ", "_")
            
            # 确定目标目录
            target_dir = os.path.join(self.plugins_dir, plugin_id)
            
            # 如果目标目录已存在，先备份
            if os.path.exists(target_dir):
                backup_dir = f"{target_dir}.bak"
                # 删除旧的备份
                if os.path.exists(backup_dir):
                    shutil.rmtree(backup_dir)
                # 备份当前版本
                shutil.move(target_dir, backup_dir)
            
            # 拷贝插件文件到目标目录
            plugin_root = os.path.dirname(plugin_json_path)
            shutil.copytree(plugin_root, target_dir)
            
            # 重新扫描插件
            self.scan_plugins()
            
            return plugin_id
    
    def download_plugin(self, url, target_path=None):
        """从URL下载插件"""
        # 解析URL获取文件名
        if not target_path:
            filename = os.path.basename(urlparse(url).path)
            if not filename.lower().endswith('.zip'):
                filename += '.zip'
            target_path = os.path.join(tempfile.gettempdir(), filename)
        
        # 下载文件
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(target_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return target_path
            
        except Exception as e:
            raise Exception(f"下载插件失败: {str(e)}")
    
    def update_plugin(self, plugin_id, plugin_package_path):
        """更新插件"""
        # 如果插件已加载，先卸载
        if plugin_id in self.loaded_plugins:
            self.unload_plugin(plugin_id)
        
        # 安装新版本（会覆盖旧版本）
        return self.install_plugin(plugin_package_path)
    
    def remove_plugin(self, plugin_id):
        """删除插件"""
        if plugin_id not in self.plugins:
            raise ValueError(f"插件不存在: {plugin_id}")
        
        # 如果插件已加载，先卸载
        if plugin_id in self.loaded_plugins:
            self.unload_plugin(plugin_id)
        
        # 删除插件目录
        plugin_path = self.plugins[plugin_id]["path"]
        if os.path.exists(plugin_path):
            shutil.rmtree(plugin_path)
        
        # 从插件列表中移除
        del self.plugins[plugin_id]
        
        return True