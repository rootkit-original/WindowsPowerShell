# AI Assistant Plugin - Simple version

function global:ai {
    param([string]$Question)
    
    if (-not $Question) {
        Write-Host "Usage: ai 'your question'" -ForegroundColor Yellow
        return
    }
    
    try {
        $scriptPath = "$PSScriptRoot\..\..\Scripts\xkit_compact.py"
        if (Test-Path $scriptPath) {
            python $scriptPath ai-context $Question
        } else {
            Write-Host "XKit AI service not found" -ForegroundColor Red
        }
    } catch {
        Write-Host "Error calling AI service: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Verbose "AI Assistant plugin loaded"