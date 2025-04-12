@echo off
echo ============================================================
echo Nexus Full Diagnostic Tool
echo ============================================================
echo.

rem 设置环境变量
set NEXUS_HOME=%~dp0
echo NEXUS_HOME set to: %NEXUS_HOME%

rem 检查Python安装
echo Checking Python installation...
python --version > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python not found. Please install Python and add it to your PATH.
    pause
    exit /b 1
)

echo Python found. Running diagnostic...
echo.

rem 运行诊断工具
python "%NEXUS_HOME%diagnose_nexus.py"

echo.
echo ============================================================
echo Diagnostic completed.
echo ============================================================

echo.
echo Would you like to:
echo 1. Create icon files
echo 2. Configure Maya paths
echo 3. Run Nexus in debug mode
echo 4. Exit
choice /c 1234 /m "Choose an option (1-4): "

if %ERRORLEVEL% EQU 1 (
    echo Creating icon files...
    python "%NEXUS_HOME%nexus_icon_creator.py"
    pause
) else if %ERRORLEVEL% EQU 2 (
    echo Running Maya path configuration...
    call "%NEXUS_HOME%configure_maya.bat"
) else if %ERRORLEVEL% EQU 3 (
    echo Running Nexus in debug mode...
    call "%NEXUS_HOME%run_nexus_debug.bat"
)

echo.
echo Thank you for using the Nexus Diagnostic Tool.
pause