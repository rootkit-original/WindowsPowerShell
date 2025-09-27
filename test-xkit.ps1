# Test XKit Profile Loading
Write-Host "🧪 Testando carregamento do XKit Profile..." -ForegroundColor Cyan

# Reload profile
. "$PSScriptRoot\Microsoft.PowerShell_profile.ps1"

Write-Host "`n🔍 Testando comandos..." -ForegroundColor Yellow

# Test new XKit commands
Write-Host "`n1. Testando XKit v3.0:" -ForegroundColor Cyan
xkit version

# Test legacy commands
Write-Host "`n2. Testando comandos legacy:" -ForegroundColor Cyan
Write-Host "Comando 'gs' disponível: $((Get-Command gs -ErrorAction SilentlyContinue) -ne $null)" -ForegroundColor White
Write-Host "Comando 'ga' disponível: $((Get-Command ga -ErrorAction SilentlyContinue) -ne $null)" -ForegroundColor White
Write-Host "Comando 'gc' disponível: $((Get-Command gc -ErrorAction SilentlyContinue) -ne $null)" -ForegroundColor White

# List all git-related functions
Write-Host "`n3. Comandos git disponíveis:" -ForegroundColor Cyan
Get-Command g* -CommandType Function -ErrorAction SilentlyContinue | Select-Object Name | Format-Table -AutoSize

Write-Host "`n✅ Testes concluídos!" -ForegroundColor Green