#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Maya角色部门启动脚本 - 为Maya配置角色制作环境
"""

import os
import sys
import maya.cmds as cmds
import maya.mel as mel

def setup_environment():
    """设置Maya环境变量和路径"""
    # 获取Nexus主目录
    nexus_home = os.environ.get("NEXUS_HOME", os.path.dirname(os.path.dirname(__file__)))
    
    # 添加脚本路径
    maya_scripts_path = os.path.join(nexus_home, "scripts", "maya")
    character_scripts_path = os.path.join(maya_scripts_path, "character")
    
    # 添加到Maya的Python路径
    if maya_scripts_path not in sys.path:
        sys.path.append(maya_scripts_path)
    if character_scripts_path not in sys.path:
        sys.path.append(character_scripts_path)
    
    print("已设置Maya角色环境")
    return True

def create_character_menu():
    """创建角色工具菜单"""
    # 如果菜单已存在，先删除
    if cmds.menu("nexusCharacterMenu", exists=True):
        cmds.deleteUI("nexusCharacterMenu")
    
    # 创建菜单
    gMainWindow = mel.eval('$temp = $gMainWindow')
    character_menu = cmds.menu("nexusCharacterMenu", label="角色工具", parent=gMainWindow, tearOff=True)
    
    # 添加菜单项
    cmds.menuItem(parent=character_menu, label="创建骨架", 
                 command="import character_rig_tools; character_rig_tools.create_skeleton()")
    
    cmds.menuItem(parent=character_menu, label="骨骼镜像", 
                 command="import character_rig_tools; character_rig_tools.mirror_skeleton()")
    
    cmds.menuItem(parent=character_menu, divider=True)
    
    cmds.menuItem(parent=character_menu, label="蒙皮工具", 
                 command="import character_skin_tools; character_skin_tools.skin_tools_ui()")
    
    cmds.menuItem(parent=character_menu, label="权重镜像", 
                 command="import character_skin_tools; character_skin_tools.mirror_weights()")
    
    cmds.menuItem(parent=character_menu, divider=True)
    
    cmds.menuItem(parent=character_menu, label="加载插件", 
                 command="import plugin_loader; plugin_loader.show_ui()")
    
    print("已创建角色工具菜单")
    return True

def load_character_plugins():
    """加载角色相关的Maya插件"""
    # 获取Nexus主目录
    nexus_home = os.environ.get("NEXUS_HOME", os.path.dirname(os.path.dirname(__file__)))
    
    # 插件目录
    plugins_dir = os.path.join(nexus_home, "plugins", "maya")
    
    # 设置插件路径
    if os.path.exists(plugins_dir):
        # 添加到Maya插件路径
        plugin_path = os.environ.get("MAYA_PLUG_IN_PATH", "")
        if plugins_dir not in plugin_path:
            os.environ["MAYA_PLUG_IN_PATH"] = plugins_dir + os.pathsep + plugin_path
    
    # 加载常用插件
    character_plugins = [
        "mgear_solvers.mll",  # 假设使用mgear作为绑定工具
        "matrixNodes.mll"     # 矩阵节点插件
    ]
    
    for plugin in character_plugins:
        try:
            if not cmds.pluginInfo(plugin, query=True, loaded=True):
                cmds.loadPlugin(plugin)
                print(f"已加载插件: {plugin}")
        except:
            print(f"警告: 无法加载插件 {plugin}")
    
    return True

def initialize():
    """初始化角色环境"""
    try:
        # 设置环境
        setup_environment()
        
        # 加载插件
        load_character_plugins()
        
        # 创建菜单
        create_character_menu()
        
        # 打印欢迎信息
        print("=" * 50)
        print("欢迎使用Nexus Maya角色环境")
        print("版本: 1.0.0")
        print("=" * 50)
        
        return True
    except Exception as e:
        print(f"初始化角色环境失败: {str(e)}")
        return False

# 当脚本被直接执行时调用初始化
if __name__ == "__main__":
    initialize()