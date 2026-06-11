@echo off
REM Canonical Pure SSZ Metric - Windows Installation Script
REM © 2025 Carmen Wrede & Lino Casu
REM Licensed under the Anti-Capitalist Software License v1.4

echo ================================================================
echo Canonical Pure SSZ Metric Installer (Windows)
echo v1.1.0-canonical-pure - Research Framework
echo ================================================================

SET DEV_MODE=false
SET TEST_MODE=false
SET RESET_VENV=false

:parse_args
if "%~1"=="" goto done_args
if "%~1"=="--dev" set DEV_MODE=true
if "%~1"=="--test" set TEST_MODE=true
if "%~1"=="--reset-venv" set RESET_VENV=true
shift
goto parse_args
:done_args

REM Check Python version
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python >= 3.9 from https://python.org
    echo INSTALL: FAILED
    exit /b 1
)

python -c "import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)"
if errorlevel 1 (
    echo ERROR: Python version >= 3.9 is required.
    echo INSTALL: FAILED
    exit /b 1
)

if "%RESET_VENV%"=="true" (
    echo Resetting virtual environment...
    echo Are you sure you want to delete .venv? (Ctrl+C to cancel)
    pause
    if exist ".venv" (
        rmdir /s /q ".venv"
    )
)

if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        echo INSTALL: FAILED
        exit /b 1
    )
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    echo INSTALL: FAILED
    exit /b 1
)

echo Upgrading pip...
python -m pip install --upgrade pip --quiet

if "%DEV_MODE%"=="true" (
    echo Installing package in developer mode...
    python -m pip install -e ".[dev,viz]"
) else (
    echo Installing package in production mode...
    python -m pip install -e .
)

if "%TEST_MODE%"=="true" (
    echo Running tests...
    python -m pytest -q
    if errorlevel 1 (
        echo ERROR: Tests failed.
        echo INSTALL: FAILED
        exit /b 1
    )
    echo Tests passed!
)

echo ================================================================
echo INSTALL: PASS
echo ================================================================
