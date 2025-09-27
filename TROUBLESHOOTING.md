# 🚑 Troubleshooting - XKit v3.0.0

## 🔍 Problemas Comuns v3.0.0

### 🚫 XKit não inicia

**Problema**: `python: O termo não é reconhecido` ou `xkit_main.py: ImportError`

**Solução**:
```powershell
# 1. Verificar Python 3.11+
python --version
py --version

# 2. Tentar execução direta
cd "$env:USERPROFILE\Documents\WindowsPowerShell"
python Scripts\xkit_main.py --version

# 3. Se Import Error, instalar dependências
pip install -r Scripts\requirements.txt
```

### 🔌 MCP Servers não conectam

**Problema**: `MCP server connection failed` ou `xkit mcp-list` vazio

**Solução**:
```powershell
# Verificar configuração MCP
xkit mcp-status
Get-Content Scripts\xkit\mcp\config.json

# Testar conectividade individual
xkit mcp-test core-server

# Reinicar MCP client
xkit mcp-restart
```

### 🧩 Plugins não carregam

**Problema**: `Plugin load failed` ou funcionalidades ausentes

**Solução**:
```powershell
# Verificar plugins
xkit plugin-status
xkit plugin-list

# Recarregar plugin específico
xkit plugin-reload git-plugin

# Logs detalhados
xkit system-logs --plugins
```

### 🤖 IA não funciona

**Problema**: `AI analysis failed` ou `Gemini API error`

**Solução**:
```powershell
# Verificar chave API
$env:GEMINI_API_KEY
echo $env:GEMINI_API_KEY

# Testar conexão
xkit ai analyze "test"

# Verificar quota API
xkit ai-status
```

### 📱 Telegram não envia

**Problema**: `Telegram send failed` ou bot não responde

**Solução**:
```powershell
# Verificar configuração
$env:TELEGRAM_TOKEN
$env:ADMIN_ID

# Testar bot
xkit tg-status
xkit tg-send "teste"

# Verificar bot ativo no Telegram
```

### 🚀 AutoStart não funciona

**Problema**: XKit não carrega automaticamente no Windows

**Solução**:
```powershell
# Verificar configuração
.\manage-autostart.ps1 status

# Reconfigurar AutoStart
.\clean-autostart.ps1
.\install-autostart-simple.ps1

# Verificar logs
Get-Content startup.log -Tail 20

# Testar manualmente
powershell -File xkit-startup-autostart.ps1
```

### ⚡ Performance Issues

**Problema**: XKit startup lento ou comandos demorados

**Solução**:
```powershell
# Verificar métricas
xkit --version  # Mostra tempo de startup
xkit system-status

# Análise IA de performance
xkit ai analyze "System performance analysis"

# Verificar Python dependencies
pip list | grep -E "(gemini|telegram|mcp)"

# Limpar cache se necessário
xkit system-cache-clear
```

### 🔧 PowerShell Compatibility

**Problema**: Diferenças entre PowerShell 5.1 e 7+

**Solução**:
```powershell
# Verificar versão PowerShell
$PSVersionTable

# Para PowerShell 5.1 (UTF-8)
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001

# Para PowerShell 7+ (já configurado)
# Usar Windows Terminal para melhor suporte emoji

# Testar comandos legacy
gs  # Deve funcionar em ambas as versões
```

### 📊 Logs e Diagnóstico

**Problema**: Precisar de informações de debug

**Solução**:
```powershell
# Logs detalhados
xkit system-logs

# Último erro ocorrido
xkit error-last

# Export de configuração
xkit system-export-config

# Informações do ambiente
xkit system-info
```

## 🛠️ Diagnóstico Avançado

### 🔍 Análise Completa do Sistema

```powershell
# Script de diagnóstico completo
@'
Write-Host "=== XKit v3.0.0 Diagnostic Report ===" -ForegroundColor Cyan
Write-Host ""

# Versão e ambiente
Write-Host "1. Version Info:" -ForegroundColor Yellow
python --version
$PSVersionTable.PSVersion
xkit --version

Write-Host "`n2. XKit Status:" -ForegroundColor Yellow
xkit system-status

Write-Host "`n3. MCP Status:" -ForegroundColor Yellow  
xkit mcp-status

Write-Host "`n4. Plugin Status:" -ForegroundColor Yellow
xkit plugin-status

Write-Host "`n5. Last Error:" -ForegroundColor Yellow
xkit error-last

Write-Host "`n6. Environment:" -ForegroundColor Yellow
echo "GEMINI_API_KEY: $($env:GEMINI_API_KEY -ne $null)"
echo "TELEGRAM_TOKEN: $($env:TELEGRAM_TOKEN -ne $null)"
echo "ADMIN_ID: $env:ADMIN_ID"

Write-Host "`n=== End Diagnostic ===" -ForegroundColor Cyan
'@ | Invoke-Expression
```

## 🔧 Recovery Solutions

### 🆘 Reinstalação Completa

```powershell
# 1. Backup configurações
Copy-Item .env .env.backup -ErrorAction SilentlyContinue

# 2. Remover AutoStart
.\clean-autostart.ps1

# 3. Backup profile personalizado (se houver)
Copy-Item $PROFILE "$env:TEMP\profile_backup.ps1" -ErrorAction SilentlyContinue

# 4. Reinstalar XKit
git pull origin develop --force
python Scripts\xkit_main.py --reset

# 5. Reconfigurar
.\install-autostart-simple.ps1
```

### 🔄 Reset Factory

```powershell
# Reset completo para configurações padrão
xkit system-reset-factory

# Ou manualmente:
Remove-Item Scripts\xkit\config\* -Recurse -Force
python Scripts\xkit_main.py --init
```

## 🆘 Suporte

### 📞 Onde buscar ajuda:

1. **📖 Documentação**: Leia [INSTALL.md](INSTALL.md), [USAGE.md](USAGE.md), [ARCHITECTURE.md](ARCHITECTURE.md)
2. **🤖 IA Integrada**: Use `xkit ai analyze "describe my problem"` ou `question "como resolver..."`
3. **🐛 GitHub Issues**: [Reportar bugs](https://github.com/rootkit-original/WindowsPowerShell/issues)
4. **💬 GitHub Discussions**: [Discussões da comunidade](https://github.com/rootkit-original/WindowsPowerShell/discussions)
5. **📱 Telegram**: Configure bot para suporte remoto

### 📊 Informações para Support

Quando reportar problemas, inclua:

```powershell
# Execute e copie a saída:
xkit system-info
xkit --version
xkit error-last
```

---

**💡 Dica**: A maioria dos problemas podem ser resolvidos com `xkit ai analyze "my error message"` - a IA consegue diagnosticar e sugerir soluções!