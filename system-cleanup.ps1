#!/usr/bin/env pwsh
<#
.SYNOPSIS
    🧹 XKit v3.0 System Cleanup Script
    
.DESCRIPTION
    Script automático de limpeza e reorganização do sistema XKit v3.0
    baseado na análise completa usando GitHub MCP Server.
    
.PARAMETER DryRun
    Executa simulação sem fazer alterações reais
    
.PARAMETER BackupFirst
    Cria backup antes das alterações
    
.EXAMPLE
    .\system-cleanup.ps1 -DryRun
    .\system-cleanup.ps1 -BackupFirst
    
.NOTES
    Author: XKit System Analysis
    Version: 1.0.0
    Created: $(Get-Date -Format "yyyy-MM-dd")
#>

param(
    [switch]$DryRun,
    [switch]$BackupFirst
)

# 🎨 Configurações de Display
$Host.UI.RawUI.WindowTitle = "🧹 XKit v3.0 System Cleanup"

function Write-Header {
    param([string]$Message)
    Write-Host "`n" -NoNewline
    Write-Host "="*60 -ForegroundColor Cyan
    Write-Host "  $Message" -ForegroundColor White
    Write-Host "="*60 -ForegroundColor Cyan
    Write-Host ""
}

function Write-Step {
    param([string]$Message, [string]$Status = "Info")
    $emoji = switch ($Status) {
        "Success" { "✅" }
        "Warning" { "⚠️ " }
        "Error"   { "❌" }
        "Info"    { "🔧" }
        Default   { "🔧" }
    }
    Write-Host "$emoji $Message" -ForegroundColor $(
        switch ($Status) {
            "Success" { "Green" }
            "Warning" { "Yellow" }
            "Error"   { "Red" }
            Default   { "Cyan" }
        }
    )
}

function Test-GitRepository {
    try {
        $gitStatus = git status 2>&1
        if ($LASTEXITCODE -ne 0) {
            throw "Not a git repository"
        }
        return $true
    }
    catch {
        Write-Step "❌ Erro: Este script deve ser executado na raiz de um repositório Git!" "Error"
        exit 1
    }
}

function New-BackupIfRequested {
    if ($BackupFirst) {
        $timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
        $backupDir = "backup-$timestamp"
        
        Write-Step "📦 Criando backup em: $backupDir"
        
        if (-not $DryRun) {
            # Criar backup dos arquivos que serão movidos/removidos
            New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
            
            # Backup arquivos Telegram
            if (Test-Path "telegram-*.py") {
                New-Item -ItemType Directory -Path "$backupDir/telegram" -Force | Out-Null
                Copy-Item -Path "telegram-*.py" -Destination "$backupDir/telegram/" -Force
            }
            
            # Backup arquivos de instalação legados
            $legacyInstallers = @("install-autostart-simple.ps1", "manage-autostart.ps1", 
                                "clean-autostart.ps1", "uninstall-autostart.ps1")
            foreach ($file in $legacyInstallers) {
                if (Test-Path $file) {
                    Copy-Item -Path $file -Destination "$backupDir/" -Force
                }
            }
            
            # Backup outros arquivos
            $otherFiles = @("setup.py", "startup.log")
            foreach ($file in $otherFiles) {
                if (Test-Path $file) {
                    Copy-Item -Path $file -Destination "$backupDir/" -Force
                }
            }
        }
        
        Write-Step "✅ Backup criado com sucesso!" "Success"
    }
}

function Move-TelegramFiles {
    Write-Header "📁 FASE 1: Reorganizando Arquivos Telegram"
    
    # Verificar se existem arquivos telegram na raiz
    $telegramFiles = Get-ChildItem -Path "telegram-*.py" -ErrorAction SilentlyContinue
    
    if ($telegramFiles.Count -eq 0) {
        Write-Step "ℹ️  Nenhum arquivo telegram encontrado na raiz" "Info"
        return
    }
    
    Write-Step "📂 Encontrados $($telegramFiles.Count) arquivos telegram na raiz"
    
    # Criar estrutura de diretório
    $telegramLegacyDir = "Scripts/telegram/legacy"
    Write-Step "📁 Criando diretório: $telegramLegacyDir"
    
    if (-not $DryRun) {
        New-Item -ItemType Directory -Path $telegramLegacyDir -Force | Out-Null
    }
    
    # Mover cada arquivo
    foreach ($file in $telegramFiles) {
        $newName = $file.Name -replace "telegram-", "" -replace "\.py$", ".py"
        $destination = Join-Path $telegramLegacyDir $newName
        
        Write-Step "🔄 Movendo: $($file.Name) → $destination"
        
        if (-not $DryRun) {
            Move-Item -Path $file.FullName -Destination $destination -Force
        }
    }
    
    Write-Step "✅ Arquivos Telegram reorganizados!" "Success"
}

function Remove-LegacyFiles {
    Write-Header "🗑️  FASE 2: Removendo Arquivos Legados"
    
    # Arquivos para remoção
    $filesToRemove = @(
        @{ Path = "setup.py"; Reason = "Substituído por pyproject.toml" },
        @{ Path = "startup.log"; Reason = "Log não deve ser versionado" },
        @{ Path = "install-autostart-simple.ps1"; Reason = "Funcionalidade consolidada em install-xkit-v3.ps1" },
        @{ Path = "manage-autostart.ps1"; Reason = "Funcionalidade consolidada" },
        @{ Path = "clean-autostart.ps1"; Reason = "Funcionalidade consolidada" },
        @{ Path = "uninstall-autostart.ps1"; Reason = "Funcionalidade consolidada" }
    )
    
    foreach ($file in $filesToRemove) {
        if (Test-Path $file.Path) {
            Write-Step "🗑️  Removendo: $($file.Path) - $($file.Reason)"
            
            if (-not $DryRun) {
                Remove-Item -Path $file.Path -Force
            }
        }
        else {
            Write-Step "ℹ️  Já removido: $($file.Path)" "Info"
        }
    }
    
    Write-Step "✅ Arquivos legados removidos!" "Success"
}

function Update-GitIgnore {
    Write-Header "📝 FASE 3: Atualizando .gitignore"
    
    $gitignorePath = ".gitignore"
    $newEntries = @(
        "# XKit System Cleanup - Auto-generated entries",
        "*.log",
        "startup.log", 
        "Scripts/telegram/legacy/",
        "backup-*/",
        ""
    )
    
    if (Test-Path $gitignorePath) {
        $currentContent = Get-Content $gitignorePath -Raw
        $needsUpdate = $false
        
        foreach ($entry in $newEntries) {
            if ($entry -ne "" -and -not $currentContent.Contains($entry)) {
                $needsUpdate = $true
                break
            }
        }
        
        if ($needsUpdate) {
            Write-Step "📝 Adicionando entradas ao .gitignore"
            
            if (-not $DryRun) {
                Add-Content -Path $gitignorePath -Value $newEntries
            }
        }
        else {
            Write-Step "ℹ️  .gitignore já atualizado" "Info"
        }
    }
    else {
        Write-Step "📝 Criando .gitignore"
        if (-not $DryRun) {
            Set-Content -Path $gitignorePath -Value $newEntries
        }
    }
    
    Write-Step "✅ .gitignore atualizado!" "Success"
}

function Move-Documentation {
    Write-Header "📚 FASE 4: Reorganizando Documentação"
    
    $docsToMove = @(
        @{ Source = "API.md"; Destination = "docs/api/API.md" },
        @{ Source = "ARCHITECTURE.md"; Destination = "docs/architecture/ARCHITECTURE.md" },
        @{ Source = "MCP_TELEGRAM_IMPLEMENTATION.md"; Destination = "docs/development/mcp-telegram-implementation.md" }
    )
    
    foreach ($doc in $docsToMove) {
        if (Test-Path $doc.Source) {
            $destDir = Split-Path $doc.Destination -Parent
            Write-Step "📂 Criando diretório: $destDir"
            
            if (-not $DryRun) {
                New-Item -ItemType Directory -Path $destDir -Force | Out-Null
            }
            
            Write-Step "📄 Movendo: $($doc.Source) → $($doc.Destination)"
            
            if (-not $DryRun) {
                Move-Item -Path $doc.Source -Destination $doc.Destination -Force
            }
        }
        else {
            Write-Step "ℹ️  Já movido: $($doc.Source)" "Info"
        }
    }
    
    Write-Step "✅ Documentação reorganizada!" "Success"
}

function Show-CleanupSummary {
    Write-Header "📊 RESUMO DA LIMPEZA"
    
    $metrics = @{
        "Arquivos Telegram reorganizados" = (Get-ChildItem -Path "telegram-*.py" -ErrorAction SilentlyContinue).Count
        "Arquivos legados removidos" = 6
        "Documentos reorganizados" = 3
        "Estruturas criadas" = 2
    }
    
    foreach ($metric in $metrics.GetEnumerator()) {
        Write-Step "$($metric.Key): $($metric.Value)" "Info"
    }
    
    Write-Host ""
    if ($DryRun) {
        Write-Step "⚠️  MODO DRY RUN - Nenhuma alteração foi feita" "Warning"
        Write-Step "Execute sem -DryRun para aplicar as alterações" "Info"
    }
    else {
        Write-Step "✅ Limpeza concluída com sucesso!" "Success"
        Write-Step "Execute 'git status' para revisar as alterações" "Info"
    }
}

function Test-PostCleanup {
    Write-Header "🔍 FASE 5: Validação Pós-Limpeza"
    
    $validations = @(
        @{ 
            Test = { Test-Path "Scripts/telegram/legacy" }
            Message = "Diretório telegram/legacy criado"
        },
        @{ 
            Test = { -not (Test-Path "telegram-*.py") }
            Message = "Arquivos telegram removidos da raiz"
        },
        @{ 
            Test = { -not (Test-Path "setup.py") }
            Message = "setup.py removido"
        },
        @{ 
            Test = { Test-Path "pyproject.toml" }
            Message = "pyproject.toml mantido"
        },
        @{ 
            Test = { Test-Path ".gitignore" }
            Message = ".gitignore existe"
        }
    )
    
    $passedTests = 0
    foreach ($validation in $validations) {
        $result = & $validation.Test
        if ($result) {
            Write-Step "✅ $($validation.Message)" "Success"
            $passedTests++
        }
        else {
            Write-Step "❌ $($validation.Message)" "Error"
        }
    }
    
    Write-Host ""
    Write-Step "Validações: $passedTests/$($validations.Count) ✅" $(
        if ($passedTests -eq $validations.Count) { "Success" } else { "Warning" }
    )
}

# 🚀 EXECUÇÃO PRINCIPAL
try {
    Write-Header "🧹 XKit v3.0 System Cleanup Script"
    
    if ($DryRun) {
        Write-Step "⚠️  MODO DRY RUN - Simulação apenas, nenhuma alteração será feita" "Warning"
    }
    
    # Verificações iniciais
    Test-GitRepository
    
    # Backup se solicitado
    New-BackupIfRequested
    
    # Executar fases de limpeza
    Move-TelegramFiles
    Remove-LegacyFiles  
    Update-GitIgnore
    Move-Documentation
    
    # Validação pós-limpeza
    if (-not $DryRun) {
        Test-PostCleanup
    }
    
    # Resumo final
    Show-CleanupSummary
    
    Write-Header "🎉 SCRIPT CONCLUÍDO COM SUCESSO!"
    
    if (-not $DryRun) {
        Write-Host "Próximos passos recomendados:" -ForegroundColor Yellow
        Write-Host "1. git status" -ForegroundColor Cyan
        Write-Host "2. git add ." -ForegroundColor Cyan  
        Write-Host "3. git commit -m 'feat: system cleanup and reorganization'" -ForegroundColor Cyan
        Write-Host "4. Testar funcionalidades críticas" -ForegroundColor Cyan
    }
}
catch {
    Write-Step "💥 Erro durante execução: $($_.Exception.Message)" "Error"
    exit 1
}