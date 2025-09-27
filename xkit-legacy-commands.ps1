# XKit Legacy Commands - Minimal Load
# Carrega apenas as funções essenciais do Oh-My-XKit sem prompt customizado

Write-Host "🎨 Carregando comandos legacy do XKit..." -ForegroundColor Magenta

# Git shortcuts
function global:gs { git status $args }
function global:ga { git add $args }
function global:gaa { git add --all }
function global:gc { git commit $args }
function global:gcm { git commit -m $args }
function global:gp { git push $args }
function global:gl { git pull $args }
function global:gco { git checkout $args }
function global:gb { git branch $args }
function global:gd { git diff $args }
function global:glog { git log --oneline --graph --decorate $args }

# Docker shortcuts
function global:d { docker $args }
function global:dc { docker-compose $args }
function global:dps { docker ps $args }
function global:di { docker images $args }

# Quick navigation
function global:.. { Set-Location .. }
function global:... { Set-Location ..\.. }
function global:.... { Set-Location ..\..\.. }

# Quick file operations
function global:ll { Get-ChildItem -Force $args }
function global:la { Get-ChildItem -Force -Hidden $args }

# XKit specific
function global:reload-profile { . $PROFILE }
function global:edit-profile { code $PROFILE }

Write-Host "✅ Comandos legacy carregados (gs, ga, gc, d, dc, etc.)" -ForegroundColor Green