# Oh My XKit - PowerShell Framework
# Simple and functional version

$XKIT_VERSION = "2.1.0"
$OH_MY_XKIT = "$PSScriptRoot"

# Configuration
$XKIT_THEME = "powerlevel10k-xkit"
$XKIT_PLUGINS = @("git", "docker", "ai-assistant", "telegram-notifier")

# Load theme function
function Load-XKitTheme {
    param([string]$ThemeName = $XKIT_THEME)
    
    $themePath = "$OH_MY_XKIT\themes\$ThemeName.ps1"
    if (Test-Path $themePath) {
        . $themePath
    } else {
        Set-DefaultXKitPrompt
    }
}

# Load plugins function
function Load-XKitPlugins {
    foreach ($plugin in $XKIT_PLUGINS) {
        $pluginPath = "$OH_MY_XKIT\plugins\$plugin\$plugin.plugin.ps1"
        if (Test-Path $pluginPath) {
            . $pluginPath
        }
    }
}

# Default prompt
function Set-DefaultXKitPrompt {
    function global:prompt {
        $user = $env:USERNAME
        $computer = $env:COMPUTERNAME
        $location = (Get-Location).Path.Replace($HOME, '~')
        
        # Git branch
        $branch = ""
        try {
            $gitBranch = git rev-parse --abbrev-ref HEAD 2>$null
            if ($gitBranch -and $LASTEXITCODE -eq 0) {
                $branch = " [$gitBranch]"
            }
        } catch {}
        
        Write-Host "$user@$computer" -NoNewline -ForegroundColor Green
        if ($branch) { Write-Host $branch -NoNewline -ForegroundColor Yellow }
        Write-Host " ~$(Split-Path $location -Leaf)" -NoNewline -ForegroundColor Cyan
        Write-Host "`n$ " -NoNewline -ForegroundColor White
        return ""
    }
}

# Utility functions
function xkit-version { 
    Write-Host "Oh My XKit v$XKIT_VERSION" -ForegroundColor Green
}

function xkit-reload { 
    . $PROFILE
    Write-Host "Reloaded!" -ForegroundColor Green
}

function xkit-help {
    Write-Host "Oh My XKit v$XKIT_VERSION" -ForegroundColor Green
    Write-Host "Available commands:" -ForegroundColor Cyan
    Write-Host "  xkit-version  - Show version" -ForegroundColor White
    Write-Host "  xkit-reload   - Reload profile" -ForegroundColor White  
    Write-Host "  xkit-help     - Show this help" -ForegroundColor White
    Write-Host "Git commands: gst, ga, gc, gp, gl, gb, gco" -ForegroundColor Yellow
    Write-Host "Docker commands: d, dps, di, p, pps, pi" -ForegroundColor Yellow
    Write-Host "AI command: ai 'question'" -ForegroundColor Yellow
    Write-Host "Telegram: tg 'message'" -ForegroundColor Yellow
}

# Load theme and plugins automatically
Load-XKitTheme
Load-XKitPlugins

Write-Host "Oh My XKit v$XKIT_VERSION loaded!" -ForegroundColor Green