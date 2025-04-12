@echo off
echo ============================================================
echo Nexus Environment Manager (Debug Mode)
echo ============================================================
echo.

rem 创建日志文件
set LOGFILE=nexus_debug_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%.log
set LOGFILE=%LOGFILE: =0%
echo Logging to: %LOGFILE%
echo Nexus Debug Log > %LOGFILE%
echo Time: %date% %time% >> %LOGFILE%
echo. >> %LOGFILE%

rem 设置环境变量
echo Setting environment variables...
set NEXUS_HOME=%~dp0
echo NEXUS_HOME set to: %NEXUS_HOME% >> %LOGFILE%

rem 检查Python安装
echo Checking Python installation...
python --version > temp.txt 2>&1
set /p PYTHON_VERSION=<temp.txt
del temp.txt
echo Python version: %PYTHON_VERSION% >> %LOGFILE%

if "%PYTHON_VERSION%"=="" (
    echo ERROR: Python not found. Please install Python and add it to your PATH.
    echo ERROR: Python not found >> %LOGFILE%
    pause
    exit /b 1
)

echo Python found: %PYTHON_VERSION%

rem 检查必要的包
echo Checking required packages...
echo.

echo Checking PyQt5...
python -c "import PyQt5; print('PyQt5 version:', PyQt5.QtCore.PYQT_VERSION_STR)" > temp.txt 2>&1
set /p PYQT_VERSION=<temp.txt
del temp.txt
echo %PYQT_VERSION% >> %LOGFILE%

if not "%PYQT_VERSION:error=%" == "%PYQT_VERSION%" (
    echo Installing PyQt5...
    python -m pip install PyQt5
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Failed to install PyQt5.
        echo ERROR: Failed to install PyQt5 >> %LOGFILE%
        pause
        exit /b 1
    )
) else (
    echo Found %PYQT_VERSION%
)

echo Checking PyYAML...
python -c "import yaml; print('PyYAML version:', yaml.__version__)" > temp.txt 2>&1
set /p YAML_VERSION=<temp.txt
del temp.txt
echo %YAML_VERSION% >> %LOGFILE%

if not "%YAML_VERSION:error=%" == "%YAML_VERSION%" (
    echo Installing PyYAML...
    python -m pip install pyyaml
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Failed to install PyYAML.
        echo ERROR: Failed to install PyYAML >> %LOGFILE%
        pause
        exit /b 1
    )
) else (
    echo Found %YAML_VERSION%
)

echo Checking cryptography...
python -c "import cryptography; print('Cryptography version:', cryptography.__version__)" > temp.txt 2>&1
set /p CRYPTO_VERSION=<temp.txt
del temp.txt
echo %CRYPTO_VERSION% >> %LOGFILE%

if not "%CRYPTO_VERSION:error=%" == "%CRYPTO_VERSION%" (
    echo Installing cryptography...
    python -m pip install cryptography
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Failed to install cryptography.
        echo ERROR: Failed to install cryptography >> %LOGFILE%
        pause
        exit /b 1
    )
) else (
    echo Found %CRYPTO_VERSION%
)

rem 检查文件
echo Checking required files...
echo.

echo Checking main.py...
if not exist "%NEXUS_HOME%main.py" (
    echo ERROR: main.py not found.
    echo ERROR: main.py not found >> %LOGFILE%
    pause
    exit /b 1
)
echo main.py found.

echo Checking config directory...
if not exist "%NEXUS_HOME%config" (
    echo ERROR: config directory not found.
    echo ERROR: config directory not found >> %LOGFILE%
    pause
    exit /b 1
)
echo config directory found.

echo Checking environments.yaml...
if not exist "%NEXUS_HOME%config\environments.yaml" (
    echo ERROR: environments.yaml not found.
    echo ERROR: environments.yaml not found >> %LOGFILE%
    pause
    exit /b 1
)
echo environments.yaml found.

echo Checking core modules...
if not exist "%NEXUS_HOME%core\config_manager.py" (
    echo ERROR: config_manager.py not found.
    echo ERROR: config_manager.py not found >> %LOGFILE%
    pause
    exit /b 1
)
if not exist "%NEXUS_HOME%core\software_launcher.py" (
    echo ERROR: software_launcher.py not found.
    echo ERROR: software_launcher.py not found >> %LOGFILE%
    pause
    exit /b 1
)
if not exist "%NEXUS_HOME%core\plugin_manager.py" (
    echo ERROR: plugin_manager.py not found.
    echo ERROR: plugin_manager.py not found >> %LOGFILE%
    pause
    exit /b 1
)
echo Core modules found.

echo All checks passed!
echo All checks passed! >> %LOGFILE%
echo. >> %LOGFILE%

rem 询问用户是否继续
echo.
echo ============================================================
echo All preliminary checks have passed. Do you want to:
echo 1. Run Nexus in console mode (shows errors)
echo 2. Run Nexus in normal mode (background)
echo 3. Exit without running
echo ============================================================
choice /c 123 /m "Choose an option (1-3): "

if %ERRORLEVEL% EQU 1 (
    echo Running Nexus in console mode...
    echo Running Nexus in console mode >> %LOGFILE%
    echo.
    echo NOTE: This window will remain open. If Nexus crashes, error messages will appear here.
    echo.
    echo ============================================================
    python "%NEXUS_HOME%main.py"
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Nexus exited with error code %ERRORLEVEL%
        echo ERROR: Nexus exited with error code %ERRORLEVEL% >> %LOGFILE%
        pause
        exit /b %ERRORLEVEL%
    )
) else if %ERRORLEVEL% EQU 2 (
    echo Running Nexus in normal mode...
    echo Running Nexus in normal mode >> %LOGFILE%
    start pythonw "%NEXUS_HOME%main.py"
) else (
    echo Exiting without running Nexus.
    echo User chose to exit without running Nexus >> %LOGFILE%
)

echo ============================================================
echo Debug session completed.
echo See %LOGFILE% for details.
echo ============================================================
pause