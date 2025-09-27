# 📖 Guia de Instalação - XKit v3.0.0

> **Instruções passo-a-passo para instalar o XKit v3.0.0 com Hybrid MCP Architecture no Windows**

## 🚦 Pré-requisitos

- **Windows 10/11** (Build 19041 ou superior recomendado)
- **PowerShell 5.1+** ou **PowerShell 7+** (ambos suportados)
- **Python 3.11+** ([Download aqui](https://python.org)) - *Requerido para Hybrid MCP Architecture*
- **Git** ([Download aqui](https://git-scm.com))
- **Windows Terminal** (opcional, mas recomendado para melhor experiência com emojis)

## 🚀 Instalação Rápida

```powershell
# 1. Clone o repositório
git clone https://github.com/rootkit-original/WindowsPowerShell.git "$env:USERPROFILE\Documents\WindowsPowerShell"

# 2. Entre no diretório
cd "$env:USERPROFILE\Documents\WindowsPowerShell"

# 3. Execute o XKit (auto-instala dependências)
python Scripts\xkit_main.py

# 4. Recarregue o PowerShell
powershell
```

### 📦 Instalação Automática (Recomendada)

```powershell
# Execute o script de instalação automática
.\install-xkit-v3.ps1

# Configure o AutoStart (opcional)
.\install-autostart-simple.ps1
```

## ✅ Verificação

```powershell
# Verificar se XKit está funcionando
xkit --version
xkit --help

# Testar comandos principais
xkit git-status
xkit ai analyze "Hello World"

# Legacy commands (compatibilidade v2.1)
gs      # git status
ga .    # git add .
```

## 🔧 Configurações Opcionais

### 🤖 Integração AI e Telegram

```powershell
# Configurar chaves API (arquivo .env ou variáveis de ambiente)
$env:GEMINI_API_KEY = "sua-chave-gemini-2.0-flash"
$env:TELEGRAM_TOKEN = "seu-token-bot-telegram"  
$env:ADMIN_ID = "seu-telegram-user-id"

# Ou criar arquivo .env no diretório do XKit
@'
GEMINI_API_KEY=sua-chave-gemini-2.0-flash
TELEGRAM_TOKEN=seu-token-bot-telegram
ADMIN_ID=seu-telegram-user-id
'@ | Out-File -Encoding UTF8 .env
```

### 🐳 Container Support

```powershell
# Podman (recomendado para desenvolvimento)
winget install -e --id RedHat.Podman

# Ou Docker
winget install -e --id Docker.DockerDesktop
```

### 🚀 Sistema AutoStart

```powershell
# Configurar XKit para iniciar com Windows
.\install-autostart-simple.ps1

# Gerenciar configurações de AutoStart
.\manage-autostart.ps1 status
.\manage-autostart.ps1 enable
.\manage-autostart.ps1 disable
```

### 🔌 MCP Servers Externos (Avançado)

```powershell
# Configurar MCP servers externos
# Editar Scripts/xkit/mcp/config.json
# Adicionar servers personalizados no formato MCP
```

## 🔍 Troubleshooting

### Execution Policy
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Python não encontrado
```powershell
# Verificar versão Python
python --version  # Deve ser 3.11+
py --version

# Se não funcionar, reinstalar Python com PATH
```

### Profile não carrega automaticamente
```powershell
# Verificar profile
Test-Path $PROFILE

# Recarregar manualmente
. "$env:USERPROFILE\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1"

# Executar XKit diretamente
python "$env:USERPROFILE\Documents\WindowsPowerShell\Scripts\xkit_main.py"
```

### MCP Servers não conectam
```powershell
# Verificar logs MCP
xkit mcp-status

# Testar conectividade
xkit mcp-test

# Verificar configuração
Get-Content Scripts\xkit\mcp\config.json
```

### Emojis não aparecem (PowerShell 5.1)
```powershell
# Configurar console para UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001

# Recomendação: usar Windows Terminal
```

## 🔄 Atualização

```powershell
cd "$env:USERPROFILE\Documents\WindowsPowerShell"

# Fazer backup das configurações
Copy-Item .env .env.backup -ErrorAction SilentlyContinue

# Atualizar código
git pull origin develop

# Executar migração se necessário
python Scripts\xkit_main.py --migrate

# Recarregar profile
powershell
```

## 🗑️ Desinstalação

```powershell
# Remover AutoStart
.\clean-autostart.ps1

# Remover diretório (backup .env primeiro!)
Remove-Item "$env:USERPROFILE\Documents\WindowsPowerShell" -Recurse -Force
```

---

## 📚 Próximos Passos

1. **📖 Leia o [USAGE.md](USAGE.md)** - Guia completo de comandos
2. **🏗️ Veja [ARCHITECTURE.md](ARCHITECTURE.md)** - Entenda a arquitetura
3. **🤖 Configure IA** - Integre Gemini e Telegram
4. **🔌 Explore MCP** - Adicione servers externos
5. **🚀 Configure AutoStart** - Inicie automático com Windows

**Pronto! Seu ambiente XKit v3.0.0 está configurado! 🎉**