# 🎯 Guia de Uso - XKit v3.0.0

Referência completa de todos os comandos e funcionalidades do XKit v3.0.0 com Hybrid MCP Architecture.

## 🆕 Nova Sintaxe v3.0.0

O XKit v3.0.0 introduz uma sintaxe consistente baseada em **actions**:

```powershell
# Sintaxe principal
xkit <action> <parameters>

# Exemplos
xkit git-status           # Git status aprimorado
xkit ai analyze "código"  # Análise IA
xkit mcp-list            # Listar MCP servers
```

**✅ Compatibilidade**: Comandos legacy (gs, ga, gc) continuam funcionando!

## 🚀 Comandos XKit v3.0.0

### 🤖 AI Commands (Novo!)

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `xkit ai analyze` | Análise IA completa | `xkit ai analyze "Como otimizar este código Python?"` |
| `xkit ai explain` | Explica código/conceito | `xkit ai explain "async def fetch():"` |
| `xkit ai suggest` | Sugestões de melhoria | `xkit ai suggest "projeto Flask"` |
| `xkit ai review` | Review de código | `xkit ai review arquivo.py` |

### 🔌 MCP Commands (Novo!)

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `xkit mcp-list` | Lista MCP servers ativos | `xkit mcp-list` |
| `xkit mcp-status` | Status dos servers | `xkit mcp-status` |
| `xkit mcp-test` | Testa conectividade MCP | `xkit mcp-test server-name` |
| `xkit mcp-tools` | Lista tools disponíveis | `xkit mcp-tools` |

### 🧩 Plugin Commands (Novo!)

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `xkit plugin-list` | Lista plugins carregados | `xkit plugin-list` |
| `xkit plugin-reload` | Recarrega plugin | `xkit plugin-reload git-plugin` |
| `xkit plugin-status` | Status dos plugins | `xkit plugin-status` |

### 📁 Git Commands

| Comando | Novo Formato v3.0 | Descrição | Exemplo |
|---------|-------------------|-----------|---------|
| `gs` / `xkit git-status` | ✅ Ambos funcionam | Status do repositório | `gs` ou `xkit git-status` |
| `ga` / `xkit git-add` | ✅ Ambos funcionam | Adiciona arquivos | `ga .` ou `xkit git-add .` |
| `gc` / `xkit git-commit` | ✅ Ambos funcionam | Commit com mensagem | `gc "fix: bug"` ou `xkit git-commit "fix: bug"` |
| `gp` / `xkit git-push` | ✅ Ambos funcionam | Push para remote | `gp` ou `xkit git-push` |
| `gl` / `xkit git-log` | ✅ Ambos funcionam | Histórico de commits | `gl --oneline` |
| `xkit git-create-branch` | 🆕 Novo | Criar branch inteligente | `xkit git-create-branch feature/nova` |

### 🐳 Container Commands  

| Comando | Novo Formato v3.0 | Descrição | Exemplo |
|---------|-------------------|-----------|---------|
| `d` / `xkit container-run` | ✅ Ambos funcionam | Executar container | `d run -it ubuntu` |
| `dc` / `xkit container-list` | ✅ Ambos funcionam | Listar containers | `dc` ou `xkit container-list` |
| `di` / `xkit container-images` | ✅ Ambos funcionam | Listar imagens | `di` |
| `xkit container-logs` | 🆕 Novo | Logs do container | `xkit container-logs nome-container` |

### 📱 Telegram & Notifications  

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `tg` / `xkit tg-send` | Envia mensagem Telegram | `tg "Deploy concluído!"` |
| `xkit tg-status` | 🆕 Status bot Telegram | `xkit tg-status` |
| `question` | Pergunta ao assistente AI | `question "Como otimizar Python?"` |

### 🛡️ Error Handling & System

| Comando | Novo Formato v3.0 | Descrição | Exemplo |
|---------|-------------------|-----------|---------|
| `xkit --version` | 🆕 Novo padrão | Versão e info do sistema | `xkit --version` |
| `xkit --help` | 🆕 Novo padrão | Ajuda completa | `xkit --help` |
| `xkit system-status` | 🆕 Melhorado | Status detalhado do sistema | `xkit system-status` |
| `xkit error-last` | 🆕 Novo | Último erro ocorrido | `xkit error-last` |
| `xkit error-fix` | 🆕 Novo | Tentar correção automática | `xkit error-fix` |

## 🎯 Exemplos Práticos v3.0.0

### 🚀 Workflow de Desenvolvimento Moderno

```powershell
# 1. Verificar estado do projeto com IA
xkit ai analyze "Analyze current project structure"
xkit git-status

# 2. Criar nova feature branch
xkit git-create-branch feature/user-authentication

# 3. Desenvolver com assistência IA
xkit ai suggest "JWT authentication in Python"

# 4. Commit inteligente
ga .  # Ou: xkit git-add .
gc "feat: implement JWT authentication"  # Ou: xkit git-commit

# 5. Push com notificação
gp  # Ou: xkit git-push
tg "🚀 Feature branch pushed: JWT authentication"
```

### 🔌 Usando MCP Servers

```powershell
# Verificar servers disponíveis
xkit mcp-list

# Usar server para análise de código
xkit mcp-tools code-analysis
xkit ai analyze --server code-analysis "otimize this function"

# Integrar com ferramentas externas
xkit mcp-test github-integration
```

### 🧩 Gerenciamento de Plugins

```powershell
# Ver plugins carregados
xkit plugin-list

# Recarregar plugin após mudanças
xkit plugin-reload git-plugin

# Status de todos os plugins
xkit plugin-status
```

### 🤖 Inteligência Artificial Avançada

```powershell
# Análise de código com contexto
xkit ai explain "def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)"

# Review completo de arquivo
xkit ai review src/main.py

# Sugestões de arquitetura
xkit ai analyze "How to implement microservices in Python?"

# Perguntas contextuais (com IA sabendo do projeto)
question "Como implementar cache Redis neste projeto?"
```

### 🚀 Sistema AutoStart

```powershell
# Verificar status do AutoStart
.\manage-autostart.ps1 status

# Logs de inicialização  
Get-Content startup.log -Tail 10

# Testar notificação de startup
tg "🌅 Sistema iniciado com XKit v3.0.0"
```

### 📊 Monitoramento e Logs

```powershell
# Status completo do sistema
xkit system-status

# Verificar performance
xkit --version  # Mostra métricas de startup

# Logs de erro
xkit error-last

# Análise de problemas com IA
xkit ai analyze "System showing slow performance"
```

---

## 🔗 Links Relacionados

- **[README.md](README.md)** - Visão geral do projeto
- **[INSTALL.md](INSTALL.md)** - Instalação detalhada  
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Arquitetura técnica
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Solução de problemas
- **[API.md](API.md)** - Referência da API Python
- **[RELEASE_NOTES_v3.0.0.md](RELEASE_NOTES_v3.0.0.md)** - Novidades da versão

*Para ajuda contextual, use `xkit --help` ou `question "Como usar XKit?"` no terminal.*