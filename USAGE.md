# XKit v2.1 - Guia de Uso

## 🎯 Visão Geral dos Comandos

O XKit oferece uma interface intuitiva com comandos organizados por categoria.

## 📋 Comandos Principais

### Informações e Ajuda

```powershell
# Mostra todos os comandos disponíveis
xkit-help

# Status detalhado do ambiente
xkit-status

# Informações sobre o projeto atual
xkit-info
```

### Inteligência Artificial

```powershell
# Sugestões inteligentes baseadas no contexto
xkit-ai

# Resolver problema específico
xkit-solve "erro ao executar comando"

# Análise de contexto avançada
xkit-ai "como otimizar este projeto?"
```

### Gerenciamento de Containers

```powershell
# Status dos containers
container-status

# Subir serviços com compose
compose-up

# Parar serviços
compose-down

# Comandos diretos do Podman/Docker
podman ps
docker images
```

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