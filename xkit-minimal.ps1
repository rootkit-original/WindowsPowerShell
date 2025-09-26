# XKit - Ultra-Minimal PowerShell Profile
# All logic is in Python. This is just a thin wrapper.

# XKit Python Bridge - Single function to rule them all
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
        Write-Host "ERROR: XKit Python main not found at: $PythonMain" -ForegroundColor Red
        return $false
    }
    
    # Execute Python with error handling
    try {
        # Set environment variables for UTF-8 and API keys
        $env:PYTHONIOENCODING = "utf-8"
        $env:GEMINI_API_KEY = "AIzaSyCvzBo-iK-KBdwedZYSHyoHcMzsYqEArC4"
        $env:TELEGRAM_TOKEN = "8477588651:AAGaQLuk7hsfW5UWiNEnpGWK2Z6rRLg9A-s"
        $env:ADMIN_ID = "7335391186"
        
        # Set console encoding to UTF-8 for better emoji support
        [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
        
        # Build and execute command
        $cmd = @("python", $PythonMain, $Action) + $Arguments
        & $cmd[0] $cmd[1..($cmd.Length-1)]
        
        if ($LASTEXITCODE -and $LASTEXITCODE -ne 0) {
            Write-Host "ERROR: XKit Python failed with exit code: $LASTEXITCODE" -ForegroundColor Red
            return $false
        }
        # Don't return anything for successful execution to avoid "True" output
    }
    catch {
        Write-Host "ERROR: XKit execution failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Essential commands - all delegate to Python
function global:xkit-help { Invoke-XKit "show-help" @args }
function global:xkit-version { Invoke-XKit "show-version" @args }
function global:xkit-status { Invoke-XKit "show-status" @args }
function global:xkit-reload { 
    Write-Host "🔄 Reloading XKit profile..." -ForegroundColor Yellow
    . $PROFILE
    Write-Host "✅ XKit profile reloaded!" -ForegroundColor Green
}

# Git shortcuts with error handling
function global:gst { try { git status } catch { Invoke-XKit "handle-error" $_.Exception.Message "git status" "Git operation" } }
function global:ga { try { git add @args } catch { Invoke-XKit "handle-error" $_.Exception.Message "git add" "Git operation" } }
function global:gc { try { git commit @args } catch { Invoke-XKit "handle-error" $_.Exception.Message "git commit" "Git operation" } }
function global:gp { try { git push @args } catch { Invoke-XKit "handle-error" $_.Exception.Message "git push" "Git operation" } }
function global:glog { try { git log --oneline -10 @args } catch { Invoke-XKit "handle-error" $_.Exception.Message "git log" "Git operation" } }
function global:gb { try { git branch @args } catch { Invoke-XKit "handle-error" $_.Exception.Message "git branch" "Git operation" } }
function global:gco { try { git checkout @args } catch { Invoke-XKit "handle-error" $_.Exception.Message "git checkout" "Git operation" } }

# Docker/Podman shortcuts with error handling  
function global:d { try { podman @args } catch { Invoke-XKit "handle-error" $_.Exception.Message "podman" "Container operation" } }
function global:dps { try { podman ps @args } catch { Invoke-XKit "handle-error" $_.Exception.Message "podman ps" "Container operation" } }
function global:di { try { podman images @args } catch { Invoke-XKit "handle-error" $_.Exception.Message "podman images" "Container operation" } }

# AI & Communication (keep Out-Null for these)
function global:question { Invoke-XKit "ask-ai" @args }
function global:tg { Invoke-XKit "send-telegram" @args | Out-Null }

# Error handling commands
function global:xerr { Invoke-XKit "show-error-details" @args }
function global:xfix { Invoke-XKit "retry-error" @args }
function global:xtest-error { Invoke-XKit "test-error" @args }

# Enhanced commands with error handling
function global:xgit { 
    try { 
        git @args
        if ($LASTEXITCODE -ne 0) { Invoke-XKit "handle-error" "Git command failed with exit code $LASTEXITCODE" "git $($args -join ' ')" "Enhanced Git" }
    } catch { 
        Invoke-XKit "handle-error" $_.Exception.Message "git $($args -join ' ')" "Enhanced Git" 
    }
}

function global:xpython { 
    try { 
        python @args
        if ($LASTEXITCODE -ne 0) { Invoke-XKit "handle-error" "Python command failed with exit code $LASTEXITCODE" "python $($args -join ' ')" "Enhanced Python" }
    } catch { 
        Invoke-XKit "handle-error" $_.Exception.Message "python $($args -join ' ')" "Enhanced Python" 
    }
}

# Simple prompt
function global:prompt {
    $location = (Get-Location).Path.Replace($HOME, '~')
    $branch = ""
    try {
        $gitBranch = git rev-parse --abbrev-ref HEAD 2>$null
        if ($gitBranch -and $LASTEXITCODE -eq 0) {
            $branch = " [$gitBranch]"
        }
    } catch {}
    
    Write-Host "$env:USERNAME@$env:COMPUTERNAME" -NoNewline -ForegroundColor Green
    Write-Host $branch -NoNewline -ForegroundColor Yellow
    Write-Host " ~$(Split-Path $location -Leaf)" -NoNewline -ForegroundColor Blue
    return " $ "
}

# Welcome message (only once)
if (-not $global:XKitLoaded) {
    $global:XKitLoaded = $true
    Invoke-XKit "show-welcome" | Out-Null
}