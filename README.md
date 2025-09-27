# 🚀 XKit v3.0 - Hybrid MCP Architecture

> **Sistema inteligente de desenvolvimento Windows com arquitetura MCP híbrida, plugins hot-reload e IA integrada**

[![Version](https://img.shields.io/badge/version-3.0.0--dev-blue.svg)](https://github.com/rootkit-original/WindowsPowerShell)
[![PowerShell](https://img.shields.io/badge/PowerShell-5.1%2B-blue.svg)](https://github.com/PowerShell/PowerShell)
[![Python](https://img.shields.io/badge/Python-3.11+-green.svg)](https://www.python.org/)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

<div align="center">

### 🎯 **Oh-my-zsh Experience for Windows PowerShell + AI Power**

**XKit v3.0** é um framework avançado de desenvolvimento que combina a elegância do oh-my-zsh com a potência de IA e arquitetura moderna MCP para Windows PowerShell.

[🚀 Quick Start](#-instalação-rápida) • 
[📖 Documentation](#-documentação) • 
[🧩 Plugins](#-plugin-system) • 
[🤖 AI Integration](#-sistema-ai-integrado) • 
[🏗️ Architecture](#-arquitetura-híbrida-mcp)

</div>

---

## ✨ **O que torna o XKit especial?**

### 🔌 **MCP Integration First**
- Extensibilidade através do **Model Context Protocol**
- Servidores MCP internos e externos
- Interoperabilidade com ecossistema MCP global

### 🧩 **Plugin System Avançado**
- Hot-reload de plugins sem reinicialização
- Auto-discovery de plugins
- API simples para desenvolvimento

### 📡 **Event-Driven Architecture**
- Event bus central para comunicação assíncrona
- Handlers especializados com retry logic
- Event sourcing para auditoria

### 🏗️ **Hexagonal Architecture**
- Clean separation com ports e adapters
- Testabilidade e manutenibilidade
- Dependency injection container

### 🤖 **AI-Powered**
- **Gemini 2.0 Flash** integrado para análises
- Error handling inteligente com @xpilot
- Sugestões contextuais e análise de código

### ⚡ **Python-First Design**
- PowerShell apenas como wrapper mínimo
- Toda lógica em Python para performance
- Rico suporte a Unicode e emojis

---

## 🚀 **Instalação Rápida**

### **Método 1: Auto-Install (Recomendado)**

```powershell
# Execute o installer automático
irm https://raw.githubusercontent.com/rootkit-original/WindowsPowerShell/develop/install-xkit-v3.ps1 | iex
```

### **Método 2: Clone Manual**

```powershell
# Clone o repositório
git clone https://github.com/rootkit-original/WindowsPowerShell.git "$env:USERPROFILE\Documents\WindowsPowerShell"

# Navegue para o diretório
cd "$env:USERPROFILE\Documents\WindowsPowerShell"

# Execute o setup
python Scripts\xkit_main.py --setup

# Recarregue o PowerShell
powershell
```

### **Pré-requisitos**

| Requisito | Versão Mínima | Comando de Verificação |
|-----------|---------------|------------------------|
| PowerShell | 5.1+ | `$PSVersionTable.PSVersion` |
| Python | 3.11+ | `python --version` |
| Git | 2.30+ | `git --version` |

---

## 🎯 **Comandos Principais**

### 🔌 **MCP Commands**

```powershell
# Status completo do sistema MCP
xkit mcp-status

# Lista servidores MCP conectados
xkit mcp-servers

# Lista todas as ferramentas disponíveis
xkit mcp-tools

# Conectar a servidor MCP externo  
xkit mcp-connect --server "git://localhost:8000"

# Executar ferramenta MCP específica
xkit mcp-call --tool "analyze_code" --args "{'file': 'main.py'}"
```

### 🧩 **Plugin System**

```powershell
# Lista plugins instalados e status
xkit plugin-list

# Carrega plugin específico
xkit plugin-load git-enhanced

# Hot-reload de plugin
xkit plugin-reload ai-assistant

# Descobre novos plugins
xkit plugin-discover

# Informações detalhadas do plugin
xkit plugin-info docker-manager
```

### 🤖 **AI Assistant**

```powershell
# Análise completa com Gemini AI
xkit ai analyze "Como implementar cache Redis?"

# Explica código Python/PowerShell
xkit ai explain "async def process_data():"

# Sugestões de melhoria contextuais
xkit ai suggest "performance optimization Flask app"

# Correção automática de erros
xkit ai fix --error "ModuleNotFoundError: requests"

# Geração de código
xkit ai generate --type "REST API" --spec "FastAPI with PostgreSQL"
```

### 🔧 **Enhanced Git Workflow**

```powershell
# Git status com análise IA
xkit git-status

# Smart branch creation com naming convention
xkit git-create-branch --type feature --description "MCP integration"

# Auto-commit com mensagens inteligentes
xkit git-smart-commit

# Branch cleanup com safety checks
xkit git-cleanup-branches

# Interactive rebase helper
xkit git-interactive-rebase
```

### 📊 **System Management**

```powershell
# Status geral do sistema XKit
xkit status

# Performance metrics
xkit metrics

# Health check completo
xkit health-check

# Update all components
xkit update

# Backup configuration
xkit backup --type config
```

---

## 🏗️ **Arquitetura Híbrida MCP**

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                           XKit v3.0 Hybrid MCP Architecture                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  PowerShell Layer (Minimal Wrapper)                                        │
│  ├── Microsoft.PowerShell_profile.ps1     # Profile básico                  │
│  ├── xkit-v3.ps1                          # Entry point                     │
│  └── oh-my-xkit/                          # Legacy compatibility            │
├─────────────────────────────────────────────────────────────────────────────┤
│  Python Core (Hexagonal Architecture)                                      │
│  ├── xkit_main.py                         # Application entry point         │
│  └── xkit/                                                                  │
│      ├── 💎 core/                         # Core Domain                     │
│      │   ├── application.py              # Application services             │
│      │   ├── container.py                # DI container                     │
│      │   ├── domain/                     # Business entities               │
│      │   └── ports/                      # Interface contracts             │
│      ├── 🔌 adapters/                    # External Integration             │
│      │   ├── cli/                        # Command line interface           │
│      │   ├── external/                   # External APIs                   │
│      │   └── web/                        # Web interface (future)          │
│      ├── 🔌 mcp/                         # MCP Integration Layer           │
│      │   ├── client.py                   # MCP client protocol             │
│      │   ├── protocol.py                 # MCP protocol implementation     │
│      │   ├── config.json                 # Server configurations          │
│      │   └── servers/                    # Internal MCP servers           │
│      │       ├── core_server.py          # Core commands                  │
│      │       ├── ai_server.py            # AI analysis server            │
│      │       ├── git_server.py           # Git operations server          │
│      │       └── project_server.py       # Project analysis server       │
│      ├── 🧩 plugins/                     # Plugin System                   │
│      │   ├── manager.py                  # Plugin manager                  │
│      │   ├── loader.py                   # Dynamic loading                 │
│      │   ├── registry.py                 # Plugin registry                 │
│      │   ├── base.py                     # Plugin interface               │
│      │   └── core/                       # Essential plugins              │
│      │       ├── git_plugin.py           # Git operations                 │
│      │       ├── ai_plugin.py            # AI assistance                  │
│      │       ├── docker_plugin.py        # Container management           │
│      │       └── telegram_plugin.py      # Notifications                  │
│      ├── 📡 events/                      # Event-Driven System            │
│      │   ├── bus.py                      # Central event bus              │
│      │   ├── events.py                   # Event definitions              │
│      │   ├── middleware.py               # Event processing               │
│      │   └── handlers/                   # Specialized handlers           │
│      │       ├── command_handler.py      # Command events                 │
│      │       ├── error_handler.py        # Error processing               │
│      │       └── plugin_handler.py       # Plugin lifecycle               │
│      └── 🛠️ infrastructure/              # Infrastructure Layer           │
│          ├── ai_service.py               # Gemini AI integration          │
│          ├── git.py                      # Git operations                 │
│          ├── display.py                  # Rich console output            │
│          └── config.py                   # Configuration management       │
└─────────────────────────────────────────────────────────────────────────────┘
```

### **Core Principles**

- **🔌 MCP-First**: Extensibilidade via Model Context Protocol
- **🧩 Plugin-Based**: Modularidade com hot-reload capabilities
- **📡 Event-Driven**: Comunicação assíncrona loose-coupled
- **🏗️ Hexagonal**: Clean architecture com ports/adapters
- **🤖 AI-Powered**: Inteligência artificial em cada camada
- **⚡ Python-Centric**: Performance e expressividade

---

## 🤖 **Sistema AI Integrado**

### **Gemini 2.0 Flash Integration**

```python
# Exemplo: Análise inteligente de código
from xkit.adapters.external.gemini_adapter import GeminiAnalyzer

analyzer = GeminiAnalyzer()
result = await analyzer.analyze_code(
    code="def fibonacci(n): return n if n <= 1 else fib(n-1) + fib(n-2)",
    context="performance optimization"
)

# Output: Análise detalhada com sugestões de memoização
```

### **@xpilot Error Handler**

```powershell
# Quando erro ocorre, IA analisa e sugere soluções
PS> import-module NonExistentModule

🤖 @xpilot: Analisando erro...
   • Módulo 'NonExistentModule' não encontrado
   • Sugestão 1: Install-Module NonExistentModule
   • Sugestão 2: Verificar PowerShell Gallery
   • Criar branch fix/module-missing? [Y/n]
```

### **AI Command Examples**

| Comando | Exemplo | Resultado |
|---------|---------|-----------|
| `xkit ai analyze` | `"docker performance"` | Análise completa Docker + sugestões |
| `xkit ai explain` | `"async def main():"` | Explicação detalhada async/await |
| `xkit ai generate` | `"FastAPI CRUD"` | Código completo REST API |
| `xkit ai refactor` | `"optimize_function.py"` | Refatoração com melhores práticas |

---

## 📊 **Performance & Metrics**

| Métrica | Target | Atual | Status |
|---------|--------|-------|--------|
| ⚡ **Startup Time** | < 500ms | ~350ms | ✅ |
| 🧠 **Memory Usage** | < 50MB | ~35MB | ✅ |
| 🔄 **Plugin Hot-reload** | < 50ms | ~25ms | ✅ |
| 🔌 **MCP Connection** | < 100ms | ~75ms | ✅ |
| 🤖 **AI Response** | < 2s | ~1.2s | ✅ |

### **Benchmarks**

```powershell
# Execute benchmark completo
xkit benchmark --full

# Compare com versão anterior  
xkit benchmark --compare v2.1.2

# Profile performance específico
xkit profile --command "git-status"
```

---

## 🧩 **Plugin System**

### **Plugin Development**

```python
# my_plugin.py
from xkit.plugins.base import XKitPlugin
from xkit.events import EventBus

class MyAwesomePlugin(XKitPlugin):
    def __init__(self):
        super().__init__(
            name="my-awesome-plugin",
            version="1.0.0",
            description="Plugin incrível para XKit"
        )
    
    async def load(self) -> None:
        """Carregamento do plugin"""
        self.register_commands({
            "awesome-command": self.awesome_command,
            "another-cmd": self.another_command
        })
        
        # Subscribe to events
        await EventBus.subscribe(
            "command_executed",
            self.on_command_executed
        )
    
    async def awesome_command(self, args: list) -> str:
        """Comando incrível"""
        return f"🎉 Awesome plugin executed with: {' '.join(args)}"
    
    async def on_command_executed(self, event):
        """Handler de eventos"""
        if event.command.startswith("git"):
            await self.log(f"Git command detected: {event.command}")
```

### **Plugin Hot-Reload**

```powershell
# Modifique seu plugin e execute:
xkit plugin-reload my-awesome-plugin

# Plugin recarregado automaticamente sem reiniciar XKit! 🔥
```

### **Available Plugins**

| Plugin | Descrição | Status | Commands |
|--------|-----------|--------|----------|
| **git-enhanced** | Git operations avançadas | ✅ Active | `git-status`, `git-branch`, `git-create-branch` |
| **ai-assistant** | Integração Gemini AI | ✅ Active | `ai analyze`, `ai explain`, `ai generate` |
| **docker-manager** | Container management | ✅ Active | `docker-status`, `docker-compose` |
| **telegram-notifier** | Notificações Telegram | 🔧 Dev | `telegram-setup`, `telegram-notify` |
| **project-analyzer** | Análise de projetos | 🚀 Soon | `project-analyze`, `project-health` |

---

## 🔌 **MCP Integration**

### **Internal MCP Servers**

```json
// xkit/mcp/config.json
{
  "servers": {
    "xkit-core": {
      "command": "python",
      "args": ["-m", "xkit.mcp.servers.core_server"],
      "description": "Core XKit commands via MCP"
    },
    "xkit-ai": {
      "command": "python", 
      "args": ["-m", "xkit.mcp.servers.ai_server"],
      "description": "AI analysis and generation"
    },
    "xkit-git": {
      "command": "python",
      "args": ["-m", "xkit.mcp.servers.git_server"], 
      "description": "Advanced Git operations"
    }
  }
}
```

### **External MCP Servers**

```powershell
# Conectar com servidor MCP externo
xkit mcp-connect --server "filesystem://localhost:9000" --name "filesystem"

# Lista ferramentas disponíveis  
xkit mcp-tools --server filesystem

# Executar ferramenta MCP
xkit mcp-call --server filesystem --tool read_file --args "{'path': 'README.md'}"
```

### **MCP Server Development**

```python
# custom_mcp_server.py
from xkit.mcp.protocol import MCPServer, Tool

class CustomMCPServer(MCPServer):
    def __init__(self):
        super().__init__(name="custom-server", version="1.0.0")
    
    async def list_tools(self) -> list[Tool]:
        return [
            Tool(
                name="custom_analysis",
                description="Análise customizada",
                parameters={
                    "type": "object",
                    "properties": {
                        "target": {"type": "string"}
                    }
                }
            )
        ]
    
    async def call_tool(self, name: str, args: dict) -> str:
        if name == "custom_analysis":
            return f"Análise de: {args['target']}"
        
        raise ValueError(f"Tool {name} not found")
```

---

## 📡 **Event-Driven Architecture**

### **Event System**

```python
# Publisher
from xkit.events import EventBus, CommandExecutedEvent

await EventBus.publish(CommandExecutedEvent(
    command="git-status",
    result="success", 
    duration=0.25
))

# Subscriber  
@EventBus.subscribe(CommandExecutedEvent)
async def handle_git_commands(event: CommandExecutedEvent):
    if event.command.startswith("git"):
        print(f"🔧 Git operation: {event.command} ({event.duration}s)")
```

### **Available Events**

| Event | Trigger | Data | Use Cases |
|-------|---------|------|-----------|
| `CommandExecutedEvent` | Comando executado | command, result, duration | Logging, metrics, notifications |
| `ErrorOccurredEvent` | Erro detectado | error, context, stack_trace | Error handling, @xpilot analysis |
| `PluginLoadedEvent` | Plugin carregado | plugin_name, version | Plugin management, dependencies |
| `AIAnalysisEvent` | Análise IA completa | query, result, confidence | AI metrics, learning |
| `GitOperationEvent` | Operação Git | operation, branch, files | Git workflow automation |

---

## 🛠️ **Development**

### **Setup Development Environment**

```powershell
# Clone com todas as branches
git clone --recurse-submodules https://github.com/rootkit-original/WindowsPowerShell.git
cd WindowsPowerShell

# Create development environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt

# Setup pre-commit hooks
pre-commit install

# Run tests
pytest tests/
```

### **Testing**

```powershell
# Run all tests
xkit test

# Test specific component
xkit test --component mcp
xkit test --component plugins
xkit test --component events

# Integration tests
xkit test --integration

# Performance tests  
xkit test --performance
```

### **Contributing**

1. 🍴 **Fork** o repositório
2. 🌟 **Create** feature branch: `git checkout -b feature/amazing-feature`
3. ✅ **Commit** changes: `git commit -m 'feat: add amazing feature'`
4. 📤 **Push** branch: `git push origin feature/amazing-feature` 
5. 🔀 **Create** Pull Request

**Commit Convention**: Seguimos [Conventional Commits](https://www.conventionalcommits.org/)

---

## 📖 **Documentação**

### **Links Úteis**

| Documento | Descrição |
|-----------|-----------|
| [📋 API.md](API.md) | Documentação completa da API |
| [🏗️ ARCHITECTURE.md](ARCHITECTURE.md) | Arquitetura detalhada |
| [🚀 ROADMAP.md](ROADMAP.md) | Roadmap e milestones |
| [📝 CHANGELOG.md](CHANGELOG.md) | Histórico de mudanças |
| [🔧 CONTRIBUTING.md](CONTRIBUTING.md) | Guia para contribuições |
| [🛠️ TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Solução de problemas |

### **Tutorials**

- [🎯 Quick Start Guide](docs/quickstart.md)
- [🧩 Plugin Development](docs/plugin-development.md)
- [🔌 MCP Server Creation](docs/mcp-server.md)
- [🤖 AI Integration](docs/ai-integration.md)
- [📡 Event System](docs/event-system.md)

---

## 🤝 **Community & Support**

### **Getting Help**

- 📋 **Issues**: [GitHub Issues](https://github.com/rootkit-original/WindowsPowerShell/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/rootkit-original/WindowsPowerShell/discussions)
- 📧 **Email**: rootkit.original@gmail.com

### **Contributing**

- 🐛 **Bug Reports**: Use issue templates
- 💡 **Feature Requests**: Start with discussion
- 🔧 **Code Contributions**: Follow contribution guidelines
- 📖 **Documentation**: Always welcome!

### **Code of Conduct**

We follow the [Contributor Covenant](CODE_OF_CONDUCT.md). Be respectful and inclusive.

---

## 📄 **License**

Este projeto está licenciado sob a **MIT License** - veja [LICENSE](LICENSE) para detalhes.

---

## 🙏 **Acknowledgments**

- **[Model Context Protocol](https://modelcontextprotocol.io/)** - Por criar o padrão MCP
- **[Gemini AI](https://gemini.google.com/)** - Pela integração inteligente
- **[Oh My Zsh](https://ohmyz.sh/)** - Pela inspiração original
- **Comunidade PowerShell** - Pelo suporte contínuo

---

<div align="center">

### **🌟 Se o XKit foi útil, deixe uma estrela! ⭐**

**Made with 💙 by [rootkit-original](https://github.com/rootkit-original)**

[⬆ Back to Top](#-xkit-v30---hybrid-mcp-architecture)

</div>