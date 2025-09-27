# 🗑️ XKit AutoStart - Script de Remoção
# Remove a configuração de inicialização automática

Write-Host "🗑️  XKit AutoStart - Remoção" -ForegroundColor Red
Write-Host "=" * 40 -ForegroundColor Red

$Removed = $false

# Remover Task Scheduler
try {
    $TaskName = "XKit-PowerShell-AutoStart"
    $Task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    
    if ($Task) {
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
        Write-Host "✅ Tarefa removida: $TaskName" -ForegroundColor Green
        $Removed = $true
    } else {
        Write-Host "ℹ️  Tarefa não encontrada: $TaskName" -ForegroundColor Gray
    }
} catch {
    Write-Host "❌ Erro ao remover tarefa: $($_.Exception.Message)" -ForegroundColor Red
}

# Remover Registry
try {
    $RegPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
    $RegName = "XKit-AutoStart"
    
    $RegEntry = Get-ItemProperty -Path $RegPath -Name $RegName -ErrorAction SilentlyContinue
    if ($RegEntry) {
        Remove-ItemProperty -Path $RegPath -Name $RegName
        Write-Host "✅ Registry removido: $RegName" -ForegroundColor Green
        $Removed = $true
    } else {
        Write-Host "ℹ️  Registry não encontrado: $RegName" -ForegroundColor Gray
    }
} catch {
    Write-Host "❌ Erro ao remover registry: $($_.Exception.Message)" -ForegroundColor Red
}

# Remover arquivos
$ScriptFiles = @(
    "$PSScriptRoot\xkit-startup.ps1",
    "$PSScriptRoot\xkit-autostart.ps1"
)

foreach ($File in $ScriptFiles) {
    if (Test-Path $File) {
        try {
            Remove-Item $File -Force
            Write-Host "✅ Arquivo removido: $(Split-Path $File -Leaf)" -ForegroundColor Green
            $Removed = $true
        } catch {
            Write-Host "❌ Erro ao remover arquivo: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

# Remover logs (opcional)
$LogDir = "$PSScriptRoot\logs"
if (Test-Path $LogDir) {
    $RemoveLogs = Read-Host "🗑️  Remover logs também? (s/N)"
    if ($RemoveLogs -eq 's' -or $RemoveLogs -eq 'S') {
        try {
            Remove-Item $LogDir -Recurse -Force
            Write-Host "✅ Logs removidos" -ForegroundColor Green
        } catch {
            Write-Host "❌ Erro ao remover logs: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

if ($Removed) {
    Write-Host "`n🎉 XKit AutoStart removido com sucesso!" -ForegroundColor Green
    Write-Host "💡 O PowerShell não será mais iniciado automaticamente" -ForegroundColor Cyan
} else {
    Write-Host "`n⚠️  Nenhuma configuração de AutoStart foi encontrada" -ForegroundColor Yellow
}

Write-Host "`nPressione qualquer tecla para continuar..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")