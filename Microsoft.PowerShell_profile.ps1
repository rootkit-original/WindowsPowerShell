# XKit v3.0.0 - Windows PowerShell Profile (ASCII Only)
# Configure UTF-8 support
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

# Load XKit v3.0 core system
$XKitScript = "$PSScriptRoot\xkit.ps1"
if (Test-Path $XKitScript) {
    Write-Host "XKit v3.0 Profile Loaded" -ForegroundColor Green
    Write-Host "Use: xkit help" -ForegroundColor Cyan
} else {
    Write-Host "XKit core not found: $XKitScript" -ForegroundColor Red
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
                $gitStatus = " *"
            }
        }
    } catch {
        # Not a git repo or git not available
    }
    
    # Build prompt similar to oh-my-zsh
    $userName = $env:USERNAME
    $computerName = $env:COMPUTERNAME
    
    Write-Host "$userName@$computerName " -NoNewline -ForegroundColor Green
    Write-Host "$gitBranch" -NoNewline -ForegroundColor Yellow
    Write-Host "$gitStatus" -NoNewline -ForegroundColor Red
    Write-Host " ~$currentDir" -NoNewline -ForegroundColor Blue  
    Write-Host ""
    Write-Host "$ " -NoNewline -ForegroundColor White
    return " "
}

Write-Host "XKit v3.0.0 Profile loaded!" -ForegroundColor Green
