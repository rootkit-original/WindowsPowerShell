# Minimal XKit Theme
# Ultra clean minimal theme

function global:prompt {
    $location = (Get-Location).Path.Replace($HOME, '~')
    $dirName = Split-Path $location -Leaf
    if (-not $dirName) { $dirName = $location }
    
    # Git branch indicator
    $git = ""
    try {
        $gitBranch = git rev-parse --abbrev-ref HEAD 2>$null
        if ($gitBranch -and $LASTEXITCODE -eq 0) {
            $git = " ($gitBranch)"
        }
    } catch {}
    
    Write-Host "$dirName" -NoNewline -ForegroundColor Cyan
    if ($git) {
        Write-Host $git -NoNewline -ForegroundColor Yellow
    }
    Write-Host " ❯ " -NoNewline -ForegroundColor Gray
    
    return ""
}

# Theme metadata
$THEME_NAME = "minimal-xkit"
$THEME_AUTHOR = "XKit Team"
$THEME_VERSION = "1.0.0" 
$THEME_DESCRIPTION = "Minimal clean prompt theme"

Write-Verbose "✅ Loaded theme: $THEME_NAME v$THEME_VERSION"