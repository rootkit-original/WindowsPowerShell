# Telegram Notifier Plugin - Simple version

function global:tg {
    param([string]$Message)
    
    if (-not $Message) {
        Write-Host "Usage: tg 'your message'" -ForegroundColor Yellow
        return
    }
    
    try {
        $scriptPath = "$PSScriptRoot\..\..\Scripts\xkit_compact.py"
        if (Test-Path $scriptPath) {
            python $scriptPath telegram-notify $Message
        } else {
            Write-Host "XKit Telegram service not found" -ForegroundColor Red
        }
    } catch {
        Write-Host "Error sending notification: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Verbose "Telegram Notifier plugin loaded"