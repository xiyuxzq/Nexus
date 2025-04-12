@echo off
echo Starting Nexus Test Version...
echo.

rem Check Python installation
where python > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python not found. Please install Python and add it to your PATH.
    pause
    exit /b 1
)

rem Install required packages
echo Installing required Python packages...
python -m pip install PyQt5 pyyaml

rem Set environment variables
set NEXUS_HOME=%~dp0
echo NEXUS_HOME set to: %NEXUS_HOME%
echo.

echo Launching Nexus Test Version...
python "%~dp0test_main.py"

if %ERRORLEVEL% NEQ 0 (
    echo Launch failed with error code: %ERRORLEVEL%
    pause
)