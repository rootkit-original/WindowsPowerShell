# 🔧 XKit AutoStart Manager
# Gerenciar a inicialização automática do XKit

param(
    [Parameter(Position=0)]
    [ValidateSet("status", "install", "uninstall", "test", "logs")]
    [string]$Action = "status"
)

$TaskName = "XKit-AutoStart-Simple"
$RegPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
$RegName = "XKit-AutoStart"
$StartupScript = "$PSScriptRoot\xkit-startup-simple.ps1"
$LogFile = "$PSScriptRoot\startup.log"

function Show-Status {
    Write-Host "🔍 XKit AutoStart - Status" -ForegroundColor Cyan
    Write-Host "=" * 30 -ForegroundColor Cyan
    
    # Verificar Registry
    $RegEntry = Get-ItemProperty $RegPath -Name $RegName -ErrorAction SilentlyContinue
    if ($RegEntry) {
        Write-Host "✅ Registry: Configurado" -ForegroundColor Green
        Write-Host "   $($RegEntry.$RegName)" -ForegroundColor Gray
    } else {
        Write-Host "❌ Registry: Não configurado" -ForegroundColor Red
    }
    
    # Verificar Task Scheduler
    $Task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($Task) {
        Write-Host "✅ Task Scheduler: $($Task.State)" -ForegroundColor Green
    } else {
        Write-Host "❌ Task Scheduler: Não encontrado" -ForegroundColor Red
    }
    
    # Verificar Script
    if (Test-Path $StartupScript) {
        Write-Host "✅ Script: Existe" -ForegroundColor Green
    } else {
        Write-Host "❌ Script: Não encontrado" -ForegroundColor Red
    }
    
    # Verificar Log
    if (Test-Path $LogFile) {
        $LastEntry = Get-Content $LogFile -Tail 1
        Write-Host "📝 Último startup: $LastEntry" -ForegroundColor White
    } else {
        Write-Host "📝 Log: Nenhum startup registrado" -ForegroundColor Yellow
    }
}

function Install-AutoStart {
    Write-Host "🚀 Instalando XKit AutoStart..." -ForegroundColor Green
    & "$PSScriptRoot\install-autostart-simple.ps1"
}

function Uninstall-AutoStart {
    Write-Host "🗑️ Removendo XKit AutoStart..." -ForegroundColor Yellow
    
    # Remover Task Scheduler
    $Task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($Task) {
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
        Write-Host "✅ Task removido" -ForegroundColor Green
    }
    
    # Remover Registry
    $RegEntry = Get-ItemProperty $RegPath -Name $RegName -ErrorAction SilentlyContinue
    if ($RegEntry) {
        Remove-ItemProperty $RegPath -Name $RegName
        Write-Host "✅ Registry removido" -ForegroundColor Green
    }
    
    # Remover Script
    if (Test-Path $StartupScript) {
        Remove-Item $StartupScript -Force
        Write-Host "✅ Script removido" -ForegroundColor Green
    }
    
    Write-Host "🎉 AutoStart removido com sucesso!" -ForegroundColor Green
}

function Test-AutoStart {
    Write-Host "🧪 Testando XKit AutoStart..." -ForegroundColor Cyan
    
    if (Test-Path $StartupScript) {
        & $StartupScript
    } else {
        Write-Host "❌ Script não encontrado: $StartupScript" -ForegroundColor Red
    }
}

function Show-Logs {
    Write-Host "📋 XKit AutoStart - Logs" -ForegroundColor Cyan
    Write-Host "=" * 25 -ForegroundColor Cyan
    
    if (Test-Path $LogFile) {
        Get-Content $LogFile | ForEach-Object {
            if ($_ -match "OK") {
                Write-Host $_ -ForegroundColor Green
            } elseif ($_ -match "ERROR") {
                Write-Host $_ -ForegroundColor Red
            } else {
                Write-Host $_ -ForegroundColor White
            }
        }
    } else {
        Write-Host "📝 Nenhum log encontrado" -ForegroundColor Yellow
    }
}

# Executar ação
switch ($Action) {
    "status" { Show-Status }
    "install" { Install-AutoStart }
    "uninstall" { Uninstall-AutoStart }
    "test" { Test-AutoStart }
    "logs" { Show-Logs }
}

Write-Host "`n💡 Uso: .\manage-autostart.ps1 [status|install|uninstall|test|logs]" -ForegroundColor Gray