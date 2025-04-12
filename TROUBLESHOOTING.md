# Nexus 故障排除指南

如果您在使用Nexus环境管理器时遇到问题，请参考以下故障排除步骤。

## 常见问题

### 1. run_nexus.bat双击后一闪而过

**可能原因**：
- Python未安装或未添加到PATH
- 缺少必要的Python包
- 文件路径或权限问题
- 程序启动过程中出错

**解决方法**：
1. 使用调试模式启动：双击`run_nexus_debug.bat`，它会显示更多诊断信息
2. 运行完整诊断：双击`run_full_diagnostic.bat`，它会检查所有系统要求并提供详细报告
3. 检查Python安装：确保已安装Python 3.6或更高版本，且已添加到PATH环境变量

### 2. 系统托盘图标不显示

**可能原因**：
- 图标文件缺失或损坏
- PyQt5安装有问题
- 程序启动过程中出错

**解决方法**：
1. 创建图标文件：运行`nexus_icon_creator.py`，它会在icons目录中创建必要的图标
2. 检查PyQt5安装：运行`diagnose_nexus.py`，确认PyQt5已正确安装
3. 检查错误日志：启动调试模式查看错误信息

### 3. 无法启动Maya

**可能原因**：
- Maya路径配置不正确
- Maya未安装
- 环境变量设置有问题

**解决方法**：
1. 配置Maya路径：运行`configure_maya.bat`，设置正确的Maya安装路径
2. 检查环境配置：确认`config/environments.yaml`中的Maya路径是否正确
3. 验证Maya安装：手动启动Maya，确认它可以正常工作

### 4. 启动后无法看到菜单

**可能原因**：
- 启动脚本有错误
- Maya启动路径不正确
- 脚本路径设置有问题

**解决方法**：
1. 检查启动脚本：确认`scripts/maya_character_startup.py`存在且没有语法错误
2. 验证脚本路径：确认环境变量中的MAYA_SCRIPT_PATH设置正确
3. 手动加载脚本：在Maya中手动执行脚本，查看错误信息

## 诊断工具

Nexus包含多个诊断工具，帮助您排查问题：

1. **diagnose_nexus.py** - 全面检查Nexus环境并诊断问题
2. **run_nexus_debug.bat** - 在调试模式下启动Nexus，显示详细错误信息
3. **run_full_diagnostic.bat** - 运行完整诊断流程，包括环境检查、图标创建和配置
4. **nexus_icon_creator.py** - 创建必要的图标文件
5. **maya_path_config.py** - 配置Maya路径的图形工具

## 获取帮助

如果您尝试上述方法后仍然遇到问题，请收集以下信息并联系技术支持：

1. 诊断日志（运行`diagnose_nexus.py`生成）
2. 调试日志（运行`run_nexus_debug.bat`生成，文件名为`nexus_debug_*.log`）
3. 您的操作系统版本
4. Python版本（运行`python --version`获取）
5. Maya版本和安装路径

## 解决方案检查清单

- [ ] Python 3.6+已安装且添加到PATH
- [ ] PyQt5已正确安装
- [ ] pyyaml和cryptography包已安装
- [ ] 图标文件存在于icons目录中
- [ ] Maya路径已正确配置
- [ ] 所有必要的目录和文件存在
- [ ] 启动脚本没有语法错误
- [ ] 系统的杀毒软件未阻止Nexus运行