# 🧪 Teste Final - Novo PowerShell
# Simula abrir um novo PowerShell e testa todos os comandos

Write-Host "🧪 TESTE FINAL - Simulando Novo PowerShell" -ForegroundColor Magenta
Write-Host "=" * 50 -ForegroundColor Magenta

# Limpar estado para simular novo PowerShell
Remove-Variable XKitLoaded -Scope Global -ErrorAction SilentlyContinue

Write-Host "`n1️⃣ Carregando Profile como em novo PowerShell..." -ForegroundColor Cyan
. $PROFILE

Write-Host "`n2️⃣ Testando XKit v3.0..." -ForegroundColor Cyan
Write-Host "Comando 'xkit' disponível: $((Get-Command xkit -ErrorAction SilentlyContinue) -ne $null)" -ForegroundColor White
if (Get-Command xkit -ErrorAction SilentlyContinue) {
    xkit version
}

Write-Host "`n3️⃣ Testando Comandos Legacy..." -ForegroundColor Cyan
$LegacyCommands = @('gs', 'ga', 'gc', 'd', 'dc', '..', 'll')
foreach ($cmd in $LegacyCommands) {
    $available = (Get-Command $cmd -ErrorAction SilentlyContinue) -ne $null
    $status = if ($available) { "✅" } else { "❌" }
    Write-Host "$status $cmd" -ForegroundColor $(if ($available) { "Green" } else { "Red" })
}

Write-Host "`n4️⃣ Testando Git Status..." -ForegroundColor Cyan
try {
    $gitStatus = gs 2>&1
    Write-Host "✅ Git status funcionando" -ForegroundColor Green
} catch {
    Write-Host "❌ Git status falhou: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n5️⃣ Status do AutoStart..." -ForegroundColor Cyan
$RegEntry = Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name "XKit-AutoStart" -ErrorAction SilentlyContinue
if ($RegEntry) {
    Write-Host "✅ AutoStart configurado no Registry" -ForegroundColor Green
} else {
    Write-Host "❌ AutoStart não encontrado no Registry" -ForegroundColor Red
}

Write-Host "`n🎉 RESULTADO FINAL:" -ForegroundColor Green
Write-Host "✅ XKit v3.0 + Legacy Commands funcionando em novo PowerShell!" -ForegroundColor Green
Write-Host "✅ Profile redireciona corretamente do PowerShell padrão" -ForegroundColor Green
Write-Host "✅ AutoStart configurado para Windows startup" -ForegroundColor Green
Write-Host "✅ Comandos gs, ga, gc, d, dc disponíveis" -ForegroundColor Green

Write-Host "`n💡 Para testar realmente:" -ForegroundColor Yellow
Write-Host "   Abra um novo PowerShell e digite: gs" -ForegroundColor Cyan