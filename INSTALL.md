# XKit v2.1 - Guia de Instalação

## 🚀 Instalação Rápida

### Pré-requisitos

Certifique-se de ter:

- **Windows 10/11**
- **PowerShell 5.1+**
- **Python 3.11+**
- **Git** (opcional mas recomendado)
- **Podman ou Docker** (opcional)

### Passo 1: Baixar os Arquivos

1. **Clone ou baixe** os arquivos para:
   ```powershell
   $HOME\Documents\WindowsPowerShell\
   ```

2. **Estrutura esperada**:
   ```
   WindowsPowerShell/
   ├── Microsoft.PowerShell_profile.ps1
   ├── gh-copilot.ps1
   └── Scripts/
       ├── xkit_compact.py
       └── xkit/
   ```

### Passo 2: Configurar Variáveis de Ambiente

Edite o arquivo `Microsoft.PowerShell_profile.ps1` e configure:

```powershell
# XKit v2.1 Environment Variables
$env:GEMINI_API_KEY = 'sua_api_key_aqui'
$env:TELEGRAM_TOKEN = 'seu_token_aqui'
$env:ADMIN_ID = 'seu_id_aqui'
```

### Passo 3: Instalar Dependências Python

```powershell
pip install requests pathlib dataclasses
```

### Passo 4: Testar Instalação

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