# XKit Command Wrapper - Simple Python-backed version

# Basic command wrappers
function global:xnpm {
    param([Parameter(ValueFromRemainingArguments)]$args)
    try {
        npm @args
        if ($LASTEXITCODE -and $LASTEXITCODE -ne 0) {
            python "$PSScriptRoot\..\..\Scripts\xkit_main.py" "handle-error" "NPM command failed with exit code $LASTEXITCODE" "npm $($args -join ' ')" "NPM operation"
        }
    }
    catch {
        python "$PSScriptRoot\..\..\Scripts\xkit_main.py" "handle-error" $_.Exception.Message "npm $($args -join ' ')" "NPM operation"
    }
}

function global:xdocker {
    param([Parameter(ValueFromRemainingArguments)]$args)
    try {
        docker @args
        if ($LASTEXITCODE -and $LASTEXITCODE -ne 0) {
            python "$PSScriptRoot\..\..\Scripts\xkit_main.py" "handle-error" "Docker command failed with exit code $LASTEXITCODE" "docker $($args -join ' ')" "Docker operation"
        }
    }
    catch {
        python "$PSScriptRoot\..\..\Scripts\xkit_main.py" "handle-error" $_.Exception.Message "docker $($args -join ' ')" "Docker operation"
    }
}

Write-Host "[LOADED] XKit Command Wrappers (Python-backed) loaded" -ForegroundColor Green