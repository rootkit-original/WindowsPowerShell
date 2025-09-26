# Oh My XKit - Error Handler Plugin (Python-backed)
# Simplified PowerShell wrapper that calls Python backend

# Global error tracking (minimal PS state)
$global:XKIT_ERROR_COUNT = 0

# Main error handling function - delegates to Python
function global:Invoke-XKitErrorHandler {
    param(
        [string]$ErrorMessage,
        [string]$Command = "",
        [string]$Context = ""
    )
    
    $global:XKIT_ERROR_COUNT++
    
    # Call Python backend for full error handling
    python "$PSScriptRoot\..\..\Scripts\xkit_main.py" "handle-error" $ErrorMessage $Command $Context
}

# Shortcut commands that call Python
function global:xerr { 
    python "$PSScriptRoot\..\..\Scripts\xkit_main.py" "show-error-details"
}

function global:xfix { 
    python "$PSScriptRoot\..\..\Scripts\xkit_main.py" "retry-error"
}

function global:xtest-error { 
    param([string]$Type = "command")
    python "$PSScriptRoot\..\..\Scripts\xkit_main.py" "test-error" $Type
}

# Enhanced command wrappers with error detection
function global:xgit {
    param([Parameter(ValueFromRemainingArguments)]$args)
    try {
        git @args
        if ($LASTEXITCODE -and $LASTEXITCODE -ne 0) {
            Invoke-XKitErrorHandler "Git command failed with exit code $LASTEXITCODE" "git $($args -join ' ')" "Git operation"
        }
    }
    catch {
        Invoke-XKitErrorHandler $_.Exception.Message "git $($args -join ' ')" "Git operation"
    }
}

function global:xpython {
    param([Parameter(ValueFromRemainingArguments)]$args)
    try {
        python @args
        if ($LASTEXITCODE -and $LASTEXITCODE -ne 0) {
            Invoke-XKitErrorHandler "Python command failed with exit code $LASTEXITCODE" "python $($args -join ' ')" "Python execution"
        }
    }
    catch {
        Invoke-XKitErrorHandler $_.Exception.Message "python $($args -join ' ')" "Python execution"
    }
}

Write-Host "[LOADED] XKit Error Handler (Python-backed) loaded" -ForegroundColor Green