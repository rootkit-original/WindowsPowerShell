# XKit v3.0 - Standardized Command Structure
# Usage: xkit <command> <params>

param(
    [Parameter(Position=0, Mandatory=$true)]
    [string]$Command,
    
    [Parameter(Position=1, ValueFromRemainingArguments=$true)]
    [string[]]$Parameters = @()
)

# Configure UTF-8 support
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

# XKit Python backend path
$XKitScript = "$PSScriptRoot\Scripts\xkit_main.py"

if (-not (Test-Path $XKitScript)) {
    Write-Host "XKit backend not found: $XKitScript" -ForegroundColor Red
    Write-Host "Make sure XKit is properly installed" -ForegroundColor Yellow
    exit 1
}

# Build command arguments: xkit <command> <params>
$AllArgs = @("xkit", $Command) + $Parameters

try {
    # Execute XKit with standardized structure
    & python $XKitScript $AllArgs
    
    if ($LASTEXITCODE -and $LASTEXITCODE -ne 0) {
        Write-Host "XKit command failed with exit code: $LASTEXITCODE" -ForegroundColor Red
        Write-Host "Try: xkit debug" -ForegroundColor Cyan
        exit $LASTEXITCODE
    }
} catch {
    Write-Host "XKit execution failed: $_" -ForegroundColor Red
    Write-Host "Try: xkit debug system" -ForegroundColor Cyan
    exit 1
}