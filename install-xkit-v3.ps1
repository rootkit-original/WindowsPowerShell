# 🚀 XKit v3.0.0 Official Installer
# Hybrid MCP Architecture Release - September 26, 2025

param(
    [switch]$AutoStart,
    [switch]$Uninstall,
    [switch]$Status,
    [switch]$Force
)

$ErrorActionPreference = "Stop"

# XKit Release Information
$XKIT_VERSION = "3.0.0"
$XKIT_CODENAME = "Hybrid MCP Architecture"
$XKIT_RELEASE_DATE = "September 26, 2025"

Write-Host "🚀 XKit v$XKIT_VERSION Installer" -ForegroundColor Magenta
Write-Host "   $XKIT_CODENAME" -ForegroundColor Cyan
Write-Host "   Release Date: $XKIT_RELEASE_DATE" -ForegroundColor Gray
Write-Host "=" * 50 -ForegroundColor Magenta

# Define paths
$XKitBase = "$env:USERPROFILE\Documents\WindowsPowerShell"
$ProfilePath = "$env:USERPROFILE\Documents\PowerShell\Microsoft.PowerShell_profile.ps1"
$LegacyProfilePath = "$env:USERPROFILE\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1"

function Test-XKitInstallation {
    $installed = $false
    $issues = @()
    
    Write-Host "`n🔍 Checking XKit Installation..." -ForegroundColor Cyan
    
    # Check main files
    if (-not (Test-Path "$XKitBase\xkit.ps1")) {
        $issues += "❌ Main xkit.ps1 not found"
    } else {
        Write-Host "✅ Main xkit.ps1 found" -ForegroundColor Green
        $installed = $true
    }
    
    if (-not (Test-Path "$XKitBase\Scripts\xkit_main.py")) {
        $issues += "❌ Python core (xkit_main.py) not found"
    } else {
        Write-Host "✅ Python core found" -ForegroundColor Green
    }
    
    if (-not (Test-Path $ProfilePath)) {
        $issues += "❌ Universal profile not found"
    } else {
        Write-Host "✅ Universal profile found" -ForegroundColor Green
    }
    
    # Check AutoStart
    $RegEntry = Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name "XKit-AutoStart" -ErrorAction SilentlyContinue
    if ($RegEntry) {
        Write-Host "✅ AutoStart configured" -ForegroundColor Green
    } else {
        Write-Host "⚠️  AutoStart not configured" -ForegroundColor Yellow
    }
    
    # Check commands
    try {
        $xkitAvailable = (Get-Command xkit -ErrorAction SilentlyContinue) -ne $null
        if ($xkitAvailable) {
            Write-Host "✅ XKit commands available" -ForegroundColor Green
        } else {
            $issues += "❌ XKit commands not available"
        }
    } catch {
        $issues += "❌ Cannot test XKit commands"
    }
    
    if ($issues.Count -gt 0) {
        Write-Host "`n⚠️  Issues found:" -ForegroundColor Yellow
        $issues | ForEach-Object { Write-Host "  $_" -ForegroundColor Red }
    }
    
    return $installed
}

function Install-XKit {
    Write-Host "`n📦 Installing XKit v$XKIT_VERSION..." -ForegroundColor Green
    
    # Check if already installed
    if (-not $Force -and (Test-XKitInstallation)) {
        $continue = Read-Host "`n⚠️  XKit already installed. Continue anyway? (y/N)"
        if ($continue -ne 'y' -and $continue -ne 'Y') {
            Write-Host "Installation cancelled." -ForegroundColor Yellow
            return
        }
    }
    
    # Ensure directories exist
    Write-Host "📁 Creating directories..." -ForegroundColor Cyan
    New-Item -ItemType Directory -Path (Split-Path $ProfilePath) -Force | Out-Null
    New-Item -ItemType Directory -Path $XKitBase -Force | Out-Null
    
    # Create universal profile
    Write-Host "📄 Creating universal profile..." -ForegroundColor Cyan
    $UniversalProfile = @'
# XKit v3.0.0 - PowerShell Profile (Universal)
# Configure UTF-8 support for emojis FIRST
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

# Check if XKit is already loaded to avoid double loading
if (-not $global:XKitLoaded) {
    # Define XKit base directory
    $XKitBase = "$env:USERPROFILE\Documents\WindowsPowerShell"
    
    # Load XKit functions without changing directory
    if (Test-Path "$XKitBase\xkit.ps1") {
        Write-Host "🔗 Loading XKit v3.0.0 (Universal Mode)..." -ForegroundColor Cyan
        
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
    
    $UniversalProfile | Out-File $ProfilePath -Encoding UTF8 -Force
    Write-Host "✅ Universal profile created" -ForegroundColor Green
    
    # Install AutoStart if requested
    if ($AutoStart) {
        Write-Host "`n🚀 Installing AutoStart..." -ForegroundColor Cyan
        if (Test-Path "$PSScriptRoot\install-autostart-simple.ps1") {
            & "$PSScriptRoot\install-autostart-simple.ps1"
        } else {
            Write-Host "⚠️  AutoStart installer not found, skipping..." -ForegroundColor Yellow
        }
    }
    
    Write-Host "`n🎉 XKit v$XKIT_VERSION installed successfully!" -ForegroundColor Green
    Write-Host "💡 Usage:" -ForegroundColor White
    Write-Host "  • Open new PowerShell window" -ForegroundColor Gray
    Write-Host "  • Type: xkit help" -ForegroundColor Gray
    Write-Host "  • Use legacy commands: gs, ga, gc, etc." -ForegroundColor Gray
    
    if (-not $AutoStart) {
        $autostart = Read-Host "`n🚀 Install AutoStart (Windows startup)? (y/N)"
        if ($autostart -eq 'y' -or $autostart -eq 'Y') {
            Install-AutoStart
        }
    }
}

function Install-AutoStart {
    Write-Host "`n🚀 Installing AutoStart..." -ForegroundColor Cyan
    if (Test-Path "$PSScriptRoot\install-autostart-simple.ps1") {
        & "$PSScriptRoot\install-autostart-simple.ps1"
    } else {
        Write-Host "❌ AutoStart installer not found" -ForegroundColor Red
    }
}

function Uninstall-XKit {
    Write-Host "`n🗑️  Uninstalling XKit..." -ForegroundColor Yellow
    
    $confirm = Read-Host "Are you sure you want to uninstall XKit? (y/N)"
    if ($confirm -ne 'y' -and $confirm -ne 'Y') {
        Write-Host "Uninstall cancelled." -ForegroundColor Green
        return
    }
    
    # Remove profiles
    if (Test-Path $ProfilePath) {
        Remove-Item $ProfilePath -Force
        Write-Host "✅ Universal profile removed" -ForegroundColor Green
    }
    
    # Remove AutoStart
    $RegEntry = Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name "XKit-AutoStart" -ErrorAction SilentlyContinue
    if ($RegEntry) {
        Remove-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name "XKit-AutoStart"
        Write-Host "✅ AutoStart removed from Registry" -ForegroundColor Green
    }
    
    $Task = Get-ScheduledTask -TaskName "XKit-AutoStart-Simple" -ErrorAction SilentlyContinue
    if ($Task) {
        Unregister-ScheduledTask -TaskName "XKit-AutoStart-Simple" -Confirm:$false
        Write-Host "✅ AutoStart task removed" -ForegroundColor Green
    }
    
    Write-Host "`n🎉 XKit uninstalled successfully!" -ForegroundColor Green
    Write-Host "💡 XKit files remain in: $XKitBase" -ForegroundColor Gray
    Write-Host "   Delete manually if desired." -ForegroundColor Gray
}

# Main execution
try {
    if ($Status) {
        Test-XKitInstallation | Out-Null
    } elseif ($Uninstall) {
        Uninstall-XKit
    } else {
        Install-XKit
    }
} catch {
    Write-Host "`n❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "💡 Run with -Force to override checks" -ForegroundColor Yellow
    exit 1
}

Write-Host "`n💡 Usage Examples:" -ForegroundColor Yellow
Write-Host "  .\install-xkit-v3.ps1               # Install XKit" -ForegroundColor Cyan
Write-Host "  .\install-xkit-v3.ps1 -AutoStart    # Install with AutoStart" -ForegroundColor Cyan
Write-Host "  .\install-xkit-v3.ps1 -Status       # Check installation" -ForegroundColor Cyan
Write-Host "  .\install-xkit-v3.ps1 -Uninstall    # Remove XKit" -ForegroundColor Cyan