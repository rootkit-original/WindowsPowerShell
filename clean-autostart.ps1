# 🧹 XKit AutoStart - Limpeza Completa
# Remove TODAS as configurações de autostart do XKit

Write-Host "🧹 XKit AutoStart - Limpeza Completa" -ForegroundColor Yellow
Write-Host "=" * 40 -ForegroundColor Yellow

$confirm = Read-Host "`n⚠️  Isso vai remover TODAS as configurações de autostart do XKit. Continuar? (s/N)"
if ($confirm -ne 's' -and $confirm -ne 'S') {
    Write-Host "Operação cancelada." -ForegroundColor Green
    exit 0
}

Write-Host "`n🔍 Procurando configurações do XKit..." -ForegroundColor Cyan

# Remover TODAS as tarefas relacionadas ao XKit
Write-Host "`n1. Verificando Task Scheduler..." -ForegroundColor Cyan
$XKitTasks = Get-ScheduledTask | Where-Object { $_.TaskName -like "*XKit*" -or $_.TaskName -like "*xkit*" }
if ($XKitTasks) {
    foreach ($task in $XKitTasks) {
        try {
            Unregister-ScheduledTask -TaskName $task.TaskName -Confirm:$false
            Write-Host "  ✅ Tarefa removida: $($task.TaskName)" -ForegroundColor Green
        } catch {
            Write-Host "  ❌ Falha ao remover: $($task.TaskName) - $($_.Exception.Message)" -ForegroundColor Red
        }
    }
} else {
    Write-Host "  ℹ️  Nenhuma tarefa XKit encontrada" -ForegroundColor Gray
}

# Remover TODAS as entradas do Registry
Write-Host "`n2. Verificando Registry..." -ForegroundColor Cyan
$RegPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
$AllEntries = Get-ItemProperty $RegPath -ErrorAction SilentlyContinue

if ($AllEntries) {
    $XKitEntries = $AllEntries.PSObject.Properties | Where-Object { 
        $_.Name -like "*XKit*" -or $_.Name -like "*xkit*" -or 
        $_.Value -like "*xkit*" -or $_.Value -like "*XKit*"
    }
    
    if ($XKitEntries) {
        foreach ($entry in $XKitEntries) {
            try {
                Remove-ItemProperty $RegPath -Name $entry.Name
                Write-Host "  ✅ Registry removido: $($entry.Name)" -ForegroundColor Green
            } catch {
                Write-Host "  ❌ Falha ao remover: $($entry.Name) - $($_.Exception.Message)" -ForegroundColor Red
            }
        }
    } else {
        Write-Host "  ℹ️  Nenhuma entrada XKit encontrada no Registry" -ForegroundColor Gray
    }
}

# Remover scripts de startup
Write-Host "`n3. Verificando scripts de startup..." -ForegroundColor Cyan
$ScriptPaths = @(
    "$env:USERPROFILE\Documents\WindowsPowerShell",
    "$env:USERPROFILE\Documents\PowerShell",
    "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
)

$ScriptPatterns = @("*xkit*startup*", "*xkit*autostart*", "*startup*xkit*", "*autostart*xkit*")

foreach ($path in $ScriptPaths) {
    if (Test-Path $path) {
        foreach ($pattern in $ScriptPatterns) {
            $scripts = Get-ChildItem $path -Name $pattern -ErrorAction SilentlyContinue
            foreach ($script in $scripts) {
                $fullPath = Join-Path $path $script
                try {
                    Remove-Item $fullPath -Force
                    Write-Host "  ✅ Script removido: $fullPath" -ForegroundColor Green
                } catch {
                    Write-Host "  ❌ Falha ao remover: $fullPath - $($_.Exception.Message)" -ForegroundColor Red
                }
            }
        }
    }
}

# Verificar pasta Startup do Windows
Write-Host "`n4. Verificando pasta Startup do Windows..." -ForegroundColor Cyan
$StartupFolder = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
if (Test-Path $StartupFolder) {
    $StartupFiles = Get-ChildItem $StartupFolder | Where-Object { $_.Name -like "*xkit*" -or $_.Name -like "*XKit*" }
    if ($StartupFiles) {
        foreach ($file in $StartupFiles) {
            try {
                Remove-Item $file.FullName -Force
                Write-Host "  ✅ Arquivo Startup removido: $($file.Name)" -ForegroundColor Green
            } catch {
                Write-Host "  ❌ Falha ao remover: $($file.Name) - $($_.Exception.Message)" -ForegroundColor Red
            }
        }
    } else {
        Write-Host "  ℹ️  Nenhum arquivo XKit na pasta Startup" -ForegroundColor Gray
    }
}

# Limpar logs antigos
Write-Host "`n5. Limpando logs..." -ForegroundColor Cyan
$LogFiles = @("$env:USERPROFILE\Documents\WindowsPowerShell\startup.log", "$env:USERPROFILE\Documents\WindowsPowerShell\autostart.log")
foreach ($logFile in $LogFiles) {
    if (Test-Path $logFile) {
        try {
            Remove-Item $logFile -Force
            Write-Host "  ✅ Log removido: $(Split-Path -Leaf $logFile)" -ForegroundColor Green
        } catch {
            Write-Host "  ❌ Falha ao remover log: $(Split-Path -Leaf $logFile)" -ForegroundColor Red
        }
    }
}

Write-Host "`n🎉 Limpeza completa finalizada!" -ForegroundColor Green
Write-Host "💡 Agora você pode reinstalar o XKit AutoStart com:" -ForegroundColor White
Write-Host "   .\install-autostart-simple.ps1" -ForegroundColor Cyan

# Verificar se ainda há algo
Write-Host "`n🔍 Verificação final..." -ForegroundColor Cyan
$RemainingTasks = Get-ScheduledTask | Where-Object { $_.TaskName -like "*XKit*" }
$RemainingReg = Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -ErrorAction SilentlyContinue | 
    Where-Object { $_.PSObject.Properties.Name -like "*XKit*" }

if (-not $RemainingTasks -and -not $RemainingReg) {
    Write-Host "✅ Sistema limpo - nenhuma configuração XKit encontrada" -ForegroundColor Green
} else {
    Write-Host "⚠️  Algumas configurações podem ter permanecido:" -ForegroundColor Yellow
    if ($RemainingTasks) { Write-Host "  - Tarefas: $($RemainingTasks.TaskName -join ', ')" -ForegroundColor Gray }
    if ($RemainingReg) { Write-Host "  - Registry: Entradas encontradas" -ForegroundColor Gray }
}