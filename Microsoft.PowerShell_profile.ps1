# XKit v3.0 - Hybrid MCP Architecture PowerShell Profile
# Ultra-Minimal Profile with Automatic Loading

# Configure UTF-8 support for emojis FIRST
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

# Load XKit v3.0 Hybrid MCP Architecture
$XKitV3 = "$PSScriptRoot\xkit-v3.ps1"
if (Test-Path $XKitV3) {
    Write-Host "🔄 Loading XKit v3.0 Hybrid MCP Architecture..." -ForegroundColor Cyan
    . $XKitV3
    Write-Host "✅ XKit v3.0 loaded successfully!" -ForegroundColor Green
} else {
    # Fallback to legacy system
    Write-Host "⚠️  XKit v3.0 not found, trying legacy..." -ForegroundColor Yellow
    $XKitMinimal = "$PSScriptRoot\xkit-minimal.ps1"
    if (Test-Path $XKitMinimal) {
        . $XKitMinimal
        Write-Host "🔄 Running XKit in legacy mode" -ForegroundColor Yellow
    } else {
        Write-Host "❌ No XKit system found!" -ForegroundColor Red
        Write-Host "💡 Expected: $XKitV3" -ForegroundColor Cyan
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