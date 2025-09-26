# XKit v3.0 - Python-First Approach
# Minimal PowerShell Profile that delegates everything to Python

# Configure UTF-8 support for emojis FIRST
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

# Load the ultra-minimal Python-first system
$XKitPython = "$PSScriptRoot\xkit-minimal-python.ps1"
if (Test-Path $XKitPython) {
    Write-Host "🔄 Loading XKit Python-First Architecture..." -ForegroundColor Cyan
    . $XKitPython
    Write-Host "✅ All commands now delegate to Python backend!" -ForegroundColor Green
} else {
    Write-Host "❌ XKit Python-First system not found!" -ForegroundColor Red
    Write-Host "💡 Expected: $XKitPython" -ForegroundColor Cyan
    
    # Fallback attempt
    $XKitV3 = "$PSScriptRoot\xkit-v3.ps1"
    if (Test-Path $XKitV3) {
        Write-Host "🔄 Trying XKit v3.0..." -ForegroundColor Yellow
        . $XKitV3
    }
}

# Chocolatey Integration
$ChocolateyProfile = "$env:ChocolateyInstall\helpers\chocolateyProfile.psm1"
if (Test-Path($ChocolateyProfile)) {
    Import-Module "$ChocolateyProfile"
}

# Environment Variables
$env:GITLAB_TOKEN = 'glpat-CoOQ3_JxrX_kC7zEYiGfs286MQp1OjEH.01.0w1yvqqa3'
$env:GITLAB_URL = 'https://localhost'

# XKit v3.0 Configuration
$env:XKIT_VERSION = '3.0.0'
$env:XKIT_ARCHITECTURE = 'hybrid-mcp'
$env:GEMINI_API_KEY = 'AIzaSyCvzBo-iK-KBdwedZYSHyoHcMzsYqEArC4'
$env:TELEGRAM_TOKEN = '8477588651:AAGaQLuk7hsfW5UWiNEnpGWK2Z6rRLg9A-s'
$env:ADMIN_ID = '7335391186'

# Note: All XKit functions are loaded from xkit-minimal.ps1