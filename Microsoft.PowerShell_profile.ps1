# XKit - Ultra-Minimal PowerShell Profile
# Version 2.1.0 - Python-First Architecture

# Configure UTF-8 support for emojis FIRST
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

# Load XKit minimal framework
$XKitMinimal = "$PSScriptRoot\xkit-minimal.ps1"
if (Test-Path $XKitMinimal) {
    . $XKitMinimal
} else {
    Write-Host "ERROR: XKit minimal framework not found!" -ForegroundColor Red
    Write-Host "Expected: $XKitMinimal" -ForegroundColor Yellow
}

# Chocolatey Integration
$ChocolateyProfile = "$env:ChocolateyInstall\helpers\chocolateyProfile.psm1"
if (Test-Path($ChocolateyProfile)) {
    Import-Module "$ChocolateyProfile"
}

# Environment Variables
$env:GITLAB_TOKEN = 'glpat-CoOQ3_JxrX_kC7zEYiGfs286MQp1OjEH.01.0w1yvqqa3'
$env:GITLAB_URL = 'https://localhost'

# XKit v2.1 AI & Telegram Configuration  
$env:GEMINI_API_KEY = 'AIzaSyCvzBo-iK-KBdwedZYSHyoHcMzsYqEArC4'
$env:TELEGRAM_TOKEN = '8477588651:AAGaQLuk7hsfW5UWiNEnpGWK2Z6rRLg9A-s'
$env:ADMIN_ID = '7335391186'

# Note: All XKit functions are loaded from xkit-minimal.ps1