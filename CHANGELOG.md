# 📝 Changelog - XKit v2.1

## [2.1.2] - 2025-09-26

### 🐛 Bug Fixes
- README.md corrigido (conteúdo duplicado/corrompido removido)
- Documentação reorganizada e limpa
- Badges de versão atualizadas para v2.1.2

### 📚 Documentation
- README.md completamente reescrito com estrutura clara
- Seções de arquitetura e desenvolvimento melhoradas
- Links e referências organizados

## [2.1.1] - 2025-09-26

### 📚 Documentation  
- Documentação completa recriada do zero
- Comandos padronizados documentados

## [2.1.0] - 2025-09-26

### 🎯 BREAKING CHANGES
- Comandos padronizados com prefixo 'x': gst→xstatus, ga→xadd, gc→xcommit, gp→xpush, glog→xlog, gb→xbranch, gco→xcheckout, d→xpodman, dps→xcontainers, di→ximages

### ✨ Features
- Clean Architecture completa (Domain/Application/Infrastructure)
- Error handling inteligente com sistema @xpilot
- Configuração UTF-8 automática para emojis
- Integração Telegram e Gemini AIV
- Sistema de comandos transparente PowerShell→Python

### 🗑️ Removed
- Código legacy: xkit_compact.py, xkit-config.ps1, Scripts/tools/

### 🐛 Bug Fixes
- Resolvido conflito gl vs Get-Location
- Corrigida saída "True" indesejada
- Configuração UTF-8 otimizada
