# Oh My XKit - PowerShell Framework
# Configuration-based version with absolute paths

# Use global configuration or fallback
$XKIT_VERSION = $global:XKIT_VERSION ?? "2.1.0"
$OH_MY_XKIT = $global:XKIT_OH_MY_XKIT ?? "$PSScriptRoot"

# Configuration
$XKIT_THEME = $global:XKIT_THEME ?? "powerlevel10k-xkit"
$XKIT_PLUGINS = $global:XKIT_PLUGIN_LIST ?? @("git", "docker", "ai-assistant", "telegram-notifier", "error-handler-simple", "command-wrapper")

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
        # Try structured plugin first
        $pluginPath = "$OH_MY_XKIT\plugins\$plugin\$plugin.plugin.ps1"
        if (Test-Path $pluginPath) {
            . $pluginPath
        } else {
            # Try simple plugin file
            $simplePluginPath = "$OH_MY_XKIT\plugins\$plugin.ps1"
            if (Test-Path $simplePluginPath) {
                . $simplePluginPath
            }
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

function global:xkit-version { 
    Write-Host "`n[XKIT] Oh My XKit v$XKIT_VERSION" -ForegroundColor Green
    Write-Host "   Enhanced PowerShell Framework" -ForegroundColor Cyan
    Write-Host "   Location: $OH_MY_XKIT" -ForegroundColor Yellow
    Write-Host "   Theme: $XKIT_THEME" -ForegroundColor Magenta
    Write-Host "   Plugins: $($XKIT_PLUGINS -join ', ')" -ForegroundColor Blue
    Write-Host ""
}

function global:xkit-reload { 
    Write-Host "[RELOAD] Reloading Oh My XKit..." -ForegroundColor Yellow
    . "$OH_MY_XKIT\oh-my-xkit.ps1"
}

function global:xkit-help {
    if (Get-Command "Invoke-XKitPython" -ErrorAction SilentlyContinue) {
        Invoke-XKitPython "show-help"
    } else {
        Write-Host "❌ XKit configuration not loaded properly" -ForegroundColor Red
        Write-Host "💡 Try reloading your profile: . $PROFILE" -ForegroundColor Yellow
    }
}

# Load theme and plugins automatically
Load-XKitTheme
Load-XKitPlugins

Write-Host "Oh My XKit v$XKIT_VERSION loaded!" -ForegroundColor Green