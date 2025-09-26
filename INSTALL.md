# XKit v2.1 - Guia de Instalação

## 🚀 Instalação Rápida (Arquitetura Ultra-Minimal)

### Pré-requisitos

Certifique-se de ter:

- **Windows 10/11**
- **PowerShell 5.1+**
- **Python 3.11+**
- **Git** (opcional mas recomendado)

### Passo 1: Estrutura de Arquivos

1. **Clone ou copie** os arquivos para:
   ```
   $HOME\Documents\WindowsPowerShell\
   ```

2. **Estrutura necessária** (ultra-minimal):
   ```
   WindowsPowerShell/
   ├── Microsoft.PowerShell_profile.ps1  # Ultra-minimal loader
   ├── xkit-minimal.ps1                  # ⭐ Single bridge file
   └── Scripts/
       ├── xkit_main.py                  # ⭐ Python entry point
       └── xkit/                         # Clean Architecture
           ├── domain/
           ├── application/
           └── infrastructure/
   ```

### Passo 2: Configurar API Keys (Opcional)

Edite `xkit-minimal.ps1` e configure suas chaves:

```powershell
# API Keys (optional)
$env:GEMINI_API_KEY = 'your_gemini_api_key'
$env:TELEGRAM_TOKEN = 'your_telegram_bot_token'
$env:ADMIN_ID = 'your_telegram_user_id'
```

### Passo 3: Testar Instalação

```powershell
# Reiniciar PowerShell ou recarregar perfil
. $PROFILE

# Testar comando básico
xkit-version

# Testar sistema completo
xtest-error
```

## ✅ Validação da Instalação

### Verificações Básicas

```powershell
# 1. Verificar se perfil carregou
$global:XKitLoaded                    # Should return: True

# 2. Testar comando principal
xkit-help                            # Should show command list

# 3. Verificar encoding UTF-8
$env:PYTHONIOENCODING               # Should return: utf-8
```

### Teste de Funcionalidades

```powershell
# Testar interface rica com emojis
xkit-status

# Testar sistema de error handling
xtest-error

# Testar commands shortcuts
ga .                                # git add . with error handling
```

## 🔧 Configuração Avançada

### Customizar API Keys

Se você quiser usar IA e notificações Telegram:

1. **Gemini AI** (opcional):
   - Obtenha chave em: https://ai.google.dev/
   - Configure: `$env:GEMINI_API_KEY = 'sua_chave'`

2. **Telegram Bot** (opcional):
   - Crie bot via @BotFather
   - Configure: `$env:TELEGRAM_TOKEN = 'bot_token'`
   - Configure: `$env:ADMIN_ID = 'your_telegram_id'`

### Personalizar Comandos

Para adicionar comandos customizados:

1. **Edite** `xkit-minimal.ps1` - adicione wrapper PowerShell
2. **Edite** `xkit_main.py` - adicione lógica Python
3. **Siga** Clean Architecture - mantenha separação de responsabilidades

## 🐛 Resolução de Problemas

### Problema: Profile não carrega

```powershell
# Verificar se arquivo existe
Test-Path $PROFILE                   # Should return: True

# Carregar manualmente
. $PROFILE

# Verificar execution policy
Get-ExecutionPolicy
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser  # If needed
```

### Problema: Python não encontrado

```powershell
# Verificar Python
python --version                     # Should show Python 3.11+

# Se não funcionar, instalar Python 3.11+ e reiniciar terminal
```

### Problema: Emojis não aparecem

```powershell
# Sistema configura automaticamente, mas se necessário:
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"
```

### Problema: Comandos não funcionam

```powershell
# Verificar se xkit-minimal.ps1 existe
Test-Path "C:\Users\$env:USERNAME\Documents\WindowsPowerShell\xkit-minimal.ps1"

# Verificar se Python main existe  
Test-Path "C:\Users\$env:USERNAME\Documents\WindowsPowerShell\Scripts\xkit_main.py"

# Testar Python entry point manualmente
python "C:\Users\$env:USERNAME\Documents\WindowsPowerShell\Scripts\xkit_main.py" show-version
```

## ⚡ Performance e Otimização

### Startup Rápido

O sistema é otimizado para:
- **PowerShell minimal** - Carregamento instantâneo
- **Python lazy-loading** - Carrega apenas quando necessário  
- **Cache inteligente** - Detecta mudanças automaticamente
- **UTF-8 nativo** - Emojis funcionam sem overhead

### Uso de Memória

- **Footprint baixo** - PowerShell praticamente vazio
- **Python modular** - Carrega apenas módulos necessários
- **Clean Architecture** - Dependências bem definidas

## 🎯 Próximos Passos

Após instalação bem-sucedida:

1. **Leia** [USAGE.md](USAGE.md) - Manual completo de uso
2. **Teste** `xtest-error` - Simular erros para conhecer o sistema
3. **Configure** APIs (opcional) - Para funcionalidades avançadas
4. **Explore** comandos - Use `xkit-help` para ver opções

## 🏗️ Desenvolvimento

Para contribuir ou customizar:

1. **Estude** [ARCHITECTURE.md](ARCHITECTURE.md) - Documentação técnica  
2. **Veja** [.github/copilot-instructions.md](.github/copilot-instructions.md) - Instruções desenvolvimento
3. **Siga** Clean Architecture - Separação domain/application/infrastructure
4. **Teste** modificações com `xtest-error` antes de usar

---

**XKit v2.1** - Instalação simples, arquitetura poderosa! 🚀

1. **Feche** o PowerShell atual
2. **Abra** um novo PowerShell
3. **Você deve ver**:
   ```
   Usuario@COMPUTADOR ~/
   $ 
   ```

4. **Teste os comandos**:
   ```powershell
   xkit-help
   xkit-status
   ```

## 🔧 Instalação Avançada

### Configuração de Container Engine

#### Para Podman:
```powershell
# Instalar via Chocolatey
choco install podman-desktop

# Ou baixar do site oficial
# https://podman.io/getting-started/installation
```

#### Para podman-compose:
```powershell
pip install podman-compose
```

### Configuração de API Keys

#### Gemini AI:
1. Acesse https://aistudio.google.com/app/apikey
2. Crie uma nova API key
3. Configure no perfil PowerShell

#### Telegram Bot:
1. Converse com @BotFather no Telegram
2. Crie um novo bot com `/newbot`
3. Obtenha o token e configure
4. Obtenha seu ID com @userinfobot

### Verificação da Instalação

Execute o validador:

```powershell
python Scripts\xkit-final-validator.py
```

Deve exibir:
```
🎉 XKit v2.1 COMPACTO FUNCIONANDO PERFEITAMENTE!
```

## 🛠️ Configuração Personalizada

### Customizar Prompt

Edite a função `prompt` no arquivo de perfil:

```powershell
function prompt {
    $user = $env:USERNAME
    $computer = $env:COMPUTERNAME
    # Customize aqui...
}
```

### Adicionar Comandos Personalizados

Crie funções no perfil:

```powershell
function meu-comando {
    python "$PSScriptRoot\Scripts\xkit_compact.py" custom-action
}
```

### Configurar Containers

Para projetos específicos, crie aliases:

```powershell
function meu-projeto-up {
    podman-compose -f meu-docker-compose.yml up -d
}
```

## ❌ Solução de Problemas

### Python não encontrado
```powershell
# Verificar instalação
python --version

# Instalar se necessário
winget install Python.Python.3.12
```

### XKit não carrega
```powershell
# Verificar permissões
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Recarregar perfil
. $PROFILE
```

### Comandos não funcionam
```powershell
# Verificar arquivo de perfil
Test-Path $PROFILE

# Criar se não existir
New-Item -Path $PROFILE -Type File -Force
```

### AI não responde
- Verificar conexão com internet
- Validar API key do Gemini
- Conferir variáveis de ambiente

### Containers não detectados
- Verificar instalação do Podman/Docker
- Testar comando: `podman --version`
- Configurar PATH se necessário

## 🔄 Atualização

Para atualizar o XKit:

1. **Backup** das configurações pessoais
2. **Baixe** a nova versão
3. **Substitua** os arquivos
4. **Mantenha** suas configurações de API
5. **Reinicie** o PowerShell

## 📞 Suporte

Se encontrar problemas:

1. **Consulte** este guia primeiro
2. **Execute** `xkit-status` para diagnóstico
3. **Verifique** os logs de erro
4. **Use** `xkit-ai "descreva o problema"` para ajuda

---

**Próximo**: [USAGE.md](USAGE.md) - Como usar o XKit