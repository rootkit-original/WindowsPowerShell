# 🚀 XKit AutoStart - Instalador Completo v3.0.0
# Execute este script para configurar a inicialização automática

Write-Host "🚀 XKit AutoStart - Instalação v3.0.0" -ForegroundColor Magenta
Write-Host "=" * 45 -ForegroundColor Magenta

# Verificar profile principal
$ProfilePath = "$env:USERPROFILE\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1"
if (-not (Test-Path $ProfilePath)) {
    Write-Host "❌ Profile principal não encontrado: $ProfilePath" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Profile principal encontrado" -ForegroundColor Green

# LIMPEZA PRIMEIRO - Remover configurações existentes
Write-Host "`n🧹 Removendo configurações antigas..." -ForegroundColor Yellow

# Remover tarefa existente
$ExistingTasks = Get-ScheduledTask -TaskName "*XKit*" -ErrorAction SilentlyContinue
if ($ExistingTasks) {
    $ExistingTasks | ForEach-Object {
        Unregister-ScheduledTask -TaskName $_.TaskName -Confirm:$false -ErrorAction SilentlyContinue
        Write-Host "  ✅ Tarefa removida: $($_.TaskName)" -ForegroundColor Green
    }
}

# Remover entradas do Registry
$RegPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
$RegEntries = @("XKit-AutoStart", "XKit-AutoStart-Simple", "XKitAutoStart")
foreach ($RegName in $RegEntries) {
    $RegEntry = Get-ItemProperty $RegPath -Name $RegName -ErrorAction SilentlyContinue
    if ($RegEntry) {
        Remove-ItemProperty $RegPath -Name $RegName -ErrorAction SilentlyContinue
        Write-Host "  ✅ Registry removido: $RegName" -ForegroundColor Green
    }
}

# Remover profiles antigos se não forem o principal
$ProfilesToClean = @(
    "$env:USERPROFILE\Documents\PowerShell\Microsoft.PowerShell_profile.ps1"
)

foreach ($profile in $ProfilesToClean) {
    if (Test-Path $profile) {
        Remove-Item $profile -Force -ErrorAction SilentlyContinue
        Write-Host "  ✅ Profile removido: $(Split-Path -Leaf $profile)" -ForegroundColor Green
    }
}

Write-Host "✅ Limpeza concluída" -ForegroundColor Green

# CRIAÇÃO DO SCRIPT DE STARTUP
Write-Host "`n📝 Criando script de startup..." -ForegroundColor Cyan

$StartupScript = "$PSScriptRoot\xkit-startup-autostart.ps1"
$StartupContent = @'
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
'@

try {
    $StartupContent | Out-File -FilePath $StartupScript -Encoding UTF8
    Write-Host "✅ Script criado: xkit-startup-autostart.ps1" -ForegroundColor Green
    
    # CONFIGURAÇÃO DOS PROFILES UNIVERSAIS
    Write-Host "`n📄 Configurando profiles universais..." -ForegroundColor Cyan
    
    # Conteúdo do profile universal
    $UniversalProfile = @'
# XKit v3.0.0 - PowerShell Profile (AutoStart Mode)
# Configure UTF-8 support for emojis FIRST
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

# Check if XKit is already loaded to avoid double loading
if (-not $global:XKitLoaded) {
    # Define XKit base directory
    $XKitBase = "$env:USERPROFILE\Documents\WindowsPowerShell"
    
    # Load XKit functions without changing directory
    if (Test-Path "$XKitBase\xkit.ps1") {
        Write-Host "🔗 Loading XKit v3.0.0 (AutoStart Mode)..." -ForegroundColor Cyan
        
        # Create xkit function that works from any directory
        function global:xkit {
            param(
                [Parameter(Position=0, Mandatory=$true)]
                [string]$Command,
                
                [Parameter(Position=1, ValueFromRemainingArguments=$true)]
                [string[]]$Parameters = @()
            )
            
            # Call XKit from its directory but return to current location
            $CurrentDir = Get-Location
            try {
                Set-Location $XKitBase
                & "$XKitBase\xkit.ps1" $Command @Parameters
            } finally {
                Set-Location $CurrentDir
            }
        }
        
        # Load legacy commands
        if (Test-Path "$XKitBase\xkit-legacy-commands.ps1") {
            $OriginalLocation = Get-Location
            Set-Location $XKitBase
            try {
                . "$XKitBase\xkit-legacy-commands.ps1"
            } finally {
                Set-Location $OriginalLocation
            }
        }
        
        $global:XKitLoaded = $true
        Write-Host "✅ XKit loaded - works from any directory!" -ForegroundColor Green
    } else {
        Write-Host "❌ XKit not found at: $XKitBase" -ForegroundColor Red
    }
} else {
    Write-Host "✅ XKit already loaded" -ForegroundColor Green
}

# Oh-My-XKit style prompt function
function global:prompt {
    $Host.UI.RawUI.WindowTitle = "PowerShell - $(Get-Location)"
    
    # Get current directory name
    $currentDir = Split-Path -Leaf -Path (Get-Location)
    if ($currentDir -eq "") { $currentDir = "~" }
    
    # Get git branch if in git repo
    $gitBranch = ""
    $gitStatus = ""
    try {
        $branch = git rev-parse --abbrev-ref HEAD 2>$null
        if ($branch) {
            $gitBranch = " [$branch]"
            
            # Check git status for indicators
            $status = git status --porcelain 2>$null
            if ($status) {
                $gitStatus = " *"  # Indicate changes
            }
        }
    } catch {
        # Not a git repo or git not available
    }
    
    # Get container info (Docker/Podman)
    $containerInfo = ""
    if ($env:DOCKER_HOST -or (Get-Command docker -ErrorAction SilentlyContinue)) {
        try {
            $containers = docker ps --format "table {{.Names}}" 2>$null | Measure-Object -Line
            if ($containers.Lines -gt 1) {
                $containerInfo = " [docker]"
            }
        } catch { }
    }
    
    # Build prompt similar to oh-my-zsh
    $userName = $env:USERNAME
    $computerName = $env:COMPUTERNAME
    
    Write-Host "$userName@$computerName " -NoNewline -ForegroundColor Green
    Write-Host "$gitBranch" -NoNewline -ForegroundColor Yellow
    Write-Host "$gitStatus" -NoNewline -ForegroundColor Red
    Write-Host " ~$currentDir" -NoNewline -ForegroundColor Blue  
    Write-Host "$containerInfo" -NoNewline -ForegroundColor Cyan
    Write-Host ""
    Write-Host "$ " -NoNewline -ForegroundColor White
    return " "
}
'@
    
    # Profile PowerShell 7+
    $PS7Profile = "$env:USERPROFILE\Documents\PowerShell\Microsoft.PowerShell_profile.ps1"
    $PS7ProfileDir = Split-Path $PS7Profile
    if (-not (Test-Path $PS7ProfileDir)) {
        New-Item -ItemType Directory -Path $PS7ProfileDir -Force | Out-Null
    }
    
    $UniversalProfile | Out-File $PS7Profile -Encoding UTF8 -Force
    Write-Host "  ✅ Profile PowerShell 7+ configurado" -ForegroundColor Green
    
    # CONFIGURAÇÃO DO WINDOWS AUTOSTART
    Write-Host "`n🚀 Configurando Windows AutoStart..." -ForegroundColor Cyan
    
    # Registry (método principal)
    $RegName = "XKit-AutoStart"
    $RegValue = "powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$StartupScript`""
    
    Set-ItemProperty -Path $RegPath -Name $RegName -Value $RegValue
    Write-Host "  ✅ Registry configurado (método principal)" -ForegroundColor Green
    
    # Task Scheduler (backup - pode falhar sem admin)
    $TaskName = "XKit-AutoStart-v3"
    try {
        $Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-WindowStyle Hidden -ExecutionPolicy Bypass -File `"$StartupScript`""
        $Trigger = New-ScheduledTaskTrigger -AtLogOn
        $Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
        $Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive
        
        Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal -Force | Out-Null
        Write-Host "  ✅ Task Scheduler configurado (backup)" -ForegroundColor Green
    } catch {
        Write-Host "  ⚠️ Task Scheduler não disponível (sem admin): Registry é suficiente" -ForegroundColor Yellow
    }
    
    Write-Host "`n🎉 XKit AutoStart v3.0.0 instalado com sucesso!" -ForegroundColor Green
    Write-Host "📋 Configurado:" -ForegroundColor White
    Write-Host "  • Registry: HKCU\Run\XKit-AutoStart" -ForegroundColor Gray
    Write-Host "  • Script: xkit-startup-autostart.ps1" -ForegroundColor Gray
    Write-Host "  • Profile PowerShell 7+: Configurado" -ForegroundColor Gray
    Write-Host "  • Profile Windows PowerShell: Usando principal" -ForegroundColor Gray
    
    # Teste opcional
    $Test = Read-Host "`n🧪 Testar agora? (s/N)"
    if ($Test -eq 's' -or $Test -eq 'S') {
        Write-Host "`n🏃‍♂️ Testando..." -ForegroundColor Cyan
        & $StartupScript
    }
    
} catch {
    Write-Host "❌ Erro na instalação: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host "`n💡 Como usar:" -ForegroundColor Yellow
Write-Host "  • Reinicie o Windows para ver AutoStart em ação" -ForegroundColor Cyan
Write-Host "  • Abra qualquer PowerShell: comandos estarão disponíveis" -ForegroundColor Cyan
Write-Host "  • Use: gs, ga, gc, xkit version, etc." -ForegroundColor Cyan

Write-Host "`n🔧 Para remover:" -ForegroundColor Yellow
Write-Host "  .\clean-autostart.ps1" -ForegroundColor Cyan