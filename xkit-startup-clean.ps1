# XKit Startup Script - AutoStart Mode (Non-Interactive)
# Configure UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

Write-Host "🚀 XKit AutoStart - Iniciando..." -ForegroundColor Cyan

# Carregar profile principal do XKit
$ProfilePath = "$env:USERPROFILE\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1"
if (Test-Path $ProfilePath) {
    try {
        . $ProfilePath
        
        # Log de startup
        $LogFile = "$PSScriptRoot\startup.log"
        "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - AutoStart OK" | Add-Content $LogFile
        
        Write-Host "✅ XKit AutoStart carregado!" -ForegroundColor Green
        
        # Enviar notificação Telegram (opcional)
        if ($env:TELEGRAM_TOKEN -and $env:ADMIN_ID) {
            try {
                $Message = "🌅 Windows + XKit v3.0.0`n⏰ $(Get-Date -Format 'HH:mm')`n💻 $env:COMPUTERNAME"
                $Body = @{
                    chat_id = $env:ADMIN_ID
                    text = $Message
                }
                $Uri = "https://api.telegram.org/bot$($env:TELEGRAM_TOKEN)/sendMessage"
                Invoke-RestMethod -Uri $Uri -Method POST -Body $Body -TimeoutSec 5 | Out-Null
                Write-Host "📱 Telegram OK" -ForegroundColor Green
            } catch {
                # Silencioso - não importa se falhar
            }
        }
        
    } catch {
        Write-Host "❌ Erro: $($_.Exception.Message)" -ForegroundColor Red
        $LogFile = "$PSScriptRoot\startup.log"
        "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - ERRO: $($_.Exception.Message)" | Add-Content $LogFile
    }
} else {
    Write-Host "❌ Profile não encontrado: $ProfilePath" -ForegroundColor Red
}

Write-Host "🎯 XKit AutoStart concluído" -ForegroundColor Gray