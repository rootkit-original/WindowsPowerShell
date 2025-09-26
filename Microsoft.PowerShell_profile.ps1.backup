# Oh My XKit - Enhanced PowerShell Profile
# Version: 2.1.0 with oh-my-zsh inspired framework

# GitHub Copilot Integration
. "$PSScriptRoot\gh-copilot.ps1"

# Load Oh My XKit framework
$OH_MY_XKIT_PATH = "$PSScriptRoot\oh-my-xkit\oh-my-xkit.ps1"
if (Test-Path $OH_MY_XKIT_PATH) {
    . $OH_MY_XKIT_PATH
    
    # Load theme
    Load-XKitTheme
    
    # Load plugins
    Load-XKitPlugins
    
    # Load help system
    $HELP_PATH = "$PSScriptRoot\oh-my-xkit\xkit-help.ps1"
    if (Test-Path $HELP_PATH) {
        . $HELP_PATH
    }
} else {
    Write-Host "⚠️  Oh My XKit not found, using fallback prompt" -ForegroundColor Yellow
    
    # Fallback prompt function
    function prompt {
        $user = $env:USERNAME
        $computer = $env:COMPUTERNAME
        $location = (Get-Location).Path.Replace($HOME, '~')
        
        # Git branch detection
        $branch = ""
        try {
            $gitBranch = git rev-parse --abbrev-ref HEAD 2>$null
            if ($gitBranch -and $LASTEXITCODE -eq 0) {
                $branch = " [$gitBranch]"
            }
        } catch {}
        
        Write-Host "$user@$computer" -NoNewline -ForegroundColor Green
        if ($branch) {
            Write-Host $branch -NoNewline -ForegroundColor Yellow
        }
        Write-Host " $location" -NoNewline -ForegroundColor Blue
        Write-Host "`n$" -NoNewline -ForegroundColor White
        return " "
    }
}

# 🛠️ Chocolatey Integration
$ChocolateyProfile = "$env:ChocolateyInstall\helpers\chocolateyProfile.psm1"
if (Test-Path($ChocolateyProfile)) {
    Import-Module "$ChocolateyProfile"
}

# 🔐 Environment Variables
$env:GITLAB_TOKEN = 'glpat-CoOQ3_JxrX_kC7zEYiGfs286MQp1OjEH.01.0w1yvqqa3'
$env:GITLAB_URL = 'https://localhost'

# 🤖 XKit v2.1 AI & Telegram Configuration
$env:GEMINI_API_KEY = 'AIzaSyCvzBo-iK-KBdwedZYSHyoHcMzsYqEArC4'
$env:TELEGRAM_TOKEN = '8477588651:AAGaQLuk7hsfW5UWiNEnpGWK2Z6rRLg9A-s'
$env:ADMIN_ID = '7335391186'

# 🚀 XKit Core Functions
function Invoke-XKit {
    param([string[]]$Arguments = @())
    
    $xkitScript = "$PSScriptRoot\Scripts\xkit_compact.py"
    if (Test-Path $xkitScript) {
        if ($Arguments.Count -gt 0) {
            python $xkitScript @Arguments
        } else {
            python $xkitScript
        }
    } else {
        Write-Host "❌ XKit não encontrado: $xkitScript" -ForegroundColor Red
        Write-Host "💡 Verifique se os arquivos estão na pasta correta" -ForegroundColor Yellow
    }
}

# 🎯 XKit Commands - Interface Simplificada
function xkit-help { Invoke-XKit "help" }
function xkit-status { Invoke-XKit "status" } 
function xkit-info { Invoke-XKit "info" }
function xkit-ai { 
    param([string]$Question)
    if ($Question) {
        Invoke-XKit "ai" $Question
    } else {
        Invoke-XKit "ai"
    }
}
function xkit-solve { 
    param([string]$Problem)
    if ($Problem) {
        Invoke-XKit "solve" $Problem  
    } else {
        Write-Host "💡 Uso: xkit-solve 'descreva o problema'" -ForegroundColor Yellow
    }
}
function xkit-reload { 
    Write-Host "🔄 Recarregando perfil do PowerShell..." -ForegroundColor Cyan
    . $PROFILE 
}

# 🐳 Container Management - Auto-Detection Engine
function Get-ContainerEngine {
    $engines = @(
        @{Name="podman"; Path="C:\Program Files\RedHat\Podman\podman.exe"},
        @{Name="docker"; Path="C:\Program Files\Docker\Docker\resources\bin\docker.exe"}
    )
    
    foreach ($engine in $engines) {
        if (Test-Path $engine.Path) {
            $composeAvailable = $false
            
            # Check for compose tools
            if ($engine.Name -eq "podman") {
                $composeAvailable = (Get-Command "podman-compose" -ErrorAction SilentlyContinue) -ne $null
            } elseif ($engine.Name -eq "docker") {
                $composeAvailable = $true  # Docker includes compose
            }
            
            return @{
                Engine = $engine.Name
                Path = $engine.Path
                HasCompose = $composeAvailable
            }
        }
    }
    return $null
}

# 🐳 Container Commands Setup
$containerInfo = Get-ContainerEngine
if ($containerInfo) {
    $enginePath = $containerInfo.Path
    $engineName = $containerInfo.Engine
    
    # Core aliases
    Set-Alias -Name docker -Value $enginePath -Force -Scope Global -ErrorAction SilentlyContinue
    Set-Alias -Name $engineName -Value $enginePath -Force -Scope Global -ErrorAction SilentlyContinue
    
    # Container management functions
    function global:container-status {
        Write-Host "📊 Container Status ($($containerInfo.Engine)):" -ForegroundColor Cyan
        
        if ($containerInfo.Engine -eq "podman") {
            Write-Host "`n🖥️  Podman Machines:" -ForegroundColor Yellow
            & $enginePath machine list 2>$null
        }
        
        Write-Host "`n🐳 Running Containers:" -ForegroundColor Yellow  
        & $enginePath ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"
        
        if ($containerInfo.HasCompose) {
            Write-Host "`n📦 Compose Available: ✅" -ForegroundColor Green
        } else {
            Write-Host "`n📦 Compose Available: ❌" -ForegroundColor Red
        }
    }
    
    # Compose commands
    if ($containerInfo.HasCompose) {
        function global:compose-up {
            Write-Host "🚀 Starting services with $($containerInfo.Engine)-compose..." -ForegroundColor Green
            if ($containerInfo.Engine -eq "podman") {
                podman-compose up -d
            } else {
                docker compose up -d
            }
        }
        
        function global:compose-down {
            Write-Host "🛑 Stopping services with $($containerInfo.Engine)-compose..." -ForegroundColor Yellow
            if ($containerInfo.Engine -eq "podman") {
                podman-compose down
            } else {
                docker compose down  
            }
        }
        
        function global:compose-logs {
            if ($containerInfo.Engine -eq "podman") {
                podman-compose logs -f
            } else {
                docker compose logs -f
            }
        }
    }
    
    # Set environment variables
    $env:CONTAINER_ENGINE = $engineName.ToLower()
    if ($containerInfo.HasCompose) {
        $env:CONTAINER_COMPOSE = if ($containerInfo.Engine -eq "podman") { "podman-compose" } else { "docker compose" }
    }
    
    # Project-specific shortcuts
    function global:dev-up {
        param([string]$Project = "dev")
        Write-Host "🔧 Starting $Project environment..." -ForegroundColor Cyan
        
        $composeFile = "docker-compose.$Project.yml"
        if (Test-Path $composeFile) {
            if ($containerInfo.Engine -eq "podman") {
                podman-compose -f $composeFile up -d
            } else {
                docker compose -f $composeFile up -d
            }
        } else {
            Write-Warning "Compose file not found: $composeFile"
        }
    }
}

# 🎉 XKit Initialization
Write-Host ""
Write-Host "🚀 " -NoNewline -ForegroundColor Blue
Write-Host "XKit v2.1" -NoNewline -ForegroundColor Green  
Write-Host " - Sistema Inteligente de Desenvolvimento" -ForegroundColor Cyan

# Initialize XKit
try {
    Invoke-XKit
} catch {
    Write-Host "⚠️  XKit executando em modo básico" -ForegroundColor Yellow
    Write-Host "💡 Use 'xkit-help' para ver comandos disponíveis" -ForegroundColor Cyan
}