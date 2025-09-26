# AI Assistant Plugin for XKit
# Integration with XKit AI services

# Quick AI commands
function ai-help {
    param([string]$Question)
    
    if (-not $Question) {
        Write-Host "🤖 AI Assistant - Quick Help" -ForegroundColor Cyan
        Write-Host "Usage: ai-help 'your question here'" -ForegroundColor White
        Write-Host "Example: ai-help 'how to fix git merge conflict'" -ForegroundColor Gray
        return
    }
    
    Write-Host "🤖 Asking AI: $Question" -ForegroundColor Yellow
    
    try {
        # Call XKit compact application
        $pythonPath = Get-Command python -ErrorAction Stop | Select-Object -ExpandProperty Source
        $scriptPath = "$PSScriptRoot\..\..\Scripts\xkit_compact.py"
        
        if (Test-Path $scriptPath) {
            $response = & $pythonPath $scriptPath ai-context $Question 2>$null
            if ($LASTEXITCODE -eq 0 -and $response) {
                Write-Host "💡 AI Response:" -ForegroundColor Green
                Write-Host $response -ForegroundColor White
            } else {
                Write-Host "❌ AI service unavailable" -ForegroundColor Red
            }
        } else {
            Write-Host "❌ XKit AI service not found" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ Error calling AI service: $($_.Exception.Message)" -ForegroundColor Red
    }
}

function ai-analyze-code {
    param(
        [Parameter(Mandatory=$true)]
        [string]$FilePath
    )
    
    if (-not (Test-Path $FilePath)) {
        Write-Host "❌ File not found: $FilePath" -ForegroundColor Red
        return
    }
    
    Write-Host "🔍 Analyzing code: $FilePath" -ForegroundColor Yellow
    
    try {
        $fileContent = Get-Content $FilePath -Raw
        $prompt = "Analyze this code for potential issues, improvements, and best practices:`n`n$fileContent"
        
        ai-help $prompt
    } catch {
        Write-Host "❌ Error analyzing code: $($_.Exception.Message)" -ForegroundColor Red
    }
}

function ai-explain-error {
    param([string]$ErrorMessage)
    
    if (-not $ErrorMessage) {
        # Try to get the last error from PowerShell
        if ($Error -and $Error[0]) {
            $ErrorMessage = $Error[0].ToString()
        } else {
            Write-Host "❌ No error message provided and no recent errors found" -ForegroundColor Red
            Write-Host "Usage: ai-explain-error 'your error message'" -ForegroundColor White
            return
        }
    }
    
    Write-Host "🔍 Analyzing error..." -ForegroundColor Yellow
    
    $prompt = "Explain this error and provide solutions: $ErrorMessage"
    ai-help $prompt
}

function ai-suggest-command {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Task
    )
    
    Write-Host "🤔 Suggesting command for: $Task" -ForegroundColor Yellow
    
    $prompt = "What PowerShell or command line command should I use to: $Task. Provide the exact command and explain it."
    ai-help $prompt
}

function ai-status {
    Write-Host "🤖 AI Assistant Status" -ForegroundColor Cyan
    Write-Host "======================" -ForegroundColor Cyan
    
    # Check if XKit is available
    $scriptPath = "$PSScriptRoot\..\..\Scripts\xkit_compact.py"
    if (Test-Path $scriptPath) {
        Write-Host "✅ XKit AI Service: Available" -ForegroundColor Green
        Write-Host "📁 Script Path: $scriptPath" -ForegroundColor White
    } else {
        Write-Host "❌ XKit AI Service: Not Found" -ForegroundColor Red
    }
    
    # Check Python
    try {
        $pythonVersion = python --version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
        } else {
            Write-Host "❌ Python: Not Available" -ForegroundColor Red
        }
    } catch {
        Write-Host "❌ Python: Not Found" -ForegroundColor Red
    }
    
    Write-Host "" -ForegroundColor White
    Write-Host "💡 Available Commands:" -ForegroundColor Cyan
    Write-Host "  ai-help 'question'       - Ask AI a question" -ForegroundColor White
    Write-Host "  ai-analyze-code file.py  - Analyze code file" -ForegroundColor White  
    Write-Host "  ai-explain-error 'msg'   - Explain an error" -ForegroundColor White
    Write-Host "  ai-suggest-command 'task' - Get command suggestions" -ForegroundColor White
}

# Export aliases
New-Alias -Name "ai" -Value "ai-help" -Force -Scope Global
New-Alias -Name "aicode" -Value "ai-analyze-code" -Force -Scope Global
New-Alias -Name "aierror" -Value "ai-explain-error" -Force -Scope Global
New-Alias -Name "aicmd" -Value "ai-suggest-command" -Force -Scope Global

# Plugin metadata
$PLUGIN_NAME = "ai-assistant"
$PLUGIN_AUTHOR = "XKit Team"
$PLUGIN_VERSION = "1.0.0" 
$PLUGIN_DESCRIPTION = "AI-powered development assistance"

Write-Verbose "✅ Loaded plugin: $PLUGIN_NAME v$PLUGIN_VERSION"