# PowerLevel10k XKit Theme - Simple version

function global:prompt {
    $user = $env:USERNAME
    $computer = $env:COMPUTERNAME  
    $location = (Get-Location).Path.Replace($HOME, '~')
    $dirName = Split-Path $location -Leaf
    if (-not $dirName) { $dirName = $location }
    
    # Git branch
    $branch = ""
    try {
        $gitBranch = git rev-parse --abbrev-ref HEAD 2>$null
        if ($gitBranch -and $LASTEXITCODE -eq 0) {
            $branch = " [$gitBranch]"
        }
    } catch {}
    
    # Container detection
    $container = ""
    if (Get-Command podman -ErrorAction SilentlyContinue) {
        $container = " [podman]"
    } elseif (Get-Command docker -ErrorAction SilentlyContinue) {
        $container = " [docker]"
    }
    
    Write-Host "$user@$computer" -NoNewline -ForegroundColor Green
    if ($branch) { Write-Host $branch -NoNewline -ForegroundColor Yellow }
    Write-Host " ~$dirName" -NoNewline -ForegroundColor Cyan
    if ($container) { Write-Host $container -NoNewline -ForegroundColor Blue }
    Write-Host "`n$ " -NoNewline -ForegroundColor White
    return ""
}