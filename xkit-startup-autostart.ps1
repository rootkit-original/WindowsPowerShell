# XKit Startup Script - AutoStart Mode
# Configure UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

# Carregar profile principal do XKit
$ProfilePath = "$env:USERPROFILE\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1"
if (Test-Path $ProfilePath) {
    try {
        . $ProfilePath
        
        # Enviar notificação Telegram
        $Message = "🌅 Windows Iniciado com XKit v3.0.0`n⏰ $(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')`n💻 $env:COMPUTERNAME`n🎨 AutoStart Mode Ativo"
        
        if ($env:TELEGRAM_TOKEN -and $env:ADMIN_ID) {
            try {
                $Body = @{
                    chat_id = $env:ADMIN_ID
                    text = $Message
                }
                $Uri = "https://api.telegram.org/bot$($env:TELEGRAM_TOKEN)/sendMessage"
                Invoke-RestMethod -Uri $Uri -Method POST -Body $Body -TimeoutSec 10 | Out-Null
                Write-Host "📱 Notificação Telegram enviada" -ForegroundColor Green
            } catch {
                Write-Host "⚠️ Falha Telegram: $($_.Exception.Message)" -ForegroundColor Yellow
            }
        }
        
        # Log de startup
        $LogFile = "$PSScriptRoot\startup.log"
        "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - AutoStart OK" | Add-Content $LogFile
        
        Write-Host "✅ XKit AutoStart carregado com sucesso!" -ForegroundColor Green
        
    } catch {
        Write-Host "❌ Erro no profile: $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "❌ Profile principal não encontrado" -ForegroundColor Red
}

Start-Sleep -Seconds 3
