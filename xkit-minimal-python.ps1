# XKit v3.0 - Ultra-Minimal Python-First Approach
# Single PowerShell function that delegates EVERYTHING to Python

# Configure UTF-8 once
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

# Single universal function for ALL XKit commands
function global:Invoke-XKitPython {
    param(
        [Parameter(Position=0, Mandatory=$true)]
        [string]$Action,
        
        [Parameter(Position=1, ValueFromRemainingArguments=$true)]
        [string[]]$Arguments = @()
    )
    
    $XKitScript = "$PSScriptRoot\Scripts\xkit_main.py"
    $AllArgs = @($Action) + $Arguments
    
    try {
        & python $XKitScript $AllArgs
    } catch {
        Write-Host "❌ XKit Error: $_" -ForegroundColor Red
        Write-Host "💡 Make sure Python and XKit are properly installed" -ForegroundColor Yellow
    }
}

# Dynamic command generation - ALL commands call the same function
$XKitCommands = @(
    # Core commands
    'xkit-help', 'xkit-status', 'xkit-version', 'xkit-reload',
    
    # MCP commands
    'mcp-status', 'mcp-servers', 'mcp-tools', 'mcp-call',
    
    # Plugin commands  
    'plugin-list', 'plugin-load', 'plugin-reload', 'plugin-unload',
    
    # Event commands
    'events-status', 'events-history', 'events-clear',
    
    # Git commands
    'git-status', 'git-branch', 'git-create-branch',
    
    # AI commands
    'ai-analyze', 'ai-explain-code', 'xpilot-analyze',
    
    # Debug commands
    'debug', 'system-init', 'diagnose'
)

# Register ALL commands dynamically
foreach ($command in $XKitCommands) {
    $commandFunc = @"
function global:$command {
    param([Parameter(ValueFromRemainingArguments)][string[]]`$args)
    Invoke-XKitPython '$command' @args
}
"@
    Invoke-Expression $commandFunc
}

# Legacy aliases for compatibility
Set-Alias -Name "help" -Value "xkit-help" -Force
Set-Alias -Name "status" -Value "xkit-status" -Force  
Set-Alias -Name "version" -Value "xkit-version" -Force

# Show minimal startup message
Write-Host "🚀 " -NoNewline -ForegroundColor Cyan
Write-Host "XKit v3.0 Python-First Architecture Ready" -ForegroundColor Green
Write-Host "💡 " -NoNewline -ForegroundColor Yellow
Write-Host "All commands delegate to Python backend"