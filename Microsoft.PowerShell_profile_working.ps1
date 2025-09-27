# XKit v3.0.0 - Windows PowerShell Profile (Working Version)
# Configure UTF-8 support
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

# Load Python integration first
$XKitPython = "$PSScriptRoot\xkit-minimal-python.ps1"
if (Test-Path $XKitPython) {
    Write-Host "🔗 Carregando XKit Python..." -ForegroundColor Cyan
    . $XKitPython
    Write-Host "✅ XKit Python carregado!" -ForegroundColor Green
}

# Load legacy commands compatibility layer
$LegacyCommands = "$PSScriptRoot\xkit-legacy-commands.ps1"
if (Test-Path $LegacyCommands) {
    . $LegacyCommands
    Write-Host "✅ Comandos legacy carregados (gs, ga, gc, d, dc, etc.)" -ForegroundColor Green
} else {
    Write-Host "⚠️ Comandos legacy não encontrados" -ForegroundColor Yellow
}

# Oh-My-XKit style prompt function
function global:prompt {
    $Host.UI.RawUI.WindowTitle = "PowerShell - $(Get-Location)"
    
    # Get current directory name
    $currentDir = Split-Path -Leaf -Path (Get-Location)
    if ($currentDir -eq "") { $currentDir = "~" }
    
    # Get git branch if in git repo
    $gitBranch = ""
    $gitStatus = ""
    try {
        $branch = git rev-parse --abbrev-ref HEAD 2>$null
        if ($branch) {
            $gitBranch = " [$branch]"
            
            # Check git status for indicators
            $status = git status --porcelain 2>$null
            if ($status) {
                $gitStatus = " *"  # Indicate changes
            }
        }
    } catch {
        # Not a git repo or git not available
    }
    
    # Get container info (Docker/Podman)
    $containerInfo = ""
    if ($env:DOCKER_HOST -or (Get-Command docker -ErrorAction SilentlyContinue)) {
        try {
            $containers = docker ps --format "table {{.Names}}" 2>$null | Measure-Object -Line
            if ($containers.Lines -gt 1) {
                $containerInfo = " [docker]"
            }
        } catch { }
    }
    
    # Build prompt similar to oh-my-zsh
    $userName = $env:USERNAME
    $computerName = $env:COMPUTERNAME
    
    Write-Host "$userName@$computerName " -NoNewline -ForegroundColor Green
    Write-Host "$gitBranch" -NoNewline -ForegroundColor Yellow
    Write-Host "$gitStatus" -NoNewline -ForegroundColor Red
    Write-Host " ~$currentDir" -NoNewline -ForegroundColor Blue  
    Write-Host "$containerInfo" -NoNewline -ForegroundColor Cyan
    Write-Host ""
    Write-Host "$ " -NoNewline -ForegroundColor White
    return " "
}

# Simple Telegram notification function
function Send-XKitTelegramNotification {
    param(
        [string]$Message,
        [string]$Token = $env:TELEGRAM_TOKEN,
        [string]$ChatId = $env:ADMIN_ID,
        [switch]$Silent
    )
    
    if (-not $Token -or -not $ChatId) {
        if (-not $Silent) { Write-Host "⚠️ Telegram não configurado" -ForegroundColor Yellow }
        return $false
    }
    
    try {
        $Body = @{
            chat_id = $ChatId
            text = $Message
        }
        
        $Uri = "https://api.telegram.org/bot$Token/sendMessage"
        Invoke-RestMethod -Uri $Uri -Method POST -Body $Body -TimeoutSec 10 | Out-Null
        
        if (-not $Silent) { Write-Host "📱 Notificacao enviada" -ForegroundColor Green }
        return $true
    } catch {
        if (-not $Silent) { Write-Host "❌ Erro Telegram: $($_.Exception.Message)" -ForegroundColor Red }
        return $false
    }
}

function global:xkit-notify {
    param([string]$message)
    if ($message) {
        Send-XKitTelegramNotification -Message $message
    } else {
        Write-Host "Uso: xkit-notify 'sua mensagem'" -ForegroundColor Yellow
    }
}

# Send startup notification if AutoStart mode
if ($env:XKIT_AUTOSTART_MODE) {
    $StartupMessage = "🌅 Windows Iniciado com XKit v3.0.0 - $(Get-Date -Format 'HH:mm') - $env:COMPUTERNAME"
    
    # Send notification silently (non-blocking)
    if ($env:TELEGRAM_TOKEN -and $env:ADMIN_ID) {
        Start-Job -ScriptBlock {
            param($msg, $token, $chatid)
            try {
                $body = @{ chat_id = $chatid; text = $msg }
                $uri = "https://api.telegram.org/bot$token/sendMessage"
                Invoke-RestMethod -Uri $uri -Method POST -Body $body -TimeoutSec 5 | Out-Null
            } catch { }
        } -ArgumentList $StartupMessage, $env:TELEGRAM_TOKEN, $env:ADMIN_ID | Out-Null
    }
}

Write-Host "✅ XKit v3.0.0 Profile carregado!" -ForegroundColor Green