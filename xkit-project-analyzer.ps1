# XKit Project Analyzer Commands
# Comandos PowerShell para análise de projetos .xkit

function global:Analyze-XKitProject {
    <#
    .SYNOPSIS
        Analisa um projeto .xkit e gera relatório de qualidade
    
    .DESCRIPTION
        Este comando analisa a estrutura de um projeto .xkit, verifica arquivos essenciais,
        calcula uma pontuação de qualidade e fornece sugestões de melhoria.
    
    .PARAMETER Path
        Caminho para o diretório do projeto (padrão: diretório atual)
    
    .EXAMPLE
        Analyze-XKitProject
        Analisa o projeto no diretório atual
    
    .EXAMPLE
        Analyze-XKitProject -Path "C:\MeuProjeto"
        Analisa um projeto específico
    #>
    param(
        [Parameter(Position = 0)]
        [string]$Path = (Get-Location)
    )
    
    Invoke-XKitPython "analyze-project" $Path
}

function global:Scan-XKitProjects {
    <#
    .SYNOPSIS
        Escaneia todos os projetos .xkit em um diretório
    
    .DESCRIPTION
        Procura recursivamente por diretórios .xkit e analisa todos os projetos encontrados,
        exibindo um resumo da qualidade de cada um.
    
    .PARAMETER Path
        Diretório base para busca (padrão: diretório atual)
    
    .EXAMPLE
        Scan-XKitProjects
        Escaneia projetos no diretório atual e subdiretórios
    
    .EXAMPLE
        Scan-XKitProjects -Path "C:\Projetos"
        Escaneia todos os projetos em uma pasta específica
    #>
    param(
        [Parameter(Position = 0)]
        [string]$Path = (Get-Location)
    )
    
    Invoke-XKitPython "scan-xkit-projects" $Path
}

function global:Get-XKitProjectScore {
    <#
    .SYNOPSIS
        Mostra apenas a pontuação de qualidade do projeto
    
    .DESCRIPTION
        Calcula e exibe a pontuação de qualidade de um projeto .xkit (0-10),
        útil para scripts e automação.
    
    .PARAMETER Path
        Caminho para o projeto (padrão: diretório atual)
    
    .EXAMPLE
        Get-XKitProjectScore
        Mostra a pontuação do projeto atual
    
    .EXAMPLE
        Get-XKitProjectScore -Path "C:\MeuProjeto"
        Mostra a pontuação de um projeto específico
    #>
    param(
        [Parameter(Position = 0)]
        [string]$Path = (Get-Location)
    )
    
    Invoke-XKitPython "project-score" $Path
}

# Aliases para comandos mais curtos
Set-Alias -Name "xkit-analyze" -Value "Analyze-XKitProject"
Set-Alias -Name "xkit-scan" -Value "Scan-XKitProjects" 
Set-Alias -Name "xkit-score" -Value "Get-XKitProjectScore"

# Exporta funções para uso global
Export-ModuleMember -Function Analyze-XKitProject, Scan-XKitProjects, Get-XKitProjectScore -Alias xkit-analyze, xkit-scan, xkit-score

# Mensagem de carregamento
Write-Host "🔍 XKit Project Analyzer loaded" -ForegroundColor Green
Write-Host "   Commands: Analyze-XKitProject, Scan-XKitProjects, Get-XKitProjectScore" -ForegroundColor Gray
Write-Host "   Aliases: xkit-analyze, xkit-scan, xkit-score" -ForegroundColor Gray