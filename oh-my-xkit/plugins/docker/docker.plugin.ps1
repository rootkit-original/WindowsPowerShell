# Docker Plugin for XKit
# Container management functionality

# Docker aliases
function d { docker @args }
function dc { docker-compose @args }
function dps { docker ps @args }
function dpsa { docker ps -a @args }
function di { docker images @args }
function drun { docker run @args }
function dexec { docker exec @args }
function dlogs { docker logs @args }

# Podman aliases (if available)
if (Get-Command podman -ErrorAction SilentlyContinue) {
    function p { podman @args }
    function pc { podman-compose @args }
    function pps { podman ps @args }
    function ppsa { podman ps -a @args }
    function pi { podman images @args }
    function prun { podman run @args }
    function pexec { podman exec @args }
    function plogs { podman logs @args }
}

# Container management functions
function docker-cleanup {
    Write-Host "🧹 Docker Cleanup Starting..." -ForegroundColor Yellow
    
    Write-Host "🗑️  Removing stopped containers..." -ForegroundColor Cyan
    docker container prune -f
    
    Write-Host "🗑️  Removing unused images..." -ForegroundColor Cyan  
    docker image prune -f
    
    Write-Host "🗑️  Removing unused volumes..." -ForegroundColor Cyan
    docker volume prune -f
    
    Write-Host "🗑️  Removing unused networks..." -ForegroundColor Cyan
    docker network prune -f
    
    Write-Host "✅ Docker cleanup complete!" -ForegroundColor Green
}

function podman-cleanup {
    if (-not (Get-Command podman -ErrorAction SilentlyContinue)) {
        Write-Host "❌ Podman not found!" -ForegroundColor Red
        return
    }
    
    Write-Host "🧹 Podman Cleanup Starting..." -ForegroundColor Yellow
    
    Write-Host "🗑️  Removing stopped containers..." -ForegroundColor Cyan
    podman container prune -f
    
    Write-Host "🗑️  Removing unused images..." -ForegroundColor Cyan
    podman image prune -f
    
    Write-Host "🗑️  Removing unused volumes..." -ForegroundColor Cyan  
    podman volume prune -f
    
    Write-Host "✅ Podman cleanup complete!" -ForegroundColor Green
}

function container-info {
    Write-Host "🐳 Container Environment Info" -ForegroundColor Cyan
    Write-Host "=============================" -ForegroundColor Cyan
    
    # Check Docker
    if (Get-Command docker -ErrorAction SilentlyContinue) {
        try {
            $dockerVersion = docker --version 2>$null
            Write-Host "✅ Docker: $dockerVersion" -ForegroundColor Green
            
            $runningContainers = (docker ps -q).Count
            $totalContainers = (docker ps -a -q).Count
            Write-Host "📊 Containers: $runningContainers running, $totalContainers total" -ForegroundColor White
            
            $images = (docker images -q).Count
            Write-Host "🏗️  Images: $images" -ForegroundColor White
        } catch {
            Write-Host "❌ Docker daemon not running" -ForegroundColor Red
        }
    } else {
        Write-Host "❌ Docker not installed" -ForegroundColor Red
    }
    
    # Check Docker Compose
    if (Get-Command docker-compose -ErrorAction SilentlyContinue) {
        $composeVersion = docker-compose --version 2>$null
        Write-Host "✅ Docker Compose: $composeVersion" -ForegroundColor Green
    } else {
        Write-Host "❌ Docker Compose not installed" -ForegroundColor Red
    }
    
    Write-Host "" -ForegroundColor White
    
    # Check Podman
    if (Get-Command podman -ErrorAction SilentlyContinue) {
        try {
            $podmanVersion = podman --version 2>$null
            Write-Host "✅ Podman: $podmanVersion" -ForegroundColor Green
            
            $runningPods = (podman ps -q).Count
            $totalPods = (podman ps -a -q).Count  
            Write-Host "📊 Containers: $runningPods running, $totalPods total" -ForegroundColor White
            
            $podImages = (podman images -q).Count
            Write-Host "🏗️  Images: $podImages" -ForegroundColor White
        } catch {
            Write-Host "❌ Podman service not running" -ForegroundColor Red
        }
    } else {
        Write-Host "❌ Podman not installed" -ForegroundColor Red  
    }
    
    # Check Podman Compose
    if (Get-Command podman-compose -ErrorAction SilentlyContinue) {
        $podmanComposeVersion = podman-compose --version 2>$null
        Write-Host "✅ Podman Compose: $podmanComposeVersion" -ForegroundColor Green
    } else {
        Write-Host "❌ Podman Compose not installed" -ForegroundColor Red
    }
}

function docker-quick-run {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Image,
        [string]$Command = "/bin/bash",
        [switch]$Interactive
    )
    
    $runArgs = @("run", "--rm")
    
    if ($Interactive) {
        $runArgs += @("-it")
    }
    
    $runArgs += @($Image)
    
    if ($Command -ne "/bin/bash") {
        $runArgs += $Command
    }
    
    Write-Host "🚀 Running: docker $($runArgs -join ' ')" -ForegroundColor Yellow
    docker @runArgs
}

# Export aliases
New-Alias -Name "dclean" -Value "docker-cleanup" -Force -Scope Global
New-Alias -Name "pclean" -Value "podman-cleanup" -Force -Scope Global
New-Alias -Name "cinfo" -Value "container-info" -Force -Scope Global
New-Alias -Name "dqr" -Value "docker-quick-run" -Force -Scope Global

# Plugin metadata
$PLUGIN_NAME = "docker"
$PLUGIN_AUTHOR = "XKit Team"
$PLUGIN_VERSION = "1.0.0"
$PLUGIN_DESCRIPTION = "Docker and Podman container management"

Write-Verbose "✅ Loaded plugin: $PLUGIN_NAME v$PLUGIN_VERSION"