# 🚀 XKit AutoStart - Instalador Simples e Funcional
# Execute este script para configurar a inicialização automática

Write-Host "🚀 XKit AutoStart - Instalação" -ForegroundColor Magenta
Write-Host "=" * 40 -ForegroundColor Magenta

# Verificar profile
$ProfilePath = "$env:USERPROFILE\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1"
if (-not (Test-Path $ProfilePath)) {
    Write-Host "❌ Profile não encontrado: $ProfilePath" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Profile encontrado" -ForegroundColor Green

# Criar script de startup
$StartupScript = "$PSScriptRoot\xkit-startup-simple.ps1"
$StartupContent = @'
# XKit Startup Script Simple
# Configure UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

# Carregar profile
$ProfilePath = "$env:USERPROFILE\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1"
if (Test-Path $ProfilePath) {
    try {
        . $ProfilePath
        
        # Enviar notificação básica
        $Message = "🌅 Windows Iniciado com XKit`n⏰ $(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')`n💻 $env:COMPUTERNAME"
        
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
'@

try {
    $StartupContent | Out-File -FilePath $StartupScript -Encoding UTF8
    Write-Host "✅ Script criado: xkit-startup-simple.ps1" -ForegroundColor Green
    
    # Criar tarefa no Task Scheduler
    $TaskName = "XKit-AutoStart-Simple"
    $Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-WindowStyle Hidden -ExecutionPolicy Bypass -File `"$StartupScript`""
    $Trigger = New-ScheduledTaskTrigger -AtLogOn
    $Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
    $Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive
    
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal -Force | Out-Null
    Write-Host "✅ Tarefa criada: $TaskName" -ForegroundColor Green
    
    # Registry backup
    $RegPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
    $RegName = "XKit-AutoStart"
    $RegValue = "powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$StartupScript`""
    
    Set-ItemProperty -Path $RegPath -Name $RegName -Value $RegValue
    Write-Host "✅ Registry configurado" -ForegroundColor Green
    
    Write-Host "`n🎉 AutoStart instalado com sucesso!" -ForegroundColor Green
    Write-Host "📋 Configurado:" -ForegroundColor White
    Write-Host "  • Task: $TaskName" -ForegroundColor Gray
    Write-Host "  • Script: xkit-startup-simple.ps1" -ForegroundColor Gray
    Write-Host "  • Registry: HKCU\Run\XKit-AutoStart" -ForegroundColor Gray
    
    # Teste
    $Test = Read-Host "`n🧪 Testar agora? (s/N)"
    if ($Test -eq 's' -or $Test -eq 'S') {
        Write-Host "`n🏃‍♂️ Testando..." -ForegroundColor Cyan
        & $StartupScript
    }
    
} catch {
    Write-Host "❌ Erro: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n💡 Para remover:" -ForegroundColor Yellow
Write-Host "  Unregister-ScheduledTask -TaskName '$TaskName' -Confirm:`$false" -ForegroundColor Cyan
Write-Host "  Remove-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run' -Name 'XKit-AutoStart'" -ForegroundColor Cyan