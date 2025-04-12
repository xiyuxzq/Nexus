@echo off
echo Starting Nexus Environment Manager...

rem Set environment variables
set NEXUS_HOME=%~dp0
echo NEXUS_HOME set to: %NEXUS_HOME%

rem Check Python installation
python --version > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python not found. Please install Python and add it to your PATH.
    pause
    exit /b 1
)

rem Install required packages
python -m pip install PyQt5 pyyaml cryptography > nul 2>&1

rem Run Nexus
echo Launching Nexus...
start pythonw "%~dp0main.py"