# Classic XKit Theme
# Simple, clean theme inspired by oh-my-zsh default

function global:prompt {
    $user = $env:USERNAME
    $computer = $env:COMPUTERNAME
    $location = (Get-Location).Path.Replace($HOME, '~')
    
    # Git branch (simple)
    $branch = ""
    try {
        $gitBranch = git rev-parse --abbrev-ref HEAD 2>$null
        if ($gitBranch -and $LASTEXITCODE -eq 0) {
            $branch = " [$gitBranch]"
        }
    } catch {}
    
    # Simple prompt
    Write-Host "$user@$computer" -NoNewline -ForegroundColor Green
    Write-Host ":$location" -NoNewline -ForegroundColor Blue
    if ($branch) { 
        Write-Host $branch -NoNewline -ForegroundColor Yellow 
    }
    Write-Host "$ " -NoNewline -ForegroundColor White
    
    return ""
}

# Theme metadata
$THEME_NAME = "classic-xkit"
$THEME_AUTHOR = "XKit Team" 
$THEME_VERSION = "1.0.0"
$THEME_DESCRIPTION = "Classic terminal prompt theme"

Write-Verbose "✅ Loaded theme: $THEME_NAME v$THEME_VERSION"