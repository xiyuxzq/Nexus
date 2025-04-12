#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
软件启动器 - 负责启动不同的软件环境
"""

import os
import sys
import subprocess
import tempfile
import platform
import re

class SoftwareLauncher:
    def __init__(self):
        self.nexus_home = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    def _resolve_path(self, path):
        """解析路径中的变量"""
        if not path:
            return path
            
        # 替换环境变量
        path = os.path.expandvars(path)
        
        # 替换Nexus特殊变量
        path = path.replace("${NEXUS_HOME}", self.nexus_home)
        
        return path
    
    def _expand_env_vars(self, env_vars):
        """展开环境变量中的占位符"""
        if not env_vars:
            return {}
            
        result = {}
        for key, value in env_vars.items():
            result[key] = self._resolve_path(value)
        
        return result
    
    def launch(self, environment):
        """启动指定环境的软件"""
        # 获取软件可执行文件路径
        executable = environment.get("executable_path")
        if not executable:
            raise ValueError("缺少软件可执行文件路径")
        
        executable = self._resolve_path(executable)
        
        if not os.path.exists(executable):
            raise FileNotFoundError(f"软件可执行文件不存在: {executable}")
        
        # 获取环境变量
        env_variables = environment.get("env_variables", {})
        env = os.environ.copy()
        
        # 添加环境变量
        expanded_env_vars = self._expand_env_vars(env_variables)
        for key, value in expanded_env_vars.items():
            # 处理PATH类环境变量，需要追加而不是覆盖
            if key.upper() in ["PATH", "PYTHONPATH", "MAYA_SCRIPT_PATH", "MAYA_PLUG_IN_PATH"]:
                current_value = env.get(key, "")
                if current_value:
                    # 确保使用正确的路径分隔符
                    separator = ";" if platform.system() == "Windows" else ":"
                    if value not in current_value.split(separator):
                        env[key] = value + separator + current_value
                    else:
                        env[key] = current_value
                else:
                    env[key] = value
            else:
                env[key] = value
        
        # 处理启动脚本
        cmd_args = []
        startup_script = environment.get("startup_script")
        
        if startup_script:
            script_path = os.path.join(self.nexus_home, startup_script)
            script_path = self._resolve_path(script_path)
            
            if os.path.exists(script_path):
                # 根据软件类型处理启动脚本
                software = environment.get("software", "").lower()
                
                if software == "maya":
                    # 创建一个临时的Python脚本，用于加载主启动脚本
                    # 这样可以更灵活地设置环境和加载插件
                    with tempfile.NamedTemporaryFile(suffix='.py', delete=False, mode='w') as temp:
                        temp.write(f"""
import os
import sys

# 添加 Nexus 路径到 Python 路径
nexus_home = r"{self.nexus_home}"
if nexus_home not in sys.path:
    sys.path.append(nexus_home)

# 加载主启动脚本
startup_script = r"{script_path}"
exec(compile(open(startup_script, 'rb').read(), startup_script, 'exec'))
""")
                        temp_path = temp.name
                    
                    # Maya使用Python启动脚本
                    # 在Windows上路径需要特殊处理
                    maya_script_path = temp_path.replace('\\', '/')
                    cmd_args.extend(["-command", f"python(\"execfile('{maya_script_path}')\")"])
                
                elif software == "3dsmax":
                    # 3ds Max使用MAXScript文件启动
                    cmd_args.extend(["-U", "MAXScript", script_path])
                
                elif software == "houdini":
                    # Houdini可以直接使用-run参数运行Python脚本
                    cmd_args.extend(["-run", script_path])
                
                elif software == "blender":
                    # Blender使用--python参数运行Python脚本
                    cmd_args.extend(["--python", script_path])
        
        # 构建完整的启动命令
        cmd = [executable] + cmd_args
        
        try:
            # 启动软件
            process = subprocess.Popen(cmd, env=env)
            
            # 记录启动信息
            print(f"已启动软件: {environment.get('name')}")
            print(f"命令: {' '.join(cmd)}")
            
            return process
        except Exception as e:
            raise RuntimeError(f"启动软件失败: {str(e)}")
    
    def is_software_running(self, executable_name):
        """检查指定的软件是否已在运行"""
        if platform.system() == "Windows":
            import wmi
            try:
                c = wmi.WMI()
                for process in c.Win32_Process():
                    if executable_name.lower() in process.Name.lower():
                        return True
                return False
            except:
                # 如果WMI不可用，使用tasklist命令
                try:
                    output = subprocess.check_output(["tasklist", "/FI", f"IMAGENAME eq {executable_name}"])
                    return executable_name.lower() in output.decode().lower()
                except:
                    return False
        else:
            # Linux/Mac
            try:
                output = subprocess.check_output(["ps", "-A"])
                return executable_name.lower() in output.decode().lower()
            except:
                return False