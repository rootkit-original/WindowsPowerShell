# XKit v3.0 - Standardized Command Structure
# Minimal PowerShell Profile that loads the new xkit command

# Configure UTF-8 support for emojis FIRST
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

# Load the new standardized xkit command script
$XKitCommand = "$PSScriptRoot\xkit.ps1"
if (Test-Path $XKitCommand) {
    Write-Host "� Loading XKit v3.0 Standardized Command Structure..." -ForegroundColor Cyan
    
    # Create global xkit function that calls the script
    function global:xkit {
        param(
            [Parameter(Position=0, Mandatory=$true)]
            [string]$Command,
            
            [Parameter(Position=1, ValueFromRemainingArguments=$true)]
            [string[]]$Parameters = @()
        )
        
        & "$PSScriptRoot\xkit.ps1" $Command @Parameters
    }
    
    Write-Host "✅ XKit command structure loaded: xkit <command> <params>" -ForegroundColor Green
    Write-Host "💡 Try: xkit help" -ForegroundColor Yellow
} else {
    Write-Host "❌ XKit command script not found!" -ForegroundColor Red
    Write-Host "💡 Expected: $XKitCommand" -ForegroundColor Cyan
    
    # Fallback to Python-first system
    $XKitPython = "$PSScriptRoot\xkit-minimal-python.ps1"
    if (Test-Path $XKitPython) {
        Write-Host "🔄 Loading fallback Python-First system..." -ForegroundColor Yellow
        . $XKitPython
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
$env:GEMINI_API_KEY = 'AIzaSyBsjNVK3p544LLk_OL4IChy7OdApkhS7vA'
$env:TELEGRAM_TOKEN = '8477588651:AAGaQLuk7hsfW5UWiNEnpGWK2Z6rRLg9A-s'
$env:ADMIN_ID = '7335391186'

# Note: All XKit functions are loaded from xkit-minimal.ps1