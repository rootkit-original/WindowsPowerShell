# 🚀 XKit AutoStart Configuration Script
# Configura o PowerShell para carregar automaticamente na inicialização do Windows

param(
    [switch]$Install,
    [switch]$Uninstall,
    [switch]$Status,
    [switch]$Test
)

# Configurações
$ScriptName = "XKit AutoStart"
$XKitPath = $PSScriptRoot
$ProfilePath = "$env:USERPROFILE\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1"
$StartupScript = "$XKitPath\xkit-autostart.ps1"

function Write-ColorText {
    param([string]$Text, [string]$Color = "White")
    Write-Host $Text -ForegroundColor $Color
}

function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Send-TelegramMessage {
    param([string]$Message)
    
    $Token = $env:TELEGRAM_TOKEN
    $ChatId = $env:ADMIN_ID
    
    if (-not $Token -or -not $ChatId) {
        Write-ColorText "⚠️  Telegram não configurado (TOKEN/ADMIN_ID)" "Yellow"
        return $false
    }
    
    try {
        $Body = @{
            chat_id = $ChatId
            text = $Message
            parse_mode = "Markdown"
        }
        
        $Uri = "https://api.telegram.org/bot$Token/sendMessage"
        $Response = Invoke-RestMethod -Uri $Uri -Method POST -Body $Body
        
        if ($Response.ok) {
            Write-ColorText "✅ Mensagem enviada para Telegram" "Green"
            return $true
        } else {
            Write-ColorText "❌ Falha ao enviar mensagem: $($Response.description)" "Red"
            return $false
        }
    } catch {
        Write-ColorText "❌ Erro Telegram: $($_.Exception.Message)" "Red"
        return $false
    }
}

function Install-AutoStart {
    Write-ColorText "🚀 Instalando XKit AutoStart..." "Cyan"
    
    # Método 1: Registry (Startup folder)
    $StartupFolder = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
    $ShortcutPath = "$StartupFolder\XKit-AutoStart.lnk"
    
    try {
        # Criar script de inicialização
        $AutoStartContent = @"
# XKit AutoStart Script
# Carrega o PowerShell com profile XKit na inicialização

# Configure UTF-8 first
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
`$env:PYTHONIOENCODING = "utf-8"

# Carregar profile XKit
`$ProfilePath = "$ProfilePath"
if (Test-Path `$ProfilePath) {
    Write-Host "🚀 Carregando XKit Profile..." -ForegroundColor Cyan
    . `$ProfilePath
    
    # Enviar notificação
    `$Message = @"
🖥️ **Windows Iniciado**
🚀 **XKit v3.0 Carregado**
⏰ **Horário:** `$(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')
💻 **Computador:** `$env:COMPUTERNAME
👤 **Usuário:** `$env:USERNAME
🏗️ **Arquitetura:** Hybrid MCP
"@
    
    # Função interna para Telegram
    function Send-StartupNotification {
        param([string]`$Msg)
        try {
            `$Token = "$env:TELEGRAM_TOKEN"
            `$ChatId = "$env:ADMIN_ID"
            if (`$Token -and `$ChatId) {
                `$Body = @{ chat_id = `$ChatId; text = `$Msg; parse_mode = "Markdown" }
                `$Uri = "https://api.telegram.org/bot`$Token/sendMessage"
                Invoke-RestMethod -Uri `$Uri -Method POST -Body `$Body | Out-Null
                Write-Host "📱 Notificação enviada para Telegram" -ForegroundColor Green
            }
        } catch {
            Write-Host "⚠️  Falha na notificação: `$(`$_.Exception.Message)" -ForegroundColor Yellow
        }
    }
    
    Send-StartupNotification `$Message
    Write-Host "✅ XKit carregado com sucesso!" -ForegroundColor Green
} else {
    Write-Host "❌ Profile XKit não encontrado: `$ProfilePath" -ForegroundColor Red
}

# Log da inicialização
`$LogPath = "$XKitPath\logs\autostart.log"
`$LogDir = Split-Path `$LogPath -Parent
if (-not (Test-Path `$LogDir)) { New-Item -ItemType Directory -Path `$LogDir -Force | Out-Null }
"`$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - XKit AutoStart executado" | Add-Content `$LogPath

# Manter console aberto por 3 segundos para ver mensagens
Start-Sleep -Seconds 3
"@
        
        $AutoStartContent | Out-File -FilePath $StartupScript -Encoding UTF8
        Write-ColorText "✅ Script criado: $StartupScript" "Green"
        
        # Método 2: Task Scheduler (Mais confiável)
        $TaskName = "XKit-AutoStart"
        $Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-WindowStyle Hidden -ExecutionPolicy Bypass -File `"$StartupScript`""
        $Trigger = New-ScheduledTaskTrigger -AtLogOn
        $Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
        $Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive
        
        # Registrar tarefa
        Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal -Force
        Write-ColorText "✅ Tarefa agendada criada: $TaskName" "Green"
        
        # Método 3: Registry Run Key (Backup)
        $RegPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
        $RegName = "XKit-AutoStart"
        $RegValue = "powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$StartupScript`""
        
        Set-ItemProperty -Path $RegPath -Name $RegName -Value $RegValue
        Write-ColorText "✅ Registry entry criada" "Green"
        
        Write-ColorText "`n🎉 XKit AutoStart instalado com sucesso!" "Green"
        Write-ColorText "📍 Métodos configurados:" "White"
        Write-ColorText "  • Task Scheduler: $TaskName" "Gray"
        Write-ColorText "  • Registry Run: HKCU\Run\$RegName" "Gray"
        Write-ColorText "  • Script: $StartupScript" "Gray"
        
        # Teste imediato
        Write-ColorText "`n🧪 Testando notificação..." "Cyan"
        $TestMessage = @"
🧪 **Teste XKit AutoStart**
✅ **Instalação concluída**
⏰ **Teste em:** $(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')
🔧 **Configurado por:** $env:USERNAME
"@
        Send-TelegramMessage $TestMessage
        
    } catch {
        Write-ColorText "❌ Erro na instalação: $($_.Exception.Message)" "Red"
        return $false
    }
    
    return $true
}

function Uninstall-AutoStart {
    Write-ColorText "🗑️  Removendo XKit AutoStart..." "Yellow"
    
    try {
        # Remover Task Scheduler
        $TaskName = "XKit-AutoStart"
        if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
            Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
            Write-ColorText "✅ Tarefa agendada removida" "Green"
        }
        
        # Remover Registry
        $RegPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
        $RegName = "XKit-AutoStart"
        if (Get-ItemProperty -Path $RegPath -Name $RegName -ErrorAction SilentlyContinue) {
            Remove-ItemProperty -Path $RegPath -Name $RegName
            Write-ColorText "✅ Registry entry removida" "Green"
        }
        
        # Remover script
        if (Test-Path $StartupScript) {
            Remove-Item $StartupScript -Force
            Write-ColorText "✅ Script removido" "Green"
        }
        
        Write-ColorText "🎉 XKit AutoStart removido com sucesso!" "Green"
        
    } catch {
        Write-ColorText "❌ Erro na remoção: $($_.Exception.Message)" "Red"
        return $false
    }
    
    return $true
}

function Show-Status {
    Write-ColorText "📊 Status do XKit AutoStart" "Cyan"
    Write-ColorText "=" * 40 "Cyan"
    
    # Task Scheduler
    $TaskName = "XKit-AutoStart"
    $Task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($Task) {
        $Status = if ($Task.State -eq "Ready") { "✅ Ativo" } else { "⚠️  Inativo ($($Task.State))" }
        Write-ColorText "Task Scheduler: $Status" "White"
    } else {
        Write-ColorText "Task Scheduler: ❌ Não configurado" "Red"
    }
    
    # Registry
    $RegPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
    $RegName = "XKit-AutoStart"
    $RegEntry = Get-ItemProperty -Path $RegPath -Name $RegName -ErrorAction SilentlyContinue
    if ($RegEntry) {
        Write-ColorText "Registry Run: ✅ Configurado" "Green"
        Write-ColorText "  Comando: $($RegEntry.$RegName)" "Gray"
    } else {
        Write-ColorText "Registry Run: ❌ Não configurado" "Red"
    }
    
    # Script
    if (Test-Path $StartupScript) {
        Write-ColorText "Script: ✅ Existe" "Green"
        Write-ColorText "  Path: $StartupScript" "Gray"
    } else {
        Write-ColorText "Script: ❌ Não encontrado" "Red"
    }
    
    # Profile
    if (Test-Path $ProfilePath) {
        Write-ColorText "Profile: ✅ Existe" "Green"
    } else {
        Write-ColorText "Profile: ❌ Não encontrado" "Red"
    }
    
    # Telegram
    if ($env:TELEGRAM_TOKEN -and $env:ADMIN_ID) {
        Write-ColorText "Telegram: ✅ Configurado" "Green"
    } else {
        Write-ColorText "Telegram: ⚠️  Não configurado" "Yellow"
    }
    
    # Logs
    $LogPath = "$XKitPath\logs\autostart.log"
    if (Test-Path $LogPath) {
        $LogCount = (Get-Content $LogPath).Count
        Write-ColorText "Logs: ✅ $LogCount entradas" "Green"
        Write-ColorText "  Última execução:" "Gray"
        $LastExecution = Get-Content $LogPath | Select-Object -Last 1
        Write-ColorText "    $LastExecution" "Gray"
    } else {
        Write-ColorText "Logs: ⚠️  Nenhum log encontrado" "Yellow"
    }
}

function Test-AutoStart {
    Write-ColorText "🧪 Testando XKit AutoStart..." "Cyan"
    
    # Testar script diretamente
    if (Test-Path $StartupScript) {
        Write-ColorText "🏃‍♂️ Executando script de teste..." "Yellow"
        & $StartupScript
        Write-ColorText "✅ Teste concluído" "Green"
    } else {
        Write-ColorText "❌ Script não encontrado para teste" "Red"
    }
}

# ================================
# MAIN EXECUTION
# ================================

Write-ColorText "🚀 XKit AutoStart Configuration" "Magenta"
Write-ColorText "=" * 50 "Magenta"

if ($Install) {
    Install-AutoStart
} elseif ($Uninstall) {
    Uninstall-AutoStart
} elseif ($Status) {
    Show-Status
} elseif ($Test) {
    Test-AutoStart
} else {
    Write-ColorText "📖 Uso:" "White"
    Write-ColorText "  -Install    Instalar AutoStart" "Gray"
    Write-ColorText "  -Uninstall  Remover AutoStart" "Gray"
    Write-ColorText "  -Status     Mostrar status" "Gray"
    Write-ColorText "  -Test       Testar execução" "Gray"
    Write-ColorText ""
    Write-ColorText "💡 Exemplo:" "Yellow"
    Write-ColorText "  .\xkit-autostart-config.ps1 -Install" "Cyan"
}