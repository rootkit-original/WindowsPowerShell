# XKit v3.0 - Hybrid MCP Architecture - Ultra-Minimal PowerShell Profile
# All logic is in Python. This is just a thin wrapper for the new architecture.

# XKit Python Bridge - Single function for Hybrid MCP Architecture
function Invoke-XKit {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Action,
        
        [Parameter(ValueFromRemainingArguments)]
        [string[]]$Arguments = @()
    )
    
    # Absolute paths (no dependencies)
    $XKitRoot = "C:\Users\Usuario\Documents\WindowsPowerShell"
    $PythonMain = "$XKitRoot\Scripts\xkit_main.py"
    
    # Verify Python main exists
    if (-not (Test-Path $PythonMain)) {
        Write-Host "Error: XKit Python main not found at: $PythonMain" -ForegroundColor Red
        Write-Host "Info: Run 'Install-XKit' to set up the hybrid architecture" -ForegroundColor Yellow
        return $false
    }
    
    # Execute Python with error handling
    try {
        # Set environment variables for UTF-8 and API keys
        $env:PYTHONIOENCODING = "utf-8"
        $env:XKIT_VERSION = "3.0.0"
        $env:XKIT_ARCHITECTURE = "hybrid-mcp"
        $env:GEMINI_API_KEY = "AIzaSyCvzBo-iK-KBdwedZYSHyoHcMzsYqEArC4"
        $env:TELEGRAM_TOKEN = "8477588651:AAGaQLuk7hsfW5UWiNEnpGWK2Z6rRLg9A-s"
        $env:ADMIN_ID = "7335391186"
        
        # Set console encoding to UTF-8 for better emoji support
        [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
        
        # Build and execute command
        $cmd = @("python", $PythonMain, $Action) + $Arguments
        & $cmd[0] $cmd[1..($cmd.Length-1)]
        
        if ($LASTEXITCODE -and $LASTEXITCODE -ne 0) {
            Write-Host "Error: XKit Python failed with exit code: $LASTEXITCODE" -ForegroundColor Red
            Write-Host "Debug: Use 'xkit debug system' for detailed diagnostics" -ForegroundColor Cyan
            return $false
        }
    }
    catch {
        Write-Host "Error: XKit execution failed: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "Debug: Use 'xkit debug system' for system diagnostics" -ForegroundColor Cyan
        return $false
    }
}

# XKit v3.0 Core Commands - Hybrid MCP Architecture
# All commands delegate to Python through MCP protocol

# Core XKit commands
function global:xkit-help { Invoke-XKit "help" @args }
function global:xkit-version { Invoke-XKit "version" @args }
function global:xkit-status { Invoke-XKit "status" @args }
function global:xkit-reload { 
    Write-Host "Reloading XKit v3.0 profile..." -ForegroundColor Yellow
    . $PROFILE
    Write-Host "XKit Hybrid MCP Architecture reloaded!" -ForegroundColor Green
}

# MCP commands - new in v3.0
function global:mcp-status { Invoke-XKit "mcp-status" @args }
function global:mcp-servers { Invoke-XKit "mcp-list-servers" @args }
function global:mcp-tools { Invoke-XKit "mcp-list-tools" @args }
function global:mcp-call { Invoke-XKit "mcp-call-tool" @args }

# Plugin commands - new in v3.0
function global:plugin-list { Invoke-XKit "plugin-list" @args }
function global:plugin-load { Invoke-XKit "plugin-load" @args }
function global:plugin-unload { Invoke-XKit "plugin-unload" @args }
function global:plugin-reload { Invoke-XKit "plugin-reload" @args }

# Event system commands - new in v3.0
function global:events-status { Invoke-XKit "events-status" @args }
function global:events-history { Invoke-XKit "events-history" @args }
function global:events-publish { Invoke-XKit "events-publish" @args }

# Git commands with enhanced error handling through MCP
function global:xstatus { Invoke-XKit "git-status" @args }
function global:xadd { Invoke-XKit "git-add" @args }
function global:xcommit { Invoke-XKit "git-commit" @args }
function global:xpush { Invoke-XKit "git-push" @args }
function global:xlog { Invoke-XKit "git-log" @args }
function global:xbranch { Invoke-XKit "git-branch" @args }
function global:xcheckout { Invoke-XKit "git-checkout" @args }
function global:xnew-branch { Invoke-XKit "git-create-branch" @args }

# Container commands through MCP
function global:xpodman { Invoke-XKit "container-podman" @args }
function global:xcontainers { Invoke-XKit "container-list" @args }
function global:ximages { Invoke-XKit "container-images" @args }
function global:xstart { Invoke-XKit "container-start" @args }
function global:xstop { Invoke-XKit "container-stop" @args }
function global:xlogs { Invoke-XKit "container-logs" @args }

# AI & Communication through MCP servers
function global:question { Invoke-XKit "ai-analyze" @args }
function global:explain { Invoke-XKit "ai-explain-code" @args }
function global:suggest { Invoke-XKit "ai-suggest" @args }
function global:tg { Invoke-XKit "telegram-send" @args }
function global:tg-error { Invoke-XKit "telegram-error" @args }

# Enhanced error handling with @xpilot integration
function global:xerr { Invoke-XKit "error-show" @args }
function global:xfix { Invoke-XKit "error-fix" @args }
function global:xpilot { Invoke-XKit "xpilot-analyze" @args }

# Development and debugging
function global:xdebug { Invoke-XKit "debug" @args }
function global:xconfig { Invoke-XKit "config" @args }
function global:xtest { Invoke-XKit "test-system" @args }

# Enhanced Python command with MCP integration
function global:xpython { Invoke-XKit "python-execute" @args }

# Modern, clean prompt for XKit v3.0
function global:prompt {
    $location = (Get-Location).Path.Replace($HOME, '~')
    
    # Show git branch if in git repo
    $branch = ""
    try {
        $gitBranch = git rev-parse --abbrev-ref HEAD 2>$null
        if ($gitBranch) { 
            $branch = " [$gitBranch]"
        }
    } catch {}
    
    # XKit v3.0 prompt with MCP indicator
    "PS $location$branch [MCP] > "
}

# Display startup message
Write-Host "XKit v3.0 Hybrid MCP Architecture loaded!" -ForegroundColor Green
Write-Host "Model Context Protocol integration active" -ForegroundColor Cyan
Write-Host "Plugin system ready | Event bus active" -ForegroundColor Yellow
Write-Host "Type 'xkit-help' for available commands" -ForegroundColor Blue

# Initialize XKit v3.0 system on first load
if (-not $global:XKitV3Loaded) {
    $global:XKitV3Loaded = $true
    Invoke-XKit "system-init" | Out-Null
}