# XKit Startup Script Simple
# Configure UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

# Carregar profile (usando o profile padrão do PowerShell que redireciona para XKit)
$ProfilePath = "$env:USERPROFILE\Documents\PowerShell\Microsoft.PowerShell_profile.ps1"
if (Test-Path $ProfilePath) {
    try {
        . $ProfilePath
        
        # Enviar notificação básica
        $Message = "🌅 Windows Iniciado com XKit v3.0 + Oh-My-XKit`n⏰ $(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')`n💻 $env:COMPUTERNAME`n🎨 Legacy commands disponíveis (gs, ga, gc, etc.)"
        
        if ($env:TELEGRAM_TOKEN -and $env:ADMIN_ID) {
            try {
                $Body = @{
                    chat_id = $env:ADMIN_ID
                    text = $Message
                }
                $Uri = "https://api.telegram.org/bot$($env:TELEGRAM_TOKEN)/sendMessage"
                Invoke-RestMethod -Uri $Uri -Method POST -Body $Body -TimeoutSec 10 | Out-Null
                Write-Host "📱 Notificação enviada" -ForegroundColor Green
            } catch {
                Write-Host "⚠️ Falha Telegram: $($_.Exception.Message)" -ForegroundColor Yellow
            }
        }
        
        # Log
        $LogFile = "$PSScriptRoot\startup.log"
        "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - Startup OK" | Add-Content $LogFile
        
        Write-Host "✅ XKit carregado com sucesso!" -ForegroundColor Green
        
    } catch {
        Write-Host "❌ Erro no profile: $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "❌ Profile não encontrado" -ForegroundColor Red
}

Start-Sleep -Seconds 2
