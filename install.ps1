# Canonical Pure SSZ Metric - Windows PowerShell Installation Script
# © 2025 Carmen Wrede & Lino Casu
# Licensed under the Anti-Capitalist Software License v1.4

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "Canonical Pure SSZ Metric Installer (PowerShell)" -ForegroundColor Cyan
Write-Host "v1.1.0-canonical-pure - Research Framework" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

$devMode = $false
$testMode = $false
$resetVenv = $false

foreach ($arg in $args) {
    if ($arg -eq "--dev") { $devMode = $true }
    if ($arg -eq "--test") { $testMode = $true }
    if ($arg -eq "--reset-venv") { $resetVenv = $true }
}

# Check Python version
try {
    $pythonVersion = python --version 2>&1
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python >= 3.9 from https://python.org" -ForegroundColor Yellow
    Write-Host "INSTALL: FAILED" -ForegroundColor Red
    exit 1
}

# Verify >= 3.9
$versionCheck = python -c "import sys; print(1 if sys.version_info >= (3, 9) else 0)"
if ($versionCheck -ne "1") {
    Write-Host "ERROR: Python >= 3.9 is required." -ForegroundColor Red
    Write-Host "INSTALL: FAILED" -ForegroundColor Red
    exit 1
}

Write-Host "Using Python: $pythonVersion" -ForegroundColor Green

if ($resetVenv -eq $true) {
    Write-Host "Resetting virtual environment..." -ForegroundColor Yellow
    Write-Host "Are you sure you want to delete .venv? (Press Enter to continue, Ctrl+C to cancel)" -ForegroundColor Yellow
    [void][System.Console]::ReadLine()
    if (Test-Path ".venv") {
        Remove-Item -Recurse -Force ".venv"
    }
}

if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
        Write-Host "INSTALL: FAILED" -ForegroundColor Red
        exit 1
    }
}

Write-Host "Activating virtual environment..." -ForegroundColor Yellow
if (Test-Path ".venv\\Scripts\\Activate.ps1") {
    . .venv\\Scripts\\Activate.ps1
} else {
    Write-Host "ERROR: Failed to find Activation script" -ForegroundColor Red
    Write-Host "INSTALL: FAILED" -ForegroundColor Red
    exit 1
}

Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet

if ($devMode -eq $true) {
    Write-Host "Installing package in developer mode..." -ForegroundColor Yellow
    python -m pip install -e ".[dev,viz]"
} else {
    Write-Host "Installing package in production mode..." -ForegroundColor Yellow
    python -m pip install -e .
}

if ($testMode -eq $true) {
    Write-Host "Running tests..." -ForegroundColor Yellow
    python -m pytest -q
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Tests failed." -ForegroundColor Red
        Write-Host "INSTALL: FAILED" -ForegroundColor Red
        exit 1
    }
    Write-Host "Tests passed!" -ForegroundColor Green
}

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "INSTALL: PASS" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Cyan
