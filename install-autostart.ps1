# 🚀 Instalador Rápido XKit AutoStart
# Execute este script para configurar a inicialização automática

Write-Host "🚀 XKit AutoStart - Instalação Rápida" -ForegroundColor Magenta
Write-Host "=" * 50 -ForegroundColor Magenta

# Verificar dependências
$ProfilePath = "$env:USERPROFILE\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1"
if (-not (Test-Path $ProfilePath)) {
    Write-Host "❌ Profile do PowerShell não encontrado!" -ForegroundColor Red
    Write-Host "💡 Certifique-se que o XKit está instalado corretamente" -ForegroundColor Yellow
    exit 1
}

# Verificar Telegram
if (-not $env:TELEGRAM_TOKEN -or -not $env:ADMIN_ID) {
    Write-Host "⚠️  Configuração Telegram não encontrada!" -ForegroundColor Yellow
    Write-Host "💡 Verifique se TELEGRAM_TOKEN e ADMIN_ID estão definidos no profile" -ForegroundColor Cyan
    
    $Continue = Read-Host "Continuar mesmo assim? (s/N)"
    if ($Continue -ne 's' -and $Continue -ne 'S') {
        Write-Host "❌ Instalação cancelada" -ForegroundColor Red
        exit 1
    }
}

Write-Host "`n🔧 Configurando AutoStart..." -ForegroundColor Cyan

# Método 1: Task Scheduler (Recomendado)
try {
    $TaskName = "XKit-PowerShell-AutoStart"
    $ScriptPath = $PSScriptRoot
    
    # Script que será executado na inicialização
    $StartupScript = "$ScriptPath\xkit-startup.ps1"
    $StartupContent = @"
# XKit Startup Script - Executa na inicialização do Windows
param([switch]`$Hide)

if (`$Hide) {
    `$Host.UI.RawUI.WindowTitle = "XKit Startup"
}

# Configure UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
`$env:PYTHONIOENCODING = "utf-8"
`$env:XKIT_AUTOSTART_MODE = "1"

# Executar profile XKit
`$ProfilePath = "$ProfilePath"
if (Test-Path `$ProfilePath) {
    . `$ProfilePath
    
    # Enviar notificação de startup
    `$Message = @"
🌅 **Windows Iniciado com XKit**
⏰ **$(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')**
💻 **`$env:COMPUTERNAME** | 👤 **`$env:USERNAME**
🚀 **XKit v3.0** | 🏗️ **Hybrid MCP Architecture**
📊 **Memória:** `$([math]::Round((Get-Process -Id `$PID).WorkingSet64/1MB, 1))MB
"@
    
    Send-XKitTelegramNotification `$Message -Silent
    
    # Log
    `$LogPath = "$ScriptPath\logs\startup.log"
    `$LogDir = Split-Path `$LogPath -Parent
    if (-not (Test-Path `$LogDir)) { New-Item -ItemType Directory -Path `$LogDir -Force | Out-Null }
    "`$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - Startup executado com sucesso" | Add-Content `$LogPath
    
    Write-Host "✅ XKit AutoStart executado com sucesso!" -ForegroundColor Green
} else {
    Write-Host "❌ Profile não encontrado: `$ProfilePath" -ForegroundColor Red
    `$ErrorMsg = "❌ **XKit AutoStart Falhou**`n📍 Profile não encontrado`n⏰ `$(Get-Date -Format 'HH:mm:ss')"
    Send-XKitTelegramNotification `$ErrorMsg -Silent
}

if (-not `$Hide) {
    Start-Sleep -Seconds 2
}
"@
    
    $StartupContent | Out-File -FilePath $StartupScript -Encoding UTF8
    Write-Host "✅ Script criado: $StartupScript" -ForegroundColor Green
    
    # Criar tarefa no Task Scheduler
    $Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-WindowStyle Hidden -ExecutionPolicy Bypass -File `"$StartupScript`" -Hide"
    $Trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
    $Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
    $Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited
    
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal -Force | Out-Null
    Write-Host "✅ Tarefa agendada: $TaskName" -ForegroundColor Green
    
    # Verificar se foi criada
    $Task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($Task -and $Task.State -eq "Ready") {
        Write-Host "✅ Tarefa ativa e pronta" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Tarefa criada mas pode não estar ativa" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "❌ Erro ao criar tarefa: $($_.Exception.Message)" -ForegroundColor Red
}

# Método 2: Registry (Backup)
try {
    $RegPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
    $RegName = "XKit-AutoStart"
    $RegValue = "powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$StartupScript`" -Hide"
    
    Set-ItemProperty -Path $RegPath -Name $RegName -Value $RegValue
    Write-Host "✅ Registry configurado: HKCU\Run\$RegName" -ForegroundColor Green
    
} catch {
    Write-Host "⚠️  Falha no Registry: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host "`n🎉 XKit AutoStart instalado com sucesso!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Configuração:" -ForegroundColor White
Write-Host "  • Task Scheduler: $TaskName" -ForegroundColor Gray
Write-Host "  • Script: $StartupScript" -ForegroundColor Gray
Write-Host "  • Registry: HKCU\Run\$RegName" -ForegroundColor Gray
Write-Host ""
Write-Host "🧪 Para testar agora:" -ForegroundColor Yellow
Write-Host "  & '$StartupScript'" -ForegroundColor Cyan
Write-Host ""
Write-Host "🗑️  Para remover:" -ForegroundColor Yellow
Write-Host "  Unregister-ScheduledTask -TaskName '$TaskName' -Confirm:`$false" -ForegroundColor Cyan
Write-Host "  Remove-ItemProperty -Path '$RegPath' -Name '$RegName'" -ForegroundColor Cyan

# Teste opcional
$Test = Read-Host "`n🧪 Executar teste agora? (s/N)"
if ($Test -eq 's' -or $Test -eq 'S') {
    Write-Host "`n🏃‍♂️ Executando teste..." -ForegroundColor Cyan
    & $StartupScript
    Write-Host "✅ Teste concluído!" -ForegroundColor Green
}

Write-Host "`n💡 Na próxima inicialização do Windows, você receberá uma notificação no Telegram!" -ForegroundColor Cyan