# Oh My XKit - PowerShell Framework
# Inspired by oh-my-zsh for Linux/Mac

$XKIT_VERSION = "2.1.0"
$OH_MY_XKIT = "$PSScriptRoot\oh-my-xkit"

# XKit Configuration
$XKIT_THEME = "powerlevel10k-xkit"
$XKIT_PLUGINS = @(
    "git", 
    "docker", 
    "ai-assistant",
    "telegram-notifier"
)

# Colors for themes
$XKIT_COLORS = @{
    "GREEN" = "Green"
    "BLUE" = "Blue" 
    "YELLOW" = "Yellow"
    "RED" = "Red"
    "CYAN" = "Cyan"
    "MAGENTA" = "Magenta"
    "WHITE" = "White"
    "GRAY" = "Gray"
}

# Load theme
function Load-XKitTheme {
    param([string]$ThemeName = $XKIT_THEME)
    
    $themePath = "$OH_MY_XKIT\themes\$ThemeName.ps1"
    if (Test-Path $themePath) {
        . $themePath
        Write-Verbose "✅ Theme loaded: $ThemeName"
    } else {
        Write-Warning "⚠️  Theme not found: $ThemeName"
        # Fallback to default theme
        Set-DefaultXKitPrompt
    }
}

# Load plugins
function Load-XKitPlugins {
    foreach ($plugin in $XKIT_PLUGINS) {
        $pluginPath = "$OH_MY_XKIT\plugins\$plugin\$plugin.plugin.ps1"
        if (Test-Path $pluginPath) {
            . $pluginPath
            Write-Verbose "✅ Plugin loaded: $plugin"
        } else {
            Write-Warning "⚠️  Plugin not found: $plugin"
        }
    }
}

# Default prompt fallback
function Set-DefaultXKitPrompt {
    function global:prompt {
        $user = $env:USERNAME
        $computer = $env:COMPUTERNAME
        $location = (Get-Location).Path.Replace($HOME, '~')
        
        # Git branch detection
        $branch = ""
        try {
            $gitBranch = git rev-parse --abbrev-ref HEAD 2>$null
            if ($gitBranch -and $LASTEXITCODE -eq 0) {
                $branch = " 🌿$gitBranch"
            }
        } catch {}
        
        # Container detection
        $container = ""
        if (Get-Command podman -ErrorAction SilentlyContinue) {
            $container = " 🐳podman"
        } elseif (Get-Command docker -ErrorAction SilentlyContinue) {
            $container = " 🐳docker"
        }
        
        # Python detection
        $python = ""
        if ($env:VIRTUAL_ENV -or (Get-Command python -ErrorAction SilentlyContinue)) {
            $python = " 🐍💙"
        }
        
        # Build prompt
        Write-Host "🪟 " -NoNewline -ForegroundColor Blue
        Write-Host "$user@$computer" -NoNewline -ForegroundColor $XKIT_COLORS["GREEN"]
        if ($branch) { Write-Host $branch -NoNewline -ForegroundColor $XKIT_COLORS["YELLOW"] }
        Write-Host " 📁$(Split-Path $location -Leaf)" -NoNewline -ForegroundColor $XKIT_COLORS["CYAN"]
        if ($container) { Write-Host $container -NoNewline -ForegroundColor $XKIT_COLORS["BLUE"] }
        if ($python) { Write-Host $python -NoNewline -ForegroundColor $XKIT_COLORS["MAGENTA"] }
        Write-Host ""
        Write-Host "$ " -NoNewline -ForegroundColor $XKIT_COLORS["WHITE"]
        return " "
    }
}

# XKit utility functions (oh-my-zsh inspired)
function xkit-version { 
    Write-Host "Oh My XKit v$XKIT_VERSION" -ForegroundColor Green
    Write-Host "🚀 PowerShell framework inspired by oh-my-zsh" -ForegroundColor Cyan
}

function xkit-reload { 
    Write-Host "🔄 Reloading Oh My XKit..." -ForegroundColor Yellow
    . $PROFILE
    Write-Host "✅ Reloaded!" -ForegroundColor Green
}

function xkit-themes {
    Write-Host "📋 Available themes:" -ForegroundColor Cyan
    Get-ChildItem "$OH_MY_XKIT\themes" -Filter "*.ps1" | ForEach-Object {
        $themeName = $_.BaseName
        if ($themeName -eq $XKIT_THEME) {
            Write-Host "  ✅ $themeName (active)" -ForegroundColor Green
        } else {
            Write-Host "  📄 $themeName" -ForegroundColor White
        }
    }
}

function xkit-plugins {
    Write-Host "🔌 Available plugins:" -ForegroundColor Cyan
    Get-ChildItem "$OH_MY_XKIT\plugins" -Directory | ForEach-Object {
        $pluginName = $_.Name
        if ($XKIT_PLUGINS -contains $pluginName) {
            Write-Host "  ✅ $pluginName (enabled)" -ForegroundColor Green
        } else {
            Write-Host "  📦 $pluginName (available)" -ForegroundColor Gray
        }
    }
}

function Set-XKitTheme {
    param([string]$ThemeName)
    
    if (Test-Path "$OH_MY_XKIT\themes\$ThemeName.ps1") {
        # Update profile configuration
        (Get-Content $PROFILE) -replace 'XKIT_THEME = ".*"', "XKIT_THEME = `"$ThemeName`"" | Set-Content $PROFILE
        Write-Host "✅ Theme set to: $ThemeName" -ForegroundColor Green
        Write-Host "🔄 Reload with: xkit-reload" -ForegroundColor Cyan
    } else {
        Write-Host "❌ Theme not found: $ThemeName" -ForegroundColor Red
        xkit-themes
    }
}

# Export functions to global scope
New-Alias -Name "omx-version" -Value "xkit-version" -Force -Scope Global
New-Alias -Name "omx-reload" -Value "xkit-reload" -Force -Scope Global  
New-Alias -Name "omx-themes" -Value "xkit-themes" -Force -Scope Global
New-Alias -Name "omx-plugins" -Value "xkit-plugins" -Force -Scope Global

Write-Host ""
Write-Host "🎨 " -NoNewline -ForegroundColor Blue
Write-Host "Oh My XKit" -NoNewline -ForegroundColor Green  
Write-Host " v$XKIT_VERSION loaded!" -ForegroundColor Cyan
Write-Host "💡 Type 'xkit-help' for commands" -ForegroundColor Yellow