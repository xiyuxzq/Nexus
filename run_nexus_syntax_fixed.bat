@echo off
echo ============================================================
echo Nexus Environment Manager (Syntax Error Fixed)
echo ============================================================
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

rem Check icon file
echo.
echo Checking icon files...
if not exist "%NEXUS_HOME%icons\nexus.ico" (
    if not exist "%NEXUS_HOME%icons\nexus.png" (
        echo Icon file not found, creating placeholder...
        
        rem Create a simple text file as placeholder
        echo This is a placeholder for the icon file. > "%NEXUS_HOME%icons\nexus.ico.txt"
    ) else (
        echo Found PNG icon file.
    )
) else (
    echo Found ICO icon file.
)

rem Run Nexus
echo.
echo Launching Nexus...
echo ============================================================
python "%~dp0main.py"

rem Check for errors
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Nexus exited with error code: %ERRORLEVEL%
    echo.
    echo If you need more detailed diagnostics, run run_full_diagnostic.bat
)

echo.
echo ============================================================
echo Press any key to exit...
pause > nul