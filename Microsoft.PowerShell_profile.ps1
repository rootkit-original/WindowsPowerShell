# Oh My XKit - Enhanced PowerShell Profile
# Version: 2.1.0 with oh-my-zsh inspired framework

# GitHub Copilot Integration
$copilotPath = "$PSScriptRoot\gh-copilot.ps1"
if (Test-Path $copilotPath) {
    . $copilotPath
}

# Load Oh My XKit framework
$OH_MY_XKIT_PATH = "$PSScriptRoot\oh-my-xkit\oh-my-xkit.ps1"
if (Test-Path $OH_MY_XKIT_PATH) {
    . $OH_MY_XKIT_PATH
} else {
    Write-Host "⚠️  Oh My XKit not found, using fallback prompt" -ForegroundColor Yellow
    
    # Fallback prompt function
    function prompt {
        $user = $env:USERNAME
        $computer = $env:COMPUTERNAME
        $location = (Get-Location).Path.Replace($HOME, '~')
        
        Write-Host "$user@$computer ~$(Split-Path $location -Leaf)" -NoNewline -ForegroundColor Green
        return "$ "
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

# XKit v2.1 AI & Telegram Configuration
$env:GEMINI_API_KEY = 'AIzaSyCvzBo-iK-KBdwedZYSHyoHcMzsYqEArC4'
$env:TELEGRAM_TOKEN = '8477588651:AAGaQLuk7hsfW5UWiNEnpGWK2Z6rRLg9A-s'
$env:ADMIN_ID = '7335391186'

# XKit Core Functions
function Invoke-XKit {
    param(
        [string]$Action,
        [string]$Context
    )
    
    $pythonScript = "$PSScriptRoot\Scripts\xkit_compact.py"
    
    if (Test-Path $pythonScript) {
        try {
            if ($Action -and $Context) {
                python $pythonScript $Action $Context
            } else {
                python $pythonScript
            }
        } catch {
            Write-Host "❌ Erro ao executar XKit: $($_.Exception.Message)" -ForegroundColor Red
        }
    } else {
        Write-Host "❌ XKit não encontrado em: $pythonScript" -ForegroundColor Red
    }
}

# XKit shortcuts
function xkit { 
    param([string]$Action, [string]$Context)
    Invoke-XKit $Action $Context 
}

# Container shortcuts
function dkr { docker @args }
function podman-status { podman ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" }
function docker-status { docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" }

# Git shortcuts  
function gs { git status }
function gl { git log --oneline -10 }
function gp { git push }
function gc { git commit -m @args }

# Welcome message
Write-Host ""
Write-Host "🎨 " -NoNewline -ForegroundColor Blue
Write-Host "Oh My XKit" -NoNewline -ForegroundColor Green  
Write-Host " v2.1.0 loaded!" -ForegroundColor Cyan
Write-Host "💡 Type 'xkit-help' for available commands" -ForegroundColor Yellow