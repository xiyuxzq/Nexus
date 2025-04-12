#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Nexus基础插件类 - 所有插件应该继承这个类
"""

class BasePlugin:
    def __init__(self, config):
        """
        初始化插件
        
        Args:
            config: 插件配置信息，从plugin.json加载
        """
        self.config = config
        self.name = config.get("name", "未命名插件")
        self.version = config.get("version", "1.0.0")
        self.author = config.get("author", "未知作者")
        self.description = config.get("description", "")
        self.software = config.get("software", [])
        self.versions = config.get("software_versions", [])
        self.departments = config.get("departments", [])
        self.initialized = False
    
    def initialize(self):
        """
        初始化插件，加载所需资源，创建菜单等
        子类应该覆盖这个方法
        
        Returns:
            bool: 初始化是否成功
        """
        self.initialized = True
        return True
    
    def create_menu(self):
        """
        创建菜单项
        子类应该覆盖这个方法
        
        Returns:
            bool: 创建菜单是否成功
        """
        return True
    
    def unload(self):
        """
        卸载插件，清理资源，删除菜单等
        子类应该覆盖这个方法
        
        Returns:
            bool: 卸载是否成功
        """
        self.initialized = False
        return True
    
    def get_settings(self):
        """
        获取插件设置
        
        Returns:
            dict: 插件设置
        """
        return self.config.get("settings", {})
    
    def update_settings(self, settings):
        """
        更新插件设置
        
        Args:
            settings: 新的设置值
            
        Returns:
            bool: 更新是否成功
        """
        if "settings" not in self.config:
            self.config["settings"] = {}
        
        self.config["settings"].update(settings)
        return True
    
    def is_compatible(self, software, version, department):
        """
        检查插件是否与指定的软件环境兼容
        
        Args:
            software: 软件名称
            version: 软件版本
            department: 部门名称
            
        Returns:
            bool: 是否兼容
        """
        # 检查软件兼容性
        if self.software and software not in self.software:
            return False
        
        # 检查版本兼容性
        if self.versions and version not in self.versions:
            return False
        
        # 检查部门兼容性
        if self.departments and department not in self.departments:
            return False
        
        return True