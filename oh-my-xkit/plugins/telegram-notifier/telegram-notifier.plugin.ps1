# Telegram Notifier Plugin for XKit
# Send notifications via Telegram

# Telegram notification functions
function telegram-notify {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Message,
        [string]$Emoji = "📢"
    )
    
    Write-Host "📱 Sending Telegram notification..." -ForegroundColor Yellow
    
    try {
        $pythonPath = Get-Command python -ErrorAction Stop | Select-Object -ExpandProperty Source
        $scriptPath = "$PSScriptRoot\..\..\Scripts\xkit_compact.py"
        
        if (Test-Path $scriptPath) {
            $fullMessage = "$Emoji $Message"
            $response = & $pythonPath $scriptPath telegram-notify $fullMessage 2>$null
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ Notification sent!" -ForegroundColor Green
            } else {
                Write-Host "❌ Failed to send notification" -ForegroundColor Red
            }
        } else {
            Write-Host "❌ XKit service not found" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ Error sending notification: $($_.Exception.Message)" -ForegroundColor Red
    }
}

function telegram-build-status {
    param(
        [Parameter(Mandatory=$true)]
        [ValidateSet("success", "failure", "started")]
        [string]$Status,
        [string]$Project = (Split-Path (Get-Location) -Leaf)
    )
    
    $emoji = switch ($Status) {
        "success" { "✅" }
        "failure" { "❌" }
        "started" { "🚀" }
    }
    
    $message = switch ($Status) {
        "success" { "Build completed successfully for $Project" }
        "failure" { "Build failed for $Project" }
        "started" { "Build started for $Project" }
    }
    
    telegram-notify $message $emoji
}

function telegram-git-push {
    param(
        [string]$Branch,
        [string]$CommitMessage
    )
    
    if (-not $Branch) {
        try {
            $Branch = git rev-parse --abbrev-ref HEAD 2>$null
        } catch {}
    }
    
    if (-not $CommitMessage) {
        try {
            $CommitMessage = git log -1 --pretty=format:"%s" 2>$null
        } catch {}
    }
    
    $message = "🔄 Pushed to $Branch"
    if ($CommitMessage) {
        $message += ": $CommitMessage"
    }
    
    telegram-notify $message "🌿"
}

function telegram-deployment {
    param(
        [Parameter(Mandatory=$true)]
        [ValidateSet("started", "success", "failure")]
        [string]$Status,
        [string]$Environment = "production",
        [string]$Version
    )
    
    $emoji = switch ($Status) {
        "started" { "🚀" }
        "success" { "🎉" } 
        "failure" { "💥" }
    }
    
    $message = switch ($Status) {
        "started" { "Deployment started to $Environment" }
        "success" { "Deployment successful to $Environment" }
        "failure" { "Deployment failed to $Environment" }
    }
    
    if ($Version) {
        $message += " (v$Version)"
    }
    
    telegram-notify $message $emoji
}

function telegram-error-alert {
    param(
        [Parameter(Mandatory=$true)]
        [string]$ErrorMessage,
        [string]$Context = (Get-Location).Path
    )
    
    $message = "🚨 Error in $Context`n`n$ErrorMessage"
    telegram-notify $message "🚨"
}

function telegram-status {
    Write-Host "📱 Telegram Notifier Status" -ForegroundColor Cyan
    Write-Host "============================" -ForegroundColor Cyan
    
    # Check if XKit service is available
    $scriptPath = "$PSScriptRoot\..\..\Scripts\xkit_compact.py"
    if (Test-Path $scriptPath) {
        Write-Host "✅ XKit Service: Available" -ForegroundColor Green
    } else {
        Write-Host "❌ XKit Service: Not Found" -ForegroundColor Red
        return
    }
    
    # Test notification
    Write-Host "🧪 Testing notification service..." -ForegroundColor Yellow
    try {
        $pythonPath = Get-Command python -ErrorAction Stop | Select-Object -ExpandProperty Source
        $response = & $pythonPath $scriptPath telegram-test 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Telegram service: Ready" -ForegroundColor Green
        } else {
            Write-Host "❌ Telegram service: Configuration error" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ Python/Service error: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    Write-Host "" -ForegroundColor White
    Write-Host "💡 Available Commands:" -ForegroundColor Cyan
    Write-Host "  telegram-notify 'message'     - Send custom notification" -ForegroundColor White
    Write-Host "  telegram-build-status success - Send build status" -ForegroundColor White
    Write-Host "  telegram-git-push             - Notify git push" -ForegroundColor White
    Write-Host "  telegram-deployment started   - Notify deployment status" -ForegroundColor White
    Write-Host "  telegram-error-alert 'error'  - Send error alert" -ForegroundColor White
}

# Automatic notifications for common events
function Enable-AutoNotifications {
    # Override git push to auto-notify
    function global:git {
        $originalCommand = Get-Command git -CommandType Application
        & $originalCommand @args
        
        if ($args[0] -eq "push" -and $LASTEXITCODE -eq 0) {
            telegram-git-push
        }
    }
    
    Write-Host "✅ Auto-notifications enabled for git push" -ForegroundColor Green
}

# Export aliases
New-Alias -Name "tg" -Value "telegram-notify" -Force -Scope Global
New-Alias -Name "tgbuild" -Value "telegram-build-status" -Force -Scope Global
New-Alias -Name "tgdeploy" -Value "telegram-deployment" -Force -Scope Global
New-Alias -Name "tgerror" -Value "telegram-error-alert" -Force -Scope Global

# Plugin metadata
$PLUGIN_NAME = "telegram-notifier"
$PLUGIN_AUTHOR = "XKit Team"
$PLUGIN_VERSION = "1.0.0"
$PLUGIN_DESCRIPTION = "Telegram notifications for development events"

Write-Verbose "✅ Loaded plugin: $PLUGIN_NAME v$PLUGIN_VERSION"