# 🚀 XKit AutoSta$StartupContent = @'
# XKit Startup Script Simple
# Configure UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

# Carregar profile principal do XKit
$ProfilePath = "$env:USERPROFILE\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1"
if (Test-Path $ProfilePath) {
    try {
        . $ProfilePath
        
        # Enviar notificação básica
        $Message = "🌅 Windows Iniciado com XKit v3.0.0`n⏰ $(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')`n💻 $env:COMPUTERNAME`n🎨 AutoStart Mode - Profiles configurados universalmente"
        
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
    # LIMPEZA PRIMEIRO - Remover configurações existentes
    Write-Host "🧹 Removendo configurações antigas..." -ForegroundColor Yellow
    
    # Remover tarefa existente
    $ExistingTask = Get-ScheduledTask -TaskName "XKit-AutoStart*" -ErrorAction SilentlyContinue
    if ($ExistingTask) {
        $ExistingTask | ForEach-Object {
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
    
    # Remover scripts antigos
    $OldScripts = @("$PSScriptRoot\xkit-startup.ps1", "$PSScriptRoot\xkit-autostart.ps1", "$PSScriptRoot\startup.ps1")
    foreach ($OldScript in $OldScripts) {
        if (Test-Path $OldScript) {
            Remove-Item $OldScript -Force -ErrorAction SilentlyContinue
            Write-Host "  ✅ Script antigo removido: $(Split-Path -Leaf $OldScript)" -ForegroundColor Green
        }
    }
    
    Write-Host "✅ Limpeza concluída" -ForegroundColor Green
    
    # AGORA INSTALAR LIMPO
    Write-Host "`n📝 Criando nova configuração..." -ForegroundColor Cyan
    $StartupContent | Out-File -FilePath $StartupScript -Encoding UTF8
    Write-Host "✅ Script criado: xkit-startup-simple.ps1" -ForegroundColor Green
    
    # Configurar TODOS os profiles para XKit funcionar
    Write-Host "`n📄 Configurando profiles universais..." -ForegroundColor Cyan
    
    # Profile PowerShell 7+
    $PS7Profile = "$env:USERPROFILE\Documents\PowerShell\Microsoft.PowerShell_profile.ps1"
    $PS7ProfileDir = Split-Path $PS7Profile
    if (-not (Test-Path $PS7ProfileDir)) {
        New-Item -ItemType Directory -Path $PS7ProfileDir -Force | Out-Null
    }
    
    # Profile Windows PowerShell 5.1 (caso não seja o principal)
    $PS5Profile = "$env:USERPROFILE\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1"
    
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
    
    # Instalar profile para ambos PowerShell 7+ e 5.1
    $UniversalProfile | Out-File $PS7Profile -Encoding UTF8 -Force
    Write-Host "  ✅ Profile PowerShell 7+ configurado" -ForegroundColor Green
    
    # Se não estivermos no diretório principal, configurar também o profile local
    $CurrentProfile = $PS5Profile
    if (Test-Path $CurrentProfile) {
        Write-Host "  ✅ Profile Windows PowerShell 5.1 já existe" -ForegroundColor Green
    } else {
        $UniversalProfile | Out-File $CurrentProfile -Encoding UTF8 -Force
        Write-Host "  ✅ Profile Windows PowerShell 5.1 configurado" -ForegroundColor Green
    }
    
    # Configurar Registry PRIMEIRO (método principal)
    $RegPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
    $RegName = "XKit-AutoStart"
    $RegValue = "powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$StartupScript`""
    
    Set-ItemProperty -Path $RegPath -Name $RegName -Value $RegValue
    Write-Host "✅ Registry configurado (método principal)" -ForegroundColor Green
    
    # Tentar Task Scheduler como backup (pode falhar sem admin)
    $TaskName = "XKit-AutoStart-Simple"
    try {
        $Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-WindowStyle Hidden -ExecutionPolicy Bypass -File `"$StartupScript`""
        $Trigger = New-ScheduledTaskTrigger -AtLogOn
        $Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
        $Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive
        
        Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal -Force | Out-Null
        Write-Host "✅ Task Scheduler configurado (backup)" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  Task Scheduler não disponível (sem admin): Registry será suficiente" -ForegroundColor Yellow
    }
    
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