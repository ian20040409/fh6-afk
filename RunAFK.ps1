<#
.SYNOPSIS
    Forza Horizon 掛機腳本自動啟動工具
.DESCRIPTION
    自動請求系統管理員權限，安裝依賴套件，並執行 AFKgame.py
#>

# 1. 檢查並自動請求系統管理員權限
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "正在請求系統管理員權限..."
    # 使用最高權限重新啟動此腳本，並繞過執行原則限制
    Start-Process PowerShell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

# 2. 將工作目錄切換至腳本所在位置 (避免系統管理員預設路徑為 System32)
Set-Location -Path $PSScriptRoot

Write-Host "========================================"
Write-Host "環境檢查與初始化"
Write-Host "========================================"

# 3. 檢查系統是否已安裝 Python
if (-not (Get-Command "python" -ErrorAction SilentlyContinue)) {
    Write-Host "錯誤：找不到 Python 執行檔。" -ForegroundColor Red
    Write-Host "請確認已安裝 Python，並在安裝時勾選「Add Python to PATH」。" -ForegroundColor Yellow
    Pause
    exit
}

# 4. 安裝或更新必備的 Python 套件
Write-Host "正在檢查並安裝 vgamepad 套件..."
python -m pip install vgamepad --disable-pip-version-check | Out-Null

# 5. 確認掛機腳本是否存在並執行
$PythonScript = "AFKgame.py"

if (Test-Path $PythonScript) {
    Write-Host "準備就緒，正在啟動掛機程式..." -ForegroundColor Green
    Write-Host "========================================"
    Write-Host ""
    
    # 執行 Python 腳本
    python $PythonScript
} else {
    Write-Host "錯誤：找不到腳本檔案 [$PythonScript]。" -ForegroundColor Red
    Write-Host "請確認 RunAFK.ps1 與 $PythonScript 放在同一個資料夾中。" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "掛機程式已結束。"
Pause