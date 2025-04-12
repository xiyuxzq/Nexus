# Nexus - 3D软件环境管理和工具启动器

Nexus是一个用于管理3D软件环境和工具的应用程序。它允许用户通过系统托盘图标快速启动不同环境配置的3D软件，并为每个环境加载相应的工具和插件。

## 功能特点

- 通过系统托盘图标快速访问
- 支持多种3D软件（Maya, 3ds Max等）
- 环境配置管理
- 可扩展的插件系统
- 适用于内外网环境

## 测试版本

本目录包含一个简化的测试版本，用于验证核心功能：

1. 系统托盘图标显示
2. 右键菜单弹出
3. 模拟软件启动

### 如何运行测试版本

1. 确保已安装Python（3.6+）和以下依赖包：
   - PyQt5
   - pyyaml

2. 运行测试版本：
   - 双击 `run_test.bat` 批处理文件
   - 或者在命令行中运行 `python test_main.py`

3. 测试操作：
   - 观察任务栏右下角是否出现Nexus图标
   - 右键点击图标，选择测试环境
   - 验证是否打开了模拟软件窗口

### 测试环境说明

测试版本包含两个虚拟环境用于测试：

- **测试环境1**：基本测试环境
- **测试环境2**：开发部门测试环境

这些环境会启动一个简单的窗口来模拟实际软件，并显示环境变量信息。

## 完整版功能

完整版Nexus将包含以下功能：

- 完整的环境配置管理
- 内外网同步机制
- 可扩展的插件系统
- 用户认证和权限管理
- 自动更新功能
- 插件商店

## 关于代码安全

Nexus设计考虑了代码安全性，可以通过以下方式保护代码：

1. 使用PyInstaller将Python代码编译为可执行文件
2. 配置文件加密存储
3. 插件加密机制
4. 用户权限管理

## 项目开发与维护

Nexus是一个持续开发的项目，欢迎贡献和反馈。