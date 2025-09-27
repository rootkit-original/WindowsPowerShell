# 🏁 XKit Simple Benchmark
# Compara performance simples entre versões

Write-Host "🚀 XKit Benchmark Simples" -ForegroundColor Magenta
Write-Host "=" * 40 -ForegroundColor Magenta

# Comandos de teste
$commands = @(
    "help",
    "system-status",
    "git-status"
)

# Função para medir comando
function Measure-Command {
    param($cmd, $version)
    
    Write-Host "🏃‍♂️ Testando: $cmd ($version)" -ForegroundColor Cyan
    
    $times = @()
    for ($i = 1; $i -le 3; $i++) {
        try {
            $measure = Measure-Command { 
                python Scripts\xkit_main.py $cmd.Split() *>$null 
            }
            $times += $measure.TotalMilliseconds
            Write-Host "  Execução $i`: $($measure.TotalMilliseconds.ToString('F1'))ms" -ForegroundColor Gray
        }
        catch {
            Write-Host "  Execução $i`: ERRO" -ForegroundColor Red
            $times += 9999
        }
    }
    
    $avg = ($times | Measure-Object -Average).Average
    Write-Host "  ✅ Média: $($avg.ToString('F1'))ms" -ForegroundColor Green
    
    return @{
        Command = $cmd
        Version = $version
        Average = $avg
        Times = $times
    }
}

# Salvar branch atual
$currentBranch = git rev-parse --abbrev-ref HEAD
Write-Host "💾 Branch atual: $currentBranch" -ForegroundColor Yellow

$results = @{
    v2 = @()
    v3 = @()
}

try {
    # Teste v2.1.2
    Write-Host "`n📦 === TESTANDO v2.1.2 ===" -ForegroundColor Magenta
    git checkout v2.1.2 *>$null
    
    foreach ($cmd in $commands) {
        $result = Measure-Command -cmd $cmd -version "v2.1.2"
        $results.v2 += $result
    }
    
    # Voltar para atual
    Write-Host "`n🔄 Voltando para versão atual..." -ForegroundColor Yellow
    git checkout $currentBranch *>$null
    
    # Teste v3.0-dev
    Write-Host "`n🚀 === TESTANDO v3.0-dev ===" -ForegroundColor Magenta
    
    foreach ($cmd in $commands) {
        $result = Measure-Command -cmd $cmd -version "v3.0-dev"
        $results.v3 += $result
    }
    
    # Comparação
    Write-Host "`n📊 === COMPARAÇÃO ===" -ForegroundColor Magenta
    Write-Host ""
    Write-Host "| Comando | v2.1.2 | v3.0-dev | Melhoria |" -ForegroundColor White
    Write-Host "|---------|---------|----------|----------|" -ForegroundColor White
    
    $totalV2 = 0
    $totalV3 = 0
    
    for ($i = 0; $i -lt $commands.Count; $i++) {
        $v2Time = $results.v2[$i].Average
        $v3Time = $results.v3[$i].Average
        
        $improvement = if ($v2Time -gt 0) { 
            [math]::Round((($v2Time - $v3Time) / $v2Time) * 100, 1) 
        } else { 0 }
        
        $improvementStr = if ($improvement -gt 0) { "+$improvement%" } 
                         elseif ($improvement -lt 0) { "$improvement%" } 
                         else { "0%" }
        
        $color = if ($improvement -gt 0) { "Green" } 
                elseif ($improvement -lt 0) { "Red" } 
                else { "Yellow" }
        
        Write-Host "| $($commands[$i]) | $($v2Time.ToString('F1'))ms | $($v3Time.ToString('F1'))ms | $improvementStr |" -ForegroundColor $color
        
        $totalV2 += $v2Time
        $totalV3 += $v3Time
    }
    
    $totalImprovement = if ($totalV2 -gt 0) { 
        [math]::Round((($totalV2 - $totalV3) / $totalV2) * 100, 1) 
    } else { 0 }
    
    Write-Host ""
    Write-Host "🎯 RESULTADO GERAL:" -ForegroundColor Magenta
    Write-Host "v2.1.2 Total: $($totalV2.ToString('F1'))ms" -ForegroundColor White
    Write-Host "v3.0-dev Total: $($totalV3.ToString('F1'))ms" -ForegroundColor White
    
    if ($totalImprovement -gt 0) {
        Write-Host "✅ Melhoria: +$totalImprovement%" -ForegroundColor Green
        Write-Host "🚀 v3.0 é mais rápido!" -ForegroundColor Green
    } elseif ($totalImprovement -lt 0) {
        Write-Host "⚠️ Degradação: $totalImprovement%" -ForegroundColor Red
        Write-Host "🐌 v3.0 está mais lento" -ForegroundColor Red
    } else {
        Write-Host "➡️ Performance similar" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "❌ Erro: $($_.Exception.Message)" -ForegroundColor Red
} finally {
    # Garantir que voltamos para branch original
    git checkout $currentBranch *>$null
}

Write-Host "`n" + "=" * 40 -ForegroundColor Magenta
Write-Host "✅ Benchmark concluído!" -ForegroundColor Green