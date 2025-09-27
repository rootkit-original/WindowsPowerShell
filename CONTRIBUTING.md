# 🤝 Como Contribuir - XKit v3.0.0

Obrigado pelo interesse em contribuir com o XKit v3.0.0! Este guia vai te orientar no desenvolvimento com a nova Hybrid MCP Architecture.

## 🎯 Visão Geral v3.0.0

O XKit v3.0.0 é uma plataforma de desenvolvimento moderna com:

- 🔌 **Hybrid MCP Architecture** - Extensibilidade via Model Context Protocol
- 🧩 **Plugin System** - Hot-reload e dependency injection
- 📡 **Event-Driven Design** - Comunicação assíncrona via event bus
- 🏗️ **Hexagonal Architecture** - Clean separation com ports/adapters
- 🤖 **AI-First** - Gemini 2.0 Flash integrado nativamente

## 🌿 Workflow de Contribuição v3.0.0

### 1. 🍴 Fork & Clone

```powershell
# Fork no GitHub, depois clone
git clone https://github.com/seu-usuario/WindowsPowerShell.git
cd WindowsPowerShell

# Adicione upstream
git remote add upstream https://github.com/rootkit-original/WindowsPowerShell.git
```

### 2. 🎯 Escolha o Tipo de Contribuição

| Tipo | Branch Base | Padrão de Nome | Exemplo |
|------|-------------|----------------|---------|
| **MCP Server** | `develop` | `feature/mcp-<server>` | `feature/mcp-github-server` |
| **Plugin** | `develop` | `feature/plugin-<name>` | `feature/plugin-docker-compose` |
| **AI Integration** | `develop` | `feature/ai-<feature>` | `feature/ai-code-review` |
| **Core Architecture** | `develop` | `feature/core-<area>` | `feature/core-event-bus` |
| **Bug Fix** | `develop` | `fix/descrição` | `fix/mcp-connection-timeout` |
| **Documentation** | `develop` | `docs/área` | `docs/mcp-server-guide` |
| **Hotfix** | `main` | `hotfix/v3.0.x-bug` | `hotfix/v3.0.1-startup-fail` |

### 3. 🚀 Criar Branch de Trabalho

```powershell
# Para features/fix/docs
git checkout develop
git pull upstream develop
git checkout -b feature/mcp-new-server

# Para hotfix
git checkout main  
git pull upstream main
git checkout -b hotfix/v3.0.1-fix-critico
```

### 4. 💻 Desenvolver com Hybrid MCP Architecture

#### 🏗️ **Estrutura do Código v3.0.0**
- **PowerShell**: Minimal wrapper em `Microsoft.PowerShell_profile.ps1`
- **Python Core**: Lógica em `Scripts/xkit/`
  - `core/` - Domain & Application layers
  - `adapters/` - External integrations  
  - `mcp/` - MCP servers and client
  - `plugins/` - Plugin system
  - `events/` - Event-driven architecture
- **Clean Architecture**: Domain/Application/Infrastructure

#### 📝 **Padrão de Commits v3.0.0**
Usamos **Conventional Commits** com escopos específicos:

```powershell
# MCP-related
git commit -m "feat(mcp): add GitHub integration MCP server"
git commit -m "fix(mcp): resolve connection timeout issues"

# Plugin system
git commit -m "feat(plugins): implement hot-reload mechanism"
git commit -m "fix(plugins): handle plugin loading errors"

# Event system
git commit -m "feat(events): add command execution events"
git commit -m "fix(events): prevent event loop blocking"

# AI integration
git commit -m "feat(ai): add code review capabilities"
git commit -m "fix(ai): handle Gemini API rate limits"

# Core architecture
git commit -m "feat(core): implement dependency injection container"
git commit -m "refactor(core): migrate to hexagonal architecture"
```

**Tipos e Escopos:**
- `feat(mcp|plugins|events|ai|core)` - Nova funcionalidade
- `fix(mcp|plugins|events|ai|core)` - Correção de bug
- `docs(api|mcp|plugins|usage)` - Documentação
- `refactor(core|adapters|infrastructure)` - Refatoração
- `test(unit|integration|e2e)` - Testes
- `chore(deps|config|build)` - Manutenção

### 5. 🧪 Testar

```powershell
# Teste manual básico v3.0.0
python Scripts\xkit_main.py --version
xkit --help
xkit system-status

# Testar funcionalidades específicas
xkit mcp-status
xkit plugin-status
xkit ai analyze "test"

# Se tiver testes automatizados
python -m pytest Scripts/tests/
```

### 6. 📤 Push & Pull Request

```powershell
# Push da branch
git push origin feature/mcp-new-server

# No GitHub:
# 1. Criar Pull Request
# 2. Base: develop (ou main para hotfix)  
# 3. Preencher template do PR
# 4. Solicitar review
```

---

## 🎯 Guias de Desenvolvimento Específicos

### 🔌 Desenvolvendo MCP Servers

```python
# Exemplo: Criar um MCP Server personalizado
from xkit.mcp.servers.base import XKitMCPServer
from xkit.mcp.protocol import Tool, ToolResult

class CustomMCPServer(XKitMCPServer):
    def __init__(self):
        super().__init__("custom-server", "1.0.0")
    
    async def list_tools(self) -> List[Tool]:
        return [
            Tool(
                name="my-command",
                description="Execute custom logic",
                inputSchema={"type": "object", "properties": {...}}
            )
        ]
    
    async def call_tool(self, name: str, arguments: dict) -> ToolResult:
        # Implement your logic here
        return ToolResult(content=[{"type": "text", "text": "Result"}])
```

### 🧩 Desenvolvendo Plugins

```python
# Exemplo: Plugin com hot-reload
from xkit.plugins.base import XKitPlugin

class MyPlugin(XKitPlugin):
    def __init__(self):
        super().__init__("my-plugin", "1.0.0")
    
    async def load(self) -> None:
        """Initialize plugin resources"""
        self.register_command("my-cmd", self.handle_command)
        
    async def unload(self) -> None:
        """Cleanup resources"""
        # Clean up any resources
        
    def handle_command(self, args: list) -> str:
        return "Plugin command executed!"
```

### 📡 Desenvolvendo Event Handlers

```python
# Exemplo: Custom event handler
from xkit.events import EventBus, XKitEvent

@event_bus.subscribe(CommandExecutedEvent)
async def my_event_handler(event: CommandExecutedEvent):
    """Handle command execution events"""
    if event.execution_time > 1000:  # Slow command
        # Log or notify about slow performance
        pass
```

## 📋 Template de Pull Request v3.0.0

```markdown
## 📝 Descrição
Breve descrição das mudanças implementadas.

## 🎯 Tipo de Mudança
- [ ] 🔌 MCP Server (novo servidor ou melhoria)
- [ ] 🧩 Plugin (novo plugin ou funcionalidade)
- [ ] 📡 Event System (novos eventos ou handlers)
- [ ] 🤖 AI Integration (melhorias na integração IA)
- [ ] 🏗️ Core Architecture (mudanças na arquitetura)
- [ ] 🐛 Bug Fix (correção de problema)
- [ ] 📚 Documentation (mudança apenas na documentação)

## 🧪 Como Testar
1. Checkout da branch: `git checkout feature/branch-name`
2. Execute: `python Scripts\xkit_main.py --version`
3. Teste específico: [descreva comandos específicos]
4. Resultado esperado: [descreva o comportamento esperado]

## 📊 Impacto na Performance
- [ ] ✅ Startup time não foi afetado (<500ms)
- [ ] ✅ Memory usage controlado (~25MB)
- [ ] ✅ Command response time OK (<100ms)

## 📸 Screenshots
Se aplicável, adicione screenshots das mudanças.

## ✅ Checklist v3.0.0
- [ ] 🔌 MCP servers testados (se aplicável)
- [ ] 🧩 Plugins carregam corretamente (se aplicável)
- [ ] 📡 Events funcionam sem bloquear (se aplicável)
- [ ] 🤖 AI features testadas (se aplicável)
- [ ] 📝 Código segue convenções do projeto
- [ ] 🧪 Testes passam localmente  
- [ ] 📚 Documentação atualizada (API.md, USAGE.md)
- [ ] 🌿 Branch está atualizada com develop
- [ ] 💬 Commits seguem padrão conventional
```

## 🏗️ Diretrizes de Arquitetura v3.0.0

### 🔌 **MCP Layer (Extensibilidade)**
```python
# Scripts/xkit/mcp/servers/ - MCP servers
class GitMCPServer(XKitMCPServer):
    async def call_tool(self, name: str, arguments: dict):
        # Server implementation
        pass

# Scripts/xkit/mcp/client.py - MCP client
class XKitMCPClient:
    async def connect_server(self, server_name: str):
        # Client connection logic
        pass
```

### 🧩 **Plugin Layer (Modularidade)**
```python
# Scripts/xkit/plugins/ - Plugin system
class GitPlugin(XKitPlugin):
    def load(self) -> None:
        # Plugin initialization
        pass
    
    def get_commands(self) -> dict:
        return {"git-enhanced": self.git_command}
```

### 📡 **Event Layer (Comunicação)**
```python
# Scripts/xkit/events/ - Event system
@event_bus.subscribe(CommandExecutedEvent)
async def handle_command(event: CommandExecutedEvent):
    # Event handling logic
    pass
```

### 🏗️ **Core Layer (Domínio)**
```python
# Scripts/xkit/core/ - Domain logic
class CommandService:
    async def execute_command(self, action: str, params: list):
        # Core business logic
        pass
```

### ⚡ **PowerShell Layer (Interface)**
```powershell
# Microsoft.PowerShell_profile.ps1 - Minimal interface
function global:xkit {
    param([Parameter(ValueFromRemainingArguments)]$args)
    python "$PSScriptRoot\Scripts\xkit_main.py" @args
}
```

### 📊 **Princípios de Design v3.0.0**
1. **MCP-First** - Extensibilidade via Model Context Protocol
2. **Plugin-Based** - Modularidade com hot-reload capability
3. **Event-Driven** - Comunicação assíncrona via event bus
4. **AI-Native** - IA integrada profundamente no core
5. **PowerShell Minimal** - Interface simples, Python faz o trabalho
6. **Performance-First** - Startup <500ms, operações otimizadas

## 🐛 Reportando Issues

### 🔍 **Antes de Reportar**
1. ✅ Procure por issues similares existentes
2. ✅ Teste na versão mais recente
3. ✅ Reproduza o problema consistentemente

### 📝 **Template de Issue v3.0.0**
```markdown
## 🐛 Descrição do Bug
Descrição clara e concisa do problema.

## 🏗️ Componente Afetado
- [ ] 🔌 MCP Server (qual server?)
- [ ] 🧩 Plugin System (qual plugin?)
- [ ] 📡 Event System (qual evento?)
- [ ] 🤖 AI Integration (Gemini API?)
- [ ] 🚀 AutoStart System
- [ ] 📱 Telegram Integration
- [ ] 🏗️ Core Architecture

## 🔄 Reproduzir
1. Execute comando '...'
2. Veja erro '...'
3. Resultado esperado era '...'

## 💻 Ambiente
- **XKit Version**: `xkit --version`
- **OS**: Windows 10/11 Build XXXXX
- **PowerShell**: `$PSVersionTable.PSVersion`
- **Python**: `python --version`
- **Terminal**: Windows Terminal / PowerShell ISE / Command Prompt

## 📊 Status do Sistema
```
xkit system-status
xkit mcp-status
xkit plugin-status
```

## 📋 Logs de Erro
```
xkit error-last
```

## 📸 Screenshots
Se aplicável, adicione screenshots do erro.
```

## 🎯 Áreas que Precisam de Contribuição v3.0.0

### 🔌 **MCP Servers (Alta Prioridade)**
- [ ] **GitHub MCP Server** - Complete GitHub API integration
- [ ] **Docker MCP Server** - Container management via MCP
- [ ] **Database MCP Server** - PostgreSQL, Redis, MongoDB support
- [ ] **API Testing MCP Server** - Postman-like functionality via MCP
- [ ] **Cloud MCP Server** - AWS, Azure, GCP integrations
- [ ] **Monitoring MCP Server** - System metrics and alerts

### 🧩 **Plugin Development**
- [ ] **IDE Integration Plugin** - VS Code, JetBrains support
- [ ] **Testing Plugin** - Advanced test automation
- [ ] **Documentation Plugin** - Auto-documentation generation
- [ ] **Performance Plugin** - System monitoring and optimization
- [ ] **Security Plugin** - Vulnerability scanning

### 📡 **Event System Enhancement**
- [ ] **Event Analytics** - Usage pattern analysis
- [ ] **Event Replay System** - Debug and testing capabilities
- [ ] **Custom Event Types** - User-defined event schemas
- [ ] **Event Persistence** - Long-term event storage

### 🤖 **AI Integration Enhancement**
- [ ] **Multi-Model Support** - GPT-4, Claude, local LLMs
- [ ] **Context Management** - Long-term conversation memory
- [ ] **Code Generation** - Advanced scaffolding capabilities
- [ ] **AI Agents** - Autonomous task execution

### 📚 **Documentação**
- [ ] **MCP Server Development Guide** - Como criar MCP servers
- [ ] **Plugin Development Guide** - Tutorial completo de plugins
- [ ] **Event System Guide** - Como usar o sistema de eventos
- [ ] **AI Integration Examples** - Casos de uso práticos com IA
- [ ] **Cross-Platform Guide** - Preparação para Linux/macOS
- [ ] **Performance Optimization Guide** - Best practices
- [ ] **Video Tutorials** - Screencasts das funcionalidades

### 🧪 **Testes & Qualidade**
- [ ] **MCP Integration Tests** - Testes de servers MCP
- [ ] **Plugin System Tests** - Hot-reload e dependency tests
- [ ] **Event System Tests** - Async event handling tests
- [ ] **Performance Benchmarks** - Automated performance tracking
- [ ] **Cross-Platform Tests** - WSL, containers testing
- [ ] **AI Integration Tests** - Gemini API integration tests
- [ ] **End-to-End Workflows** - Complete user journey tests

## 🏆 Reconhecimentos

Contribuidores são reconhecidos em:
- 📜 **CHANGELOG.md** - Créditos detalhados por versão
- 🎖️ **README.md** - Hall of Fame dos contribuidores
- 🌟 **GitHub Contributors** - Reconhecimento automático
- 🏅 **Plugin/MCP Server Credits** - Créditos nos componentes criados

## 📞 Suporte & Comunidade

### 💬 Canais de Comunicação
- **GitHub Discussions** - [Discussões gerais e ideias](https://github.com/rootkit-original/WindowsPowerShell/discussions)
- **GitHub Issues** - [Bug reports e feature requests](https://github.com/rootkit-original/WindowsPowerShell/issues)
- **Pull Requests** - [Code review e colaboração](https://github.com/rootkit-original/WindowsPowerShell/pulls)

### 🤖 Suporte Inteligente
- **AI Help**: `xkit ai analyze "como contribuir com feature X"`
- **Context-Aware Help**: `question "melhor forma de desenvolver plugin Y"`
- **Error Analysis**: Sistema AI analisa problemas automaticamente

### 📊 Community Stats & Metrics
- Track contributions and impact
- Performance improvements
- Feature adoption rates
- Community growth metrics

## 📄 Código de Conduta

Este projeto adere ao [Contributor Covenant](https://contributor-covenant.org/). 

**Diretrizes principais:**
- 🤝 **Respeito mútuo** - Trate todos com respeito e cortesia
- 🌍 **Inclusividade** - Bem-vindos desenvolvedores de todos os backgrounds
- 🎯 **Foco construtivo** - Feedback construtivo e colaborativo
- 📚 **Aprendizado conjunto** - Compartilhe conhecimento e aprenda

---

## 🚀 Começando a Contribuir Hoje

### 🎯 Para Iniciantes
1. **Fork o projeto** e clone localmente
2. **Leia a documentação** (README.md, ARCHITECTURE.md, API.md)
3. **Configure o ambiente** seguindo INSTALL.md
4. **Explore o código** em `Scripts/xkit/`
5. **Encontre uma issue** marcada com "good first issue"

### ⚡ Para Experientes
1. **Analise a arquitetura** MCP/Plugin/Event-driven
2. **Identifique áreas de melhoria** ou novas funcionalidades
3. **Proponha RFC** para mudanças significativas
4. **Implemente com testes** e documentação
5. **Contribua para o ecossistema** (MCP servers, plugins)

### 🔮 Visão de Longo Prazo
- Contribua para o **ecossistema MCP** mais amplo
- Desenvolva **plugins reutilizáveis** para a comunidade
- **Cross-platform expansion** (Linux, macOS)
- **Enterprise features** para organizações

---

**Obrigado por tornar o XKit v3.0.0 ainda melhor!** 🚀✨

*Join us in building the future of developer tooling!*