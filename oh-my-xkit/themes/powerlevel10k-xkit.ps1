# PowerLevel10k XKit Theme
# Inspired by powerlevel10k for zsh

function global:prompt {
    # Performance optimization
    $ErrorActionPreference = "SilentlyContinue"
    
    # User and system info
    $user = $env:USERNAME
    $computer = $env:COMPUTERNAME  
    $location = (Get-Location).Path
    $shortLocation = $location.Replace($HOME, '~')
    
    # Segment colors
    $userColor = "Green"
    $pathColor = "Cyan" 
    $gitColor = "Yellow"
    $containerColor = "Blue"
    $pythonColor = "Magenta"
    $errorColor = "Red"
    $arrowColor = "White"
    
    # Status indicators
    $segments = @()
    
    # Error indicator
    if ($LASTEXITCODE -ne 0 -and $LASTEXITCODE -ne $null) {
        $segments += @{
            "text" = "❌ $LASTEXITCODE"
            "color" = $errorColor
        }
    }
    
    # User@Computer segment
    $segments += @{
        "text" = "🪟 $user@$computer"
        "color" = $userColor
    }
    
    # Git branch segment  
    try {
        $gitBranch = git rev-parse --abbrev-ref HEAD 2>$null
        if ($gitBranch -and $LASTEXITCODE -eq 0) {
            # Git status indicators
            $status = git status --porcelain 2>$null
            $gitIcon = "🌿"
            if ($status) {
                # Check for staged changes
                if ($status | Where-Object { $_ -match "^[MADRC]" }) {
                    $gitIcon = "🌟" # Staged changes
                } else {
                    $gitIcon = "🔄" # Unstaged changes
                }
            }
            
            $segments += @{
                "text" = "$gitIcon $gitBranch"
                "color" = $gitColor
            }
        }
    } catch {}
    
    # Current directory segment
    $dirName = Split-Path $shortLocation -Leaf
    if (-not $dirName) { $dirName = $shortLocation }
    $segments += @{
        "text" = "📁 $dirName"
        "color" = $pathColor
    }
    
    # Container tools segment
    $containerTools = @()
    if (Get-Command podman -ErrorAction SilentlyContinue) {
        $containerTools += "podman"
    }
    if (Get-Command docker -ErrorAction SilentlyContinue) {
        $containerTools += "docker"
    }
    if ($containerTools.Count -gt 0) {
        $segments += @{
            "text" = "🐳 $($containerTools -join '|')"
            "color" = $containerColor
        }
    }
    
    # Python environment segment
    if ($env:VIRTUAL_ENV) {
        $venvName = Split-Path $env:VIRTUAL_ENV -Leaf
        $segments += @{
            "text" = "🐍 $venvName"
            "color" = $pythonColor
        }
    } elseif (Get-Command python -ErrorAction SilentlyContinue) {
        $pyVersion = python --version 2>$null | Select-String "\d+\.\d+" | ForEach-Object { $_.Matches[0].Value }
        if ($pyVersion) {
            $segments += @{
                "text" = "🐍 $pyVersion"
                "color" = $pythonColor
            }
        }
    }
    
    # XKit status segment
    if (Get-Command xkit -ErrorAction SilentlyContinue) {
        $segments += @{
            "text" = "⚡ XKit"
            "color" = "DarkCyan"
        }
    }
    
    # Build the prompt line
    Write-Host ""
    foreach ($segment in $segments) {
        Write-Host "  " -NoNewline
        Write-Host $segment.text -NoNewline -ForegroundColor $segment.color
    }
    
    # New line with arrow
    Write-Host ""
    Write-Host "❯ " -NoNewline -ForegroundColor $arrowColor
    
    return " "
}

# Theme metadata
$THEME_NAME = "powerlevel10k-xkit"
$THEME_AUTHOR = "XKit Team"
$THEME_VERSION = "1.0.0"
$THEME_DESCRIPTION = "PowerLevel10k inspired theme for PowerShell"

Write-Verbose "✅ Loaded theme: $THEME_NAME v$THEME_VERSION"