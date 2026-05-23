<#
.SYNOPSIS
    Forza Horizon AFK auto-start helper.
.DESCRIPTION
    Requests Administrator privileges, installs required dependencies,
    and runs AFKgameEN.py from the same folder.
#>

# 1. Check and request Administrator privileges.
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "Requesting Administrator privileges..."
    # Relaunch this script with elevated permissions.
    Start-Process PowerShell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

# 2. Change to the script folder to avoid starting from System32 after elevation.
Set-Location -Path $PSScriptRoot

Write-Host "========================================"
Write-Host "Dependency check and startup"
Write-Host "========================================"

# 3. Check whether Python is installed.
if (-not (Get-Command "python" -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Python was not found." -ForegroundColor Red
    Write-Host "Please install Python and enable 'Add Python to PATH' during setup." -ForegroundColor Yellow
    Pause
    exit
}

# 4. Install or update the required Python package.
Write-Host "Checking and installing the vgamepad package..."
python -m pip install vgamepad --disable-pip-version-check | Out-Null

# 5. Confirm the main script exists, then run it.
$PythonScript = "AFKgameEN.py"

if (Test-Path $PythonScript) {
    Write-Host "Ready. Starting the controller script..." -ForegroundColor Green
    Write-Host "========================================"
    Write-Host ""

    python $PythonScript
} else {
    Write-Host "Error: script file [$PythonScript] was not found." -ForegroundColor Red
    Write-Host "Please make sure RunAFK.ps1 and $PythonScript are in the same folder." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "The controller script has stopped."
Pause
