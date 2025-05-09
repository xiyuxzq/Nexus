@echo off
echo Starting Nexus Environment Manager (Fixed Version)...
echo.

rem Set environment variables
set NEXUS_HOME=%~dp0
echo NEXUS_HOME set to: %NEXUS_HOME%

rem Check Python installation
echo Checking Python installation...
python --version > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python not found. Please install Python and add it to your PATH.
    pause
    exit /b 1
)

rem Install required packages
echo Installing required Python packages...
python -m pip install PyQt5 pyyaml cryptography

rem Create icon files
echo Creating icon files...
python "%NEXUS_HOME%nexus_icon_creator.py"

rem Run fixed version of Nexus
echo Launching Nexus (fixed version)...
python "%~dp0main_icon_fix.py"

rem Check for errors
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Nexus exited with error code: %ERRORLEVEL%
    echo.
    echo Please check the error messages above.
    echo If you need more detailed diagnostics, run run_full_diagnostic.bat
)

echo.
pause