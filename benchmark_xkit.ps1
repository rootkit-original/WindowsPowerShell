# 🏁 XKit PowerShell Benchmark Suite
# Compara performance entre v2.1.2 e v3.0-dev

param(
    [string]$TestType = "full",
    [int]$Iterations = 3
)

$ErrorActionPreference = "Continue"

# Configuração de cores
$colors = @{
    Success = "Green"
    Warning = "Yellow"
    Error   = "Red"
    Info    = "Cyan"
    Header  = "Magenta"
}

function Write-ColorOutput {
    param([string]$Message, [string]$Color = "White")
    if ($colors.ContainsKey($Color)) {
        Write-Host $Message -ForegroundColor $colors[$Color]
    } else {
        Write-Host $Message -ForegroundColor White
    }
}

function Get-SystemInfo {
    return @{
        PowerShellVersion = $PSVersionTable.PSVersion.ToString()
        OSVersion = [System.Environment]::OSVersion.VersionString
        ProcessorCount = [System.Environment]::ProcessorCount
        TotalMemory = [Math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 2)
        Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    }
}

function Measure-XKitCommand {
    param(
        [string]$Command,
        [string]$Version,
        [string]$ScriptPath
    )
    
    Write-ColorOutput "🏃‍♀️ Testando: $Command ($Version)" "Info"
    
    $results = @()
    
    for ($i = 1; $i -le $Iterations; $i++) {
        try {
            $startTime = Get-Date
            $startMemory = [GC]::GetTotalMemory($false)
            
            # Executar comando
            $output = & python $ScriptPath $Command.Split() 2>&1
            
            $endTime = Get-Date
            $endMemory = [GC]::GetTotalMemory($false)
            
            $executionTime = ($endTime - $startTime).TotalMilliseconds
            $memoryUsage = [Math]::Round(($endMemory - $startMemory) / 1MB, 2)
            
            $results += @{
                Iteration = $i
                ExecutionTime = $executionTime
                MemoryUsage = $memoryUsage
                OutputSize = if ($output) { $output.Length } else { 0 }
                Success = $LASTEXITCODE -eq 0
            }
            
            Start-Sleep -Milliseconds 100  # Pequena pausa entre iterações
            
        } catch {
            Write-ColorOutput "❌ Erro na iteração $i`: $($_.Exception.Message)" "Error"
            $results += @{
                Iteration = $i
                ExecutionTime = [double]::MaxValue
                MemoryUsage = 0
                OutputSize = 0
                Success = $false
            }
        }
    }
    
    # Calcular médias (excluindo falhas)
    $successResults = $results | Where-Object { $_.Success }
    
    if ($successResults.Count -gt 0) {
        $avgTime = ($successResults | Measure-Object ExecutionTime -Average).Average
        $avgMemory = ($successResults | Measure-Object MemoryUsage -Average).Average
        $avgOutput = ($successResults | Measure-Object OutputSize -Average).Average
        
        Write-ColorOutput "✅ $Command`: ${avgTime:F2}ms (${successResults.Count}/$Iterations sucessos)" "Success"
    } else {
        $avgTime = [double]::MaxValue
        $avgMemory = 0
        $avgOutput = 0
        Write-ColorOutput "❌ $Command`: Todas as execuções falharam" "Error"
    }
    
    return @{
        Command = $Command
        Version = $Version
        AverageTime = $avgTime
        AverageMemory = $avgMemory
        AverageOutput = $avgOutput
        Iterations = $Iterations
        Successes = $successResults.Count
        DetailedResults = $results
    }
}

function Switch-GitVersion {
    param([string]$Version)
    
    try {
        Write-ColorOutput "🔄 Mudando para versão: $Version" "Info"
        $result = git checkout $Version 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "✅ Checkout realizado: $Version" "Success"
            return $true
        } else {
            Write-ColorOutput "❌ Falha no checkout: $result" "Error"
            return $false
        }
    } catch {
        Write-ColorOutput "❌ Erro durante checkout: $($_.Exception.Message)" "Error"
        return $false
    }
}

function Compare-BenchmarkResults {
    param(
        [array]$V2Results,
        [array]$V3Results
    )
    
    $comparison = @{
        Summary = @{}
        Details = @()
    }
    
    $v2TotalTime = ($V2Results | Where-Object { $_.AverageTime -ne [double]::MaxValue } | Measure-Object AverageTime -Sum).Sum
    $v3TotalTime = ($V3Results | Where-Object { $_.AverageTime -ne [double]::MaxValue } | Measure-Object AverageTime -Sum).Sum
    
    $timeImprovement = if ($v2TotalTime -gt 0) { 
        [math]::Round((($v2TotalTime - $v3TotalTime) / $v2TotalTime) * 100, 2) 
    } else { 0 }
    
    $comparison.Summary = @{
        V2TotalTime = $v2TotalTime
        V3TotalTime = $v3TotalTime
        TimeImprovement = $timeImprovement
        V2Successes = ($V2Results | Measure-Object Successes -Sum).Sum
        V3Successes = ($V3Results | Measure-Object Successes -Sum).Sum
    }
    
    # Comparação detalhada
    for ($i = 0; $i -lt $V2Results.Count; $i++) {
        $v2 = $V2Results[$i]
        $v3 = $V3Results[$i]
        
        if ($v2.Command -eq $v3.Command) {
            $cmdTimeImprovement = if ($v2.AverageTime -gt 0 -and $v2.AverageTime -ne [double]::MaxValue) {
                [math]::Round((($v2.AverageTime - $v3.AverageTime) / $v2.AverageTime) * 100, 2)
            } else { 0 }
            
            $comparison.Details += @{
                Command = $v2.Command
                V2Time = $v2.AverageTime
                V3Time = $v3.AverageTime
                TimeImprovement = $cmdTimeImprovement
                V2Memory = $v2.AverageMemory
                V3Memory = $v3.AverageMemory
                V2Success = $v2.Successes
                V3Success = $v3.Successes
            }
        }
    }
    
    return $comparison
}

function Export-BenchmarkReport {
    param(
        [hashtable]$Comparison,
        [array]$V2Results,
        [array]$V3Results,
        [hashtable]$SystemInfo
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
    $reportFile = "benchmark_report_$timestamp.md"
    
    $report = @"
# 🏁 XKit PowerShell Benchmark Report

**Data:** $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
**Sistema:** $($SystemInfo.OSVersion)
**PowerShell:** $($SystemInfo.PowerShellVersion)
**CPU Cores:** $($SystemInfo.ProcessorCount)
**RAM Total:** $($SystemInfo.TotalMemory) GB

## 📊 Resumo Geral

| Métrica | v2.1.2 | v3.0-dev | Melhoria |
|---------|---------|----------|-----------|
| **Tempo Total** | $($Comparison.Summary.V2TotalTime.ToString("F2")) ms | $($Comparison.Summary.V3TotalTime.ToString("F2")) ms | $($Comparison.Summary.TimeImprovement)% |
| **Sucessos v2** | $($Comparison.Summary.V2Successes)/$($V2Results.Count * $Iterations) | - | - |
| **Sucessos v3** | - | $($Comparison.Summary.V3Successes)/$($V3Results.Count * $Iterations) | - |

## 🔍 Comparação Detalhada

| Comando | v2.1.2 (ms) | v3.0-dev (ms) | Melhoria | Sucessos v2 | Sucessos v3 |
|---------|-------------|---------------|-----------|-------------|-------------|
"@

    foreach ($detail in $Comparison.Details) {
        $v2TimeStr = if ($detail.V2Time -eq [double]::MaxValue) { "FALHA" } else { $detail.V2Time.ToString("F2") }
        $v3TimeStr = if ($detail.V3Time -eq [double]::MaxValue) { "FALHA" } else { $detail.V3Time.ToString("F2") }
        $improvementStr = if ($detail.TimeImprovement -ne 0) { "$($detail.TimeImprovement)%" } else { "N/A" }
        
        $report += "`n| ``$($detail.Command)`` | $v2TimeStr | $v3TimeStr | $improvementStr | $($detail.V2Success)/$Iterations | $($detail.V3Success)/$Iterations |"
    }
    
    $report += @"

## 🎯 Análise de Performance

### ⚡ Melhoria Geral: $($Comparison.Summary.TimeImprovement)%

"@

    if ($Comparison.Summary.TimeImprovement -gt 0) {
        $report += "✅ **Performance melhorada!** A versão v3.0 é mais rápida em média.`n"
    } elseif ($Comparison.Summary.TimeImprovement -lt 0) {
        $report += "⚠️ **Performance degradada.** A versão v3.0 está mais lenta em média.`n"
    } else {
        $report += "➡️ **Performance similar** entre as versões.`n"
    }
    
    $report += @"

### 🏗️ Arquitetura v3.0 Features
- **MCP Integration:** Model Context Protocol para extensibilidade
- **Plugin Hot-Reload:** Carregamento dinâmico de plugins
- **Event-Driven:** Arquitetura orientada a eventos
- **Hexagonal Architecture:** Separação limpa de responsabilidades
- **AI Integration:** Gemini 2.0 Flash integrado

### 📝 Notas
- Cada comando foi executado $Iterations vezes
- Médias calculadas apenas para execuções bem-sucedidas
- Tempos incluem inicialização do Python e carregamento do sistema

---
*Gerado pelo XKit PowerShell Benchmark Suite*
"@

    $report | Out-File -FilePath $reportFile -Encoding UTF8
    Write-ColorOutput "📊 Relatório salvo: $reportFile" "Success"
    
    return $reportFile
}

# ================================
# MAIN EXECUTION
# ================================

Write-ColorOutput "🚀 XKit PowerShell Benchmark Suite" "Header"
Write-ColorOutput "=" * 60 "Header"

$systemInfo = Get-SystemInfo
Write-ColorOutput "💻 Sistema: $($systemInfo.OSVersion)" "Info"
Write-ColorOutput "⚡ PowerShell: $($systemInfo.PowerShellVersion)" "Info"
Write-ColorOutput "🔄 Iterações por comando: $Iterations" "Info"

# Comandos de teste
$testCommands = @(
    "help",
    "ai analyze 'Exemplo Python'",
    "git-status", 
    "system-status",
    "analyze-project"
)

Write-ColorOutput "`n📋 Comandos de teste:" "Info"
$testCommands | ForEach-Object { Write-ColorOutput "  • $_" "Info" }

# Salvar branch atual
$currentBranch = git rev-parse --abbrev-ref HEAD
Write-ColorOutput "`n💾 Branch atual: $currentBranch" "Info"

$v2Results = @()
$v3Results = @()

try {
    # ================================
    # BENCHMARK v2.1.2
    # ================================
    
    Write-ColorOutput "`n📦 === TESTANDO v2.1.2 ===" "Header"
    
    if (Switch-GitVersion "v2.1.2") {
        foreach ($cmd in $testCommands) {
            $result = Measure-XKitCommand -Command $cmd -Version "v2.1.2" -ScriptPath "Scripts\xkit_main.py"
            $v2Results += $result
        }
    } else {
        Write-ColorOutput "❌ Não foi possível testar v2.1.2" "Error"
    }
    
    # ================================
    # VOLTAR PARA VERSÃO ATUAL
    # ================================
    
    Write-ColorOutput "`n🔄 Voltando para $currentBranch..." "Info"
    Switch-GitVersion $currentBranch | Out-Null
    
    # ================================
    # BENCHMARK v3.0-dev (ATUAL)
    # ================================
    
    Write-ColorOutput "`n🚀 === TESTANDO v3.0-dev (ATUAL) ===" "Header"
    
    foreach ($cmd in $testCommands) {
        $result = Measure-XKitCommand -Command $cmd -Version "v3.0-dev" -ScriptPath "Scripts\xkit_main.py"
        $v3Results += $result
    }
    
    # ================================
    # ANÁLISE E RELATÓRIO
    # ================================
    
    Write-ColorOutput "`n📊 === ANÁLISE DE RESULTADOS ===" "Header"
    
    $comparison = Compare-BenchmarkResults -V2Results $v2Results -V3Results $v3Results
    
    # Exibir resumo
    Write-ColorOutput "`n📈 RESUMO:" "Header"
    Write-ColorOutput "v2.1.2 Total: $($comparison.Summary.V2TotalTime.ToString('F2')) ms" "Info"
    Write-ColorOutput "v3.0-dev Total: $($comparison.Summary.V3TotalTime.ToString('F2')) ms" "Info"
    
    $improvementColor = if ($comparison.Summary.TimeImprovement -gt 0) { "Success" } 
                       elseif ($comparison.Summary.TimeImprovement -lt 0) { "Warning" } 
                       else { "Info" }
    
    Write-ColorOutput "Melhoria: $($comparison.Summary.TimeImprovement)%" $improvementColor
    
    # Gerar relatório
    $reportFile = Export-BenchmarkReport -Comparison $comparison -V2Results $v2Results -V3Results $v3Results -SystemInfo $systemInfo
    
    Write-ColorOutput "`n🎉 Benchmark concluído!" "Success"
    Write-ColorOutput "📊 Relatório: $reportFile" "Success"
    
    # Exibir top comandos com melhoria
    $topImprovements = $comparison.Details | Where-Object { $_.TimeImprovement -gt 0 } | Sort-Object TimeImprovement -Descending | Select-Object -First 3
    
    if ($topImprovements) {
        Write-ColorOutput "`n🥇 TOP MELHORIAS:" "Success"
        $topImprovements | ForEach-Object {
            Write-ColorOutput "  • $($_.Command): $($_.TimeImprovement)%" "Success"
        }
    }
    
} catch {
    Write-ColorOutput "`n❌ Erro durante benchmark: $($_.Exception.Message)" "Error"
} finally {
    # Garantir que voltamos para a branch original
    Write-ColorOutput "`n🔙 Garantindo volta para $currentBranch..." "Info"
    Switch-GitVersion $currentBranch | Out-Null
}

Write-ColorOutput "`n" + "=" * 60 "Header"
Write-ColorOutput "✅ Benchmark finalizado!" "Header"