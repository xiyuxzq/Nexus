@echo off
echo 启动Nexus测试版...
echo.

rem 获取Python路径
where python > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo 错误: 未找到Python，请确保已安装Python并添加到PATH环境变量中。
    pause
    exit /b 1
)

rem 安装必要的包
echo 正在检查并安装必要的Python包...
pip install PyQt5 pyyaml

rem 设置环境变量
set NEXUS_HOME=%~dp0..
echo NEXUS_HOME设置为: %NEXUS_HOME%
echo.

echo 启动Nexus测试版...
python "%~dp0test_main.py"

if %ERRORLEVEL% NEQ 0 (
    echo 启动失败，错误代码: %ERRORLEVEL%
    pause
)