# XKit v2.1 - Guia de Uso

## 🎯 Visão Geral

O XKit v2.1 usa arquitetura Python-first com ponte PowerShell ultra-minimal. Todos os comandos são implementados em Python com Clean Architecture.

## 📋 Comandos Disponíveis

### 🛠️ Comandos Principais

```powershell
# Informações e Ajuda
xkit-help          # Lista todos os comandos disponíveis
xkit-status        # Status detalhado do ambiente atual
xkit-version       # Versão do XKit

# Error Handling (@xpilot Agent)
xtest-error        # Simular erro para testar sistema
xerr               # Ver detalhes do último erro
xfix               # Tentar resolver erro automaticamente

# Inteligência Artificial
question "pergunta"  # Fazer pergunta ao Gemini AI
tg "mensagem"       # Enviar mensagem via Telegram
```

### 🐍 Comandos Git com Error Handling

```powershell
# Git shortcuts com tratamento de erros integrado
ga .               # git add .
gc "msg"          # git commit -m "msg"  
gp                # git push
gl                # git log --oneline -10
gb                # git branch
gco branch        # git checkout branch

# Enhanced git command (with full error handling)
xgit status       # Git com @xpilot error handling
```

### 🐳 Comandos Docker com Error Handling

```powershell
# Docker shortcuts com tratamento de erros
d ps              # docker ps
dps               # docker ps  
di                # docker images

# Enhanced docker command
xdocker ps        # Docker com @xpilot error handling
```

### 🐍 Python com Error Handling

```powershell
# Enhanced python command
xpython script.py  # Python com @xpilot error handling
```

## 🤖 Sistema @xpilot Error Handling

### Como Funciona

1. **Detecção Automática**: Comandos enhanced (`xgit`, `xdocker`, `xpython`) detectam erros
2. **Análise IA**: Python AI agent analisa o erro usando padrões conhecidos
3. **Git Integration**: Sistema cria branch de erro automaticamente se necessário
4. **Sugestões**: Fornece sugestões contextuais e possíveis auto-fixes
5. **Workflow**: Usuário pode aceitar correções ou continuar manualmente

### Testando o Sistema

```powershell
# Testar diferentes tipos de erro
xtest-error                    # Erro genérico (comando não encontrado)
xtest-error syntax            # Erro de sintaxe
xtest-error access            # Erro de acesso/permissão
xtest-error file              # Arquivo não encontrado
xtest-error command           # Comando não reconhecido
```

### Comandos de Recovery

```powershell
xerr               # Ver detalhes completos do último erro
xfix               # Tentar resolver automaticamente
xtest-error        # Simular novos erros para teste
```

## 🎨 Interface Rica

### Welcome Screen

Ao iniciar o PowerShell, você verá:

```text
🚀 XKit - Ambiente de desenvolvimento ativo
==================================================
📁 Projeto: WindowsPowerShell
📖 XKit v2.1 - Kit de Desenvolvimento Windows Inteligente
💭 > **Sistema inteligente com AI e interface compacta estilo oh-my-zsh**
🛠️ Tecnologias: Python, PowerShell, Git
🌿 Branch: master (17 mudanças)
🐳 Container: Podman disponível

💡 Digite 'xkit-help' para ver comandos disponíveis
==================================================
🪟 📁WindowsPowerShell 🌿master ±17 📦podman 🐍💙📝
   ⚠️  2 anomalia(s) detectada(s)
   💡 xkit-help para comandos
```

### Status Compact

Interface ultra-compacta mostra:
- 🪟 **Windows** indicator
- 📁 **Projeto atual**
- 🌿 **Git branch** e mudanças  
- 📦 **Container engine** disponível
- 🐍💙📝 **Tecnologias** detectadas
- ⚠️ **Anomalias** se houver

## 🔧 Configuração

### Variáveis de Ambiente

Edite as configurações em `xkit-minimal.ps1`:

```powershell
# API Keys (hard-coded for simplicity)
$env:GEMINI_API_KEY = 'your_gemini_api_key'
$env:TELEGRAM_TOKEN = 'your_telegram_bot_token'
$env:ADMIN_ID = 'your_telegram_user_id'

# Encoding para emojis (automatically set)
$env:PYTHONIOENCODING = "utf-8"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

### Arquivos Esperados

O sistema detecta automaticamente tecnologias baseado nos arquivos:

**Python Projects:**
- `requirements.txt` - Lista de dependências
- `pyproject.toml` - Configuração moderna Python  
- `setup.py` - Script tradicional de instalação

**Node.js Projects:**
- `package.json` - Configuração do projeto

**Docker Projects:**
- `Dockerfile` - Definição da imagem
- `docker-compose.yml` - Orquestração de containers

## 🚨 Detecção de Anomalias

O sistema detecta automaticamente:

### ⚠️ Projetos com Muitas Mudanças
```text
🚨 XKit Alert - 14:16:18
📁 Projeto: xAntivirus
📝 Muitas mudanças não commitadas: 28
```

### ⚠️ Projetos sem Configuração
```text
⚠️ Projeto Python sem arquivo de configuração
```
**Solução**: Criar `requirements.txt` ou `pyproject.toml`

### ⚠️ Outros Problemas
- Containers parados inesperadamente
- Dependências em falta
- Problemas de permissão
- Comandos não encontrados

## 🎯 Exemplos Práticos

### Workflow Típico de Desenvolvimento

```powershell
# 1. Ver status do projeto
xkit-status

# 2. Se houver anomalias, investigar
xerr

# 3. Trabalhar normalmente com error handling
xgit status
xgit add .
xgit commit -m "feat: nova funcionalidade"

# 4. Se der erro, o @xpilot analisa automaticamente
xfix  # Tentar resolver automaticamente

# 5. Fazer perguntas para IA quando necessário
question "como otimizar este código Python?"

# 6. Enviar notificações importantes
tg "Deploy realizado com sucesso!"
```

### Simulação de Erros para Teste

```powershell
# Testar sistema de error handling
xtest-error                    # Comando não encontrado
xtest-error syntax            # Erro de sintaxe  
xtest-error access            # Problema de permissão
xtest-error file              # Arquivo não existe

# Ver como o sistema responde
xerr                          # Analisar erro
xfix                          # Tentar correção automática
```

## 💡 Dicas e Truques

### Performance
- Sistema usa **lazy loading** - Python só carrega quando necessário
- **Cache inteligente** - Detecta mudanças e recarrega contexto
- **UTF-8 nativo** - Emojis funcionam perfeitamente no Windows

### Debugging
- Use `xtest-error` para testar diferentes cenários
- `xerr` mostra detalhes completos com stack trace
- Sistema cria logs detalhados para troubleshooting

### Customização
- Edite `xkit-minimal.ps1` para configurações básicas
- Modifique módulos Python em `Scripts/xkit/` para funcionalidades avançadas
- Sistema segue Clean Architecture - fácil de estender

## 🆘 Resolução de Problemas

### Comando não funciona
```powershell
# Verificar se perfil carregou
$global:XKitLoaded  # Deve retornar $true

# Recarregar perfil manualmente
. $PROFILE
```

### Erros de encoding
```powershell
# Sistema configura UTF-8 automaticamente
# Se ainda houver problemas, execute:
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"
```

### Python não encontrado
```powershell
# Verificar Python disponível
python --version

# Sistema usa 'python' por padrão
# Editar xkit-minimal.ps1 se necessário
```

---

**XKit v2.1** - PowerShell minimal, Python maximal! 🚀

### Utilitários

```powershell
# Recarregar perfil do PowerShell
xkit-reload

# Testar funcionalidade
python Scripts\test-prompt.py
```

## 🎨 Interface Compacta

### Elementos da Interface

A interface compacta mostra informações essenciais:

```
🪟 📁projeto 🌿branch ✓ 🐳container 🐍💙
```

**Significado dos símbolos:**

- `🪟` - Sistema Windows
- `📁` - Nome do projeto/pasta
- `🌿` - Branch do Git atual
- `✓` - Status (limpo/modificado)
- `🐳` - Engine de container (podman/docker)
- `🐍💙` - Python ativo

### Status Indicators

```
⚠️  1 anomalia(s) detectada(s)    # Problemas encontrados
🤖✓ 📱✓                          # AI e Telegram funcionando
💡 xkit-help para comandos        # Dica de uso
```

## 🤖 Usando a IA

### Comandos de AI

A integração com Gemini AI oferece:

```powershell
# Análise do contexto atual
xkit-ai

# Resolver problema específico  
xkit-solve "containers não iniciam"

# Sugestões para otimização
xkit-ai "como melhorar performance"

# Ajuda com comandos
xkit-ai "como usar podman-compose"
```

### Exemplos Práticos

```powershell
# Analisar erro no projeto
xkit-solve "ModuleNotFoundError: No module named requests"

# Otimizar configuração
xkit-ai "como configurar ambiente Python"

# Resolver problemas de container
xkit-solve "podman machine não inicia"
```

## 🐳 Gerenciamento de Containers

### Detecção Automática

O XKit detecta automaticamente:

- Podman e Docker instalados
- podman-compose disponível
- Arquivos compose no projeto
- Containers em execução

### Comandos de Container

```powershell
# Ver status completo
container-status

# Gerenciar com compose
compose-up          # docker-compose up -d
compose-down        # docker-compose down
compose-build       # docker-compose build

# Comandos diretos
podman ps           # listar containers
podman images       # listar imagens
podman logs <nome>  # ver logs
```

### Trabalhar com Projetos

Para projetos com `docker-compose.yml`:

```powershell
# Subir o ambiente
compose-up

# Ver status
container-status

# Logs dos serviços  
podman-compose logs

# Parar tudo
compose-down
```

## ⚡ Prompt Personalizado

### Formato do Prompt

```
Usuario@COMPUTADOR [branch] ~/caminho
$ 
```

### Informações Exibidas

- **Usuario@COMPUTADOR** - Identidade do sistema
- **[branch]** - Branch Git atual (se aplicável)
- **~/caminho** - Localização atual (~ = home)
- **$** - Indicador de comando

### Cores

- **Verde** - Usuario@Computador
- **Amarelo** - Branch Git  
- **Azul** - Caminho atual
- **Branco** - Símbolo $

## 🔍 Monitoramento e Diagnóstico

### Verificar Status

```powershell
# Status geral
xkit-status

# Verificar serviços
xkit-info

# Testar conectividade
python Scripts\xkit-final-validator.py
```

### Logs e Debugging

```powershell
# Ver erros Python
python Scripts\xkit_compact.py

# Testar componentes
python Scripts\test-prompt.py

# Verificar variáveis de ambiente
$env:GEMINI_API_KEY
$env:TELEGRAM_TOKEN
```

### Resolver Problemas Comuns

```powershell
# Python não encontrado
python --version

# Perfil não carrega
. $PROFILE

# Comandos não funcionam
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 🎛️ Personalização

### Adicionar Comandos Personalizados

Edite `Microsoft.PowerShell_profile.ps1`:

```powershell
function meu-comando {
    python "$PSScriptRoot\Scripts\xkit_compact.py" custom $args
}
```

### Modificar Interface

Edite `Scripts\xkit\infrastructure\compact_display.py`:

```python
def _get_status_emoji(self, info):
    # Customize aqui os emojis
    return "🎯"  # Seu emoji personalizado
```

### Configurar AI

```powershell
# Personalizar prompts de AI
$env:CUSTOM_AI_PROMPT = "Responda como especialista Python"
```

## 📊 Métricas e Performance

### Informações de Performance

O XKit monitora:

- Tempo de carregamento
- Status dos serviços
- Saúde dos containers  
- Conectividade de APIs

### Otimização

```powershell
# Ver status detalhado
xkit-status

# Limpar cache (se necessário)
Remove-Item $env:TEMP\xkit-* -Force
```

## 🚀 Workflows Comuns

### Desenvolvimento Python

```powershell
# 1. Verificar ambiente
xkit-status

# 2. Subir containers se houver
compose-up

# 3. Usar AI para sugestões
xkit-ai "configurar ambiente Python"

# 4. Monitorar
container-status
```

### Trabalho com Git

```powershell
# O prompt mostra automaticamente
# Usuario@PC [main] ~/projeto
# $

# Usar AI para resolver conflitos
xkit-solve "merge conflict no arquivo X"
```

### Debug de Problemas

```powershell
# 1. Identificar problema
xkit-status

# 2. Usar AI para análise
xkit-solve "descreva o problema aqui"

# 3. Aplicar solução sugerida
# Seguir instruções da AI
```

---

**Próximo**: [ARCHITECTURE.md](ARCHITECTURE.md) - Arquitetura técnica detalhada