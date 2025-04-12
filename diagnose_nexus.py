#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Nexus诊断工具 - 检查Nexus环境并诊断问题
"""

import os
import sys
import platform
import time
import traceback

def print_header(title):
    """打印格式化的标题"""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)

def print_status(name, status, message=""):
    """打印状态信息"""
    if status:
        print(f"[✓] {name}: {message}")
    else:
        print(f"[✗] {name}: {message}")

def check_python():
    """检查Python环境"""
    print_header("Python环境检查")
    
    # Python版本
    py_version = platform.python_version()
    py_version_ok = int(py_version.split('.')[0]) >= 3
    print_status("Python版本", py_version_ok, py_version)
    
    # Python位数
    py_bits = "64-bit" if sys.maxsize > 2**32 else "32-bit"
    print_status("Python位数", True, py_bits)
    
    # Python路径
    py_path = sys.executable
    print_status("Python路径", os.path.exists(py_path), py_path)
    
    return py_version_ok

def check_packages():
    """检查必要的Python包"""
    print_header("Python包检查")
    all_ok = True
    
    # 检查PyQt5
    try:
        import PyQt5
        print_status("PyQt5", True, PyQt5.QtCore.PYQT_VERSION_STR)
    except ImportError:
        print_status("PyQt5", False, "未安装")
        all_ok = False
    except Exception as e:
        print_status("PyQt5", False, f"错误: {str(e)}")
        all_ok = False
    
    # 检查yaml
    try:
        import yaml
        print_status("PyYAML", True, yaml.__version__)
    except ImportError:
        print_status("PyYAML", False, "未安装")
        all_ok = False
    except Exception as e:
        print_status("PyYAML", False, f"错误: {str(e)}")
        all_ok = False
    
    # 检查cryptography
    try:
        import cryptography
        print_status("cryptography", True, cryptography.__version__)
    except ImportError:
        print_status("cryptography", False, "未安装")
        all_ok = False
    except Exception as e:
        print_status("cryptography", False, f"错误: {str(e)}")
        all_ok = False
    
    # 可选包: tkinter (用于配置工具)
    try:
        import tkinter
        print_status("tkinter (可选)", True, "已安装")
    except ImportError:
        print_status("tkinter (可选)", False, "未安装 (仅影响配置工具)")
    
    return all_ok

def check_nexus_files():
    """检查Nexus文件结构"""
    print_header("Nexus文件检查")
    all_ok = True
    
    # 获取Nexus主目录
    nexus_home = os.path.dirname(os.path.abspath(__file__))
    print_status("Nexus主目录", os.path.exists(nexus_home), nexus_home)
    
    # 检查主文件
    main_py = os.path.join(nexus_home, "main.py")
    main_ok = os.path.exists(main_py)
    print_status("main.py", main_ok, main_py)
    all_ok = all_ok and main_ok
    
    # 检查核心目录和文件
    core_dir = os.path.join(nexus_home, "core")
    core_dir_ok = os.path.exists(core_dir) and os.path.isdir(core_dir)
    print_status("core目录", core_dir_ok, core_dir)
    all_ok = all_ok and core_dir_ok
    
    if core_dir_ok:
        core_files = [
            "config_manager.py",
            "software_launcher.py",
            "plugin_manager.py"
        ]
        for file_name in core_files:
            file_path = os.path.join(core_dir, file_name)
            file_ok = os.path.exists(file_path)
            print_status(f"core/{file_name}", file_ok, file_path)
            all_ok = all_ok and file_ok
    
    # 检查配置目录和文件
    config_dir = os.path.join(nexus_home, "config")
    config_dir_ok = os.path.exists(config_dir) and os.path.isdir(config_dir)
    print_status("config目录", config_dir_ok, config_dir)
    all_ok = all_ok and config_dir_ok
    
    if config_dir_ok:
        config_files = [
            "environments.yaml",
            "settings.yaml"
        ]
        for file_name in config_files:
            file_path = os.path.join(config_dir, file_name)
            file_ok = os.path.exists(file_path)
            print_status(f"config/{file_name}", file_ok, file_path)
            all_ok = all_ok and file_ok
    
    # 检查脚本目录
    scripts_dir = os.path.join(nexus_home, "scripts")
    scripts_dir_ok = os.path.exists(scripts_dir) and os.path.isdir(scripts_dir)
    print_status("scripts目录", scripts_dir_ok, scripts_dir)
    all_ok = all_ok and scripts_dir_ok
    
    # 检查图标目录
    icons_dir = os.path.join(nexus_home, "icons")
    icons_dir_ok = os.path.exists(icons_dir) and os.path.isdir(icons_dir)
    print_status("icons目录", icons_dir_ok, icons_dir)
    all_ok = all_ok and icons_dir_ok
    
    return all_ok

def check_environment():
    """检查系统环境"""
    print_header("系统环境检查")
    
    # 操作系统
    os_name = platform.system()
    os_version = platform.version()
    print_status("操作系统", True, f"{os_name} {os_version}")
    
    # 检查PATH环境变量
    path = os.environ.get("PATH", "")
    print(f"PATH环境变量: {path[:100]}...")
    
    return True

def check_maya_installation():
    """检查Maya安装情况"""
    print_header("Maya检查")
    maya_found = False
    
    # 可能的Maya安装路径
    maya_paths = [
        r"C:\Program Files\Autodesk\Maya2019\bin\maya.exe",
        r"C:\Program Files\Autodesk\Maya2020\bin\maya.exe",
        r"C:\Program Files\Autodesk\Maya2022\bin\maya.exe",
        r"C:\Program Files\Autodesk\Maya2023\bin\maya.exe",
        r"C:\Autodesk\Maya2019\bin\maya.exe",
        r"C:\Autodesk\Maya2020\bin\maya.exe",
        r"C:\Autodesk\Maya2022\bin\maya.exe",
        r"C:\Autodesk\Maya2023\bin\maya.exe"
    ]
    
    for path in maya_paths:
        if os.path.exists(path):
            print_status(f"Maya", True, path)
            maya_found = True
    
    if not maya_found:
        print_status("Maya", False, "未找到Maya安装。如果已安装，请使用配置工具设置正确的路径。")
    
    # 检查环境配置
    nexus_home = os.path.dirname(os.path.abspath(__file__))
    env_file = os.path.join(nexus_home, "config", "environments.yaml")
    
    if os.path.exists(env_file):
        try:
            import yaml
            with open(env_file, 'r', encoding='utf-8') as f:
                environments = yaml.safe_load(f)
            
            # 检查Maya环境
            maya_envs = [env for env in environments if env.get("software") == "Maya"]
            if maya_envs:
                print(f"找到{len(maya_envs)}个Maya环境配置:")
                for env in maya_envs:
                    name = env.get("name", "未命名环境")
                    exe_path = env.get("executable_path", "未设置")
                    
                    path_exists = os.path.exists(exe_path)
                    print_status(f"  {name}", path_exists, exe_path)
            else:
                print_status("Maya环境配置", False, "未找到Maya环境配置")
        except Exception as e:
            print_status("读取环境配置", False, f"错误: {str(e)}")
    
    return maya_found

def test_qt():
    """测试PyQt5是否可以正常工作"""
    print_header("PyQt5测试")
    try:
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import QTimer
        
        app = QApplication([])
        timer = QTimer()
        timer.singleShot(100, app.quit)
        
        print_status("PyQt5初始化", True, "成功创建QApplication")
        print("开始测试PyQt事件循环... (这将持续几秒钟)")
        
        start_time = time.time()
        app.exec_()
        elapsed = time.time() - start_time
        
        print_status("PyQt5事件循环", True, f"成功完成，耗时: {elapsed:.2f}秒")
        return True
    except Exception as e:
        print_status("PyQt5测试", False, f"错误: {str(e)}")
        traceback.print_exc()
        return False

def fix_common_issues():
    """尝试修复常见问题"""
    print_header("修复常见问题")
    
    # 安装缺失的依赖
    try:
        import importlib.util
        for package in ["PyQt5", "pyyaml", "cryptography"]:
            spec = importlib.util.find_spec(package.lower())
            if spec is None:
                print(f"正在安装{package}...")
                import subprocess
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print_status(f"安装{package}", True, "安装成功")
            else:
                print_status(f"{package}", True, "已安装")
    except Exception as e:
        print_status("安装依赖", False, f"错误: {str(e)}")
    
    # 创建缺失的目录
    nexus_home = os.path.dirname(os.path.abspath(__file__))
    for dir_name in ["config", "core", "scripts", "icons", "plugins"]:
        dir_path = os.path.join(nexus_home, dir_name)
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path)
                print_status(f"创建目录 {dir_name}", True, dir_path)
            except Exception as e:
                print_status(f"创建目录 {dir_name}", False, f"错误: {str(e)}")

def run_diagnostics():
    """运行所有诊断检查"""
    print_header("Nexus诊断工具")
    print(f"时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"诊断脚本路径: {os.path.abspath(__file__)}")
    print("")
    
    # 运行所有检查
    python_ok = check_python()
    packages_ok = check_packages()
    files_ok = check_nexus_files()
    env_ok = check_environment()
    maya_ok = check_maya_installation()
    qt_ok = test_qt()
    
    # 总结结果
    print_header("诊断结果")
    print_status("Python环境", python_ok)
    print_status("Python包", packages_ok)
    print_status("Nexus文件", files_ok)
    print_status("系统环境", env_ok)
    print_status("Maya安装", maya_ok)
    print_status("PyQt5测试", qt_ok)
    
    # 总体结果
    overall_ok = python_ok and packages_ok and files_ok and qt_ok
    print("")
    if overall_ok:
        print("✓ 诊断通过! Nexus应该可以正常工作。")
        if not maya_ok:
            print("⚠ 警告: 未检测到Maya安装，请使用配置工具设置正确的Maya路径。")
    else:
        print("✗ 诊断发现问题! 请查看上面的详细信息。")
        print("")
        
        # 询问是否尝试修复
        try:
            response = input("是否尝试修复常见问题? (y/n): ")
            if response.lower() == 'y':
                fix_common_issues()
                print("\n修复完成。请重新运行诊断工具检查问题是否已解决。")
        except:
            pass

if __name__ == "__main__":
    try:
        run_diagnostics()
    except Exception as e:
        print(f"\n诊断工具遇到错误: {str(e)}")
        print("\n详细错误信息:")
        traceback.print_exc()
    
    input("\n按Enter键退出...")