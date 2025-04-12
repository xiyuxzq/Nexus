#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
配置管理器 - 负责加载和保存配置文件
"""

import os
import yaml
import json
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class ConfigManager:
    def __init__(self, config_path=None):
        # 设置配置路径
        self.config_path = config_path or os.path.join(os.path.dirname(os.path.dirname(__file__)), "config")
        self.environments_file = os.path.join(self.config_path, "environments.yaml")
        self.settings_file = os.path.join(self.config_path, "settings.yaml")
        self.users_file = os.path.join(self.config_path, "users.yaml")
        
        # 确保配置目录存在
        os.makedirs(self.config_path, exist_ok=True)
        
        # 初始化加密密钥
        self._init_encryption()
        
        # 加载配置
        self.environments = self._load_yaml(self.environments_file)
        self.settings = self._load_yaml(self.settings_file)
        self.users = self._load_yaml(self.users_file)
        
        # 如果配置文件不存在，创建默认配置
        if not self.environments:
            self._create_default_environments()
        
        if not self.settings:
            self._create_default_settings()
        
        if not self.users:
            self._create_default_users()
    
    def _init_encryption(self):
        """初始化加密功能"""
        # 使用固定的盐值，确保每次生成相同的密钥
        # 注意：在实际应用中，应该使用更安全的方式存储密钥
        salt = b'nexus_salt_value'
        password = b'nexus_secure_password'
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(password))
        self.cipher = Fernet(key)
    
    def _encrypt_data(self, data):
        """加密数据"""
        if isinstance(data, str):
            return self.cipher.encrypt(data.encode()).decode()
        return data
    
    def _decrypt_data(self, data):
        """解密数据"""
        if isinstance(data, str):
            try:
                return self.cipher.decrypt(data.encode()).decode()
            except:
                return data
        return data
    
    def _load_yaml(self, file_path, default=None):
        """加载YAML文件，如果文件不存在则返回默认值"""
        if default is None:
            default = {}
            
        if not os.path.exists(file_path):
            return default
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or default
        except Exception as e:
            print(f"加载配置文件失败: {file_path}, 错误: {str(e)}")
            return default
    
    def _save_yaml(self, data, file_path):
        """保存数据到YAML文件"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            return True
        except Exception as e:
            print(f"保存配置文件失败: {file_path}, 错误: {str(e)}")
            return False
    
    def _create_default_environments(self):
        """创建默认环境配置"""
        self.environments = [
            {
                "name": "Maya2019 Character",
                "software": "Maya",
                "version": "2019",
                "department": "Character",
                "executable_path": "C:/Program Files/Autodesk/Maya2019/bin/maya.exe",
                "startup_script": "scripts/maya_character_startup.py",
                "env_variables": {
                    "MAYA_SCRIPT_PATH": "${NEXUS_HOME}/scripts/maya",
                    "MAYA_PLUG_IN_PATH": "${NEXUS_HOME}/plugins/maya",
                    "PYTHONPATH": "${NEXUS_HOME}/scripts/maya;${PYTHONPATH}"
                },
                "menu_items": [
                    {
                        "name": "Character Tools",
                        "items": [
                            {
                                "name": "Rig Tool",
                                "script": "character/rig_tool.py"
                            },
                            {
                                "name": "Skin Tool",
                                "script": "character/skin_tool.py"
                            }
                        ]
                    }
                ]
            },
            {
                "name": "Max2019 Weapon",
                "software": "3dsMax",
                "version": "2019",
                "department": "Weapon",
                "executable_path": "C:/Program Files/Autodesk/3ds Max 2019/3dsmax.exe",
                "startup_script": "scripts/max_weapon_startup.ms",
                "env_variables": {
                    "MAX_SCRIPT_PATH": "${NEXUS_HOME}/scripts/max"
                },
                "menu_items": [
                    {
                        "name": "Weapon Tools",
                        "items": [
                            {
                                "name": "Model Tool",
                                "script": "weapon/model_tool.ms"
                            }
                        ]
                    }
                ]
            }
        ]
        self.save_environments()
    
    def _create_default_settings(self):
        """创建默认设置"""
        self.settings = {
            "auto_start": True,
            "check_updates": True,
            "update_url": "http://internal-server/nexus/updates",
            "plugin_repositories": [
                "http://internal-server/nexus/plugins"
            ],
            "log_level": "INFO"
        }
        self.save_settings()
    
    def _create_default_users(self):
        """创建默认用户配置"""
        # 管理员密码加密
        admin_password = self._encrypt_data("admin123")
        
        self.users = {
            "users": [
                {
                    "username": "admin",
                    "password": admin_password,
                    "role": "admin",
                    "departments": ["*"]
                },
                {
                    "username": "user",
                    "password": self._encrypt_data("user123"),
                    "role": "user",
                    "departments": ["Character", "Weapon"]
                }
            ]
        }
        self.save_users()
    
    def get_environments(self):
        """获取所有环境配置"""
        return self.environments
    
    def get_environment(self, name):
        """获取指定名称的环境配置"""
        for env in self.environments:
            if env.get("name") == name:
                return env
        return None
    
    def add_environment(self, environment):
        """添加新环境配置"""
        # 检查是否已存在同名环境
        for i, env in enumerate(self.environments):
            if env.get("name") == environment.get("name"):
                # 更新已存在的环境
                self.environments[i] = environment
                self.save_environments()
                return True
        
        # 添加新环境
        self.environments.append(environment)
        self.save_environments()
        return True
    
    def remove_environment(self, name):
        """删除指定名称的环境配置"""
        for i, env in enumerate(self.environments):
            if env.get("name") == name:
                del self.environments[i]
                self.save_environments()
                return True
        return False
    
    def save_environments(self):
        """保存环境配置"""
        return self._save_yaml(self.environments, self.environments_file)
    
    def get_setting(self, key, default=None):
        """获取设置项"""
        return self.settings.get(key, default)
    
    def set_setting(self, key, value):
        """设置设置项"""
        self.settings[key] = value
        return self.save_settings()
    
    def save_settings(self):
        """保存设置"""
        return self._save_yaml(self.settings, self.settings_file)
    
    def save_users(self):
        """保存用户配置"""
        return self._save_yaml(self.users, self.users_file)
    
    def authenticate_user(self, username, password):
        """验证用户登录"""
        users_list = self.users.get("users", [])
        for user in users_list:
            if user.get("username") == username:
                stored_password = user.get("password", "")
                decrypted_password = self._decrypt_data(stored_password)
                if decrypted_password == password:
                    return user
        return None
    
    def get_user_departments(self, username):
        """获取用户可访问的部门列表"""
        users_list = self.users.get("users", [])
        for user in users_list:
            if user.get("username") == username:
                departments = user.get("departments", [])
                if "*" in departments:
                    # 所有部门权限
                    return None  # None表示所有部门
                return departments
        return []  # 默认无权限