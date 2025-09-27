# XKit Project Analyzer - Simple Version
# Follows XKit documentation pattern: PowerShell wrapper calls Python

function global:Analyze-XKitProject {
    <#
    .SYNOPSIS
        Analisa um projeto .xkit
    .PARAMETER Path
        Caminho do projeto (padrão: atual)
    #>
    param([string]$Path = (Get-Location))
    
    # Follow XKit pattern: minimal PS wrapper calling Python
    Invoke-XKitPython "analyze-project" $Path
}

function global:Scan-XKitProjects {
    <#
    .SYNOPSIS
        Escaneia projetos .xkit
    .PARAMETER Path
        Caminho base (padrão: atual)
    #>
    param([string]$Path = (Get-Location))
    
    Invoke-XKitPython "scan-xkit-projects" $Path
}

function global:Get-XKitProjectScore {
    <#
    .SYNOPSIS
        Score do projeto .xkit
    .PARAMETER Path
        Caminho do projeto (padrão: atual)
    #>
    param([string]$Path = (Get-Location))
    
    Invoke-XKitPython "project-score" $Path
}

# Aliases
Set-Alias -Name "xkit-analyze" -Value "Analyze-XKitProject"
Set-Alias -Name "xkit-scan" -Value "Scan-XKitProjects"
Set-Alias -Name "xkit-score" -Value "Get-XKitProjectScore"

Write-Host "🔍 XKit Project Analyzer carregado" -ForegroundColor Green