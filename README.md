# 🚀 XKit v3.0 - Hybrid MCP Architecture

> **Sistema inteligente de desenvolvimento Windows com arquitetura MCP híbrida, plugins hot-reload e IA integrada**

[![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)](https://github.com/rootkit-original/WindowsPowerShell)
[![PowerShell](https://img.shields.io/badge/PowerShell-5.1%2B-blue.svg)](https://github.com/PowerShell/PowerShell)
[![Python](https://img.shields.io/badge/Python-3.11+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Visão Geral

O XKit v3.0 é um framework de desenvolvimento com arquitetura híbrida MCP (Model Context Protocol):

- **🔌 MCP Integration** - Extensibilidade através de servidores MCP
- **🧩 Plugin System** - Sistema de plugins com hot-reload
- **📡 Event-Driven** - Arquitetura orientada a eventos
- **🏗️ Hexagonal Architecture** - Ports and Adapters pattern
- **🤖 AI-Powered** - Gemini 2.0 Flash integrado para análises
- **⚡ Python-First** - Toda lógica em Python, PowerShell minimal

## ✨ Recursos Principais

- 🔌 **MCP Servers** - Extensibilidade via Model Context Protocol
- 🧩 **Hot-Reload Plugins** - Sistema de plugins dinâmicos
- 📡 **Event Bus** - Comunicação assíncrona entre componentes
- 🤖 **AI Integration** - Gemini AI para análise e sugestões
- 🏗️ **Clean Architecture** - Hexagonal com ports/adapters
- 🔧 **Git Workflow** - Automação inteligente de Git
- 📱 **Telegram Bot** - Notificações e assistente remoto

## 🚀 Instalação Rápida

```powershell
# Clone o repositório
git clone https://github.com/rootkit-original/WindowsPowerShell.git "$env:USERPROFILE\Documents\WindowsPowerShell"

# Execute o XKit (auto-instala dependências)
python Scripts\xkit_main.py

# Recarregue o PowerShell
powershell
```

## 🎯 Comandos Principais

### 🔌 MCP Commands

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `xkit mcp-status` | Status dos servidores MCP | `xkit mcp-status` |
| `xkit mcp-servers` | Lista servidores conectados | `xkit mcp-servers` |
| `xkit mcp-tools` | Lista ferramentas disponíveis | `xkit mcp-tools` |

### 🧩 Plugin Commands

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `xkit plugin-list` | Lista plugins carregados | `xkit plugin-list` |
| `xkit plugin-load` | Carrega um plugin | `xkit plugin-load git` |
| `xkit plugin-reload` | Recarrega plugin | `xkit plugin-reload git` |

### 🤖 AI Commands

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `xkit ai analyze` | Análise IA completa | `xkit ai analyze "Como otimizar Python?"` |
| `xkit ai explain` | Explica código | `xkit ai explain "def fibonacci(n):"` |
| `xkit ai suggest` | Sugestões de melhoria | `xkit ai suggest "projeto Flask"` |

### 🔧 Git Commands

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `xkit git-status` | Git status melhorado | `xkit git-status` |
| `xkit git-branch` | Operações de branch | `xkit git-branch` |
| `xkit git-create-branch` | Criar nova branch | `xkit git-create-branch feature/nova` |

## 🏗️ Arquitetura

```text
XKit v3.0 Hybrid MCP Architecture
├── PowerShell Layer (Minimal)
│   ├── Microsoft.PowerShell_profile.ps1  # Profile básico
│   ├── xkit-v3.ps1                       # Wrapper principal
│   └── oh-my-xkit/                       # Legacy plugins
├── Python Core (Hexagonal)
│   ├── xkit_main.py                      # Application entry point
│   └── xkit/                             # Hexagonal Architecture
│       ├── core/                         # 💎 Core Domain
│       │   ├── application.py           # Application service
│       │   ├── container.py             # DI container
│       │   └── ports/                   # Interface contracts
│       ├── adapters/                    # 🔌 External Adapters
│       │   ├── cli/                     # Command line interface
│       │   └── external/                # External services
│       ├── plugins/                     # 🧩 Plugin System
│       │   ├── manager.py               # Plugin manager
│       │   ├── loader.py                # Dynamic loading
│       │   └── base.py                  # Plugin interface
│       ├── events/                      # 📡 Event System
│       │   ├── bus.py                   # Central event bus
│       │   ├── events.py                # Event definitions
│       │   └── handlers/                # Event handlers
│       ├── mcp/                         # 🔌 MCP Integration
│       │   ├── client.py                # MCP client
│       │   ├── protocol.py              # MCP protocol
│       │   └── servers/                 # Internal MCP servers
│       └── infrastructure/              # 🛠️ Infrastructure
│           ├── ai_service.py            # Gemini AI service
│           ├── git.py                   # Git operations
│           └── display.py               # Rich console output
└── Configuration
    ├── MCP Servers                      # External MCP servers
    └── Plugin Discovery                 # Auto-discovery system
```

## 🤖 Sistema AI Integrado

O XKit v3.0 inclui integração completa com Gemini AI:

- **Análise Inteligente** - IA analisa código, erros e contexto
- **Sugestões Contextuais** - Recomendações baseadas no projeto
- **Explicação de Código** - Análise detalhada de funcionalidades
- **Error Handling** - Diagnóstico automático de problemas

```powershell
# Exemplos de uso da IA
xkit ai analyze "Como implementar cache em Redis?"
xkit ai explain "async def fetch_data():"
xkit ai suggest "otimização de performance"
```

## 📊 Performance

- ⚡ **Startup**: < 500ms para inicialização completa
- 🧠 **Memória**: ~25MB footprint com MCP ativo
- 🔄 **Hot Reload**: Plugins carregados dinamicamente
- 🔌 **MCP**: Servidores externos conectados sob demanda

## 🛠️ Desenvolvimento

### Plugin Development

```python
# Plugin Example (Python)
from xkit.plugins.base import XKitPlugin

class MyPlugin(XKitPlugin):
    def __init__(self):
        super().__init__("my-plugin", "1.0.0")
    
    def load(self):
        self.register_command("my-cmd", self.handle_command)
    
    def handle_command(self, args):
        return "✅ Command executed!"
```

### MCP Server Integration

```python
# MCP Server Example
class MyMCPServer:
    async def list_tools(self):
        return [Tool(name="analyze", description="Analyze data")]
    
    async def call_tool(self, name: str, arguments: dict):
        if name == "analyze":
            return await self.analyze_data(arguments)
```

## 📚 Documentação

- [📖 USAGE.md](USAGE.md) - Guia de uso completo
- [🔧 INSTALL.md](INSTALL.md) - Instalação detalhada
- [🏗️ ARCHITECTURE.md](ARCHITECTURE.md) - Arquitetura técnica
- [🐛 TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Solução de problemas
- [📝 API.md](API.md) - Referência da API Python
- [🔌 MCP.md](MCP.md) - Guia de integração MCP

## 🤝 Contribuindo

1. **Fork** o projeto
2. **Clone** localmente: `git clone https://github.com/your-user/WindowsPowerShell.git`
3. **Crie** branch: `git checkout -b feature/nova-funcionalidade`
4. **Teste** com MCP servers e plugins
5. **Submeta** PR com descrição clara

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes.

## 📜 Changelog

### v3.0.0 (2025-01-26)

- ✨ **Major**: Hybrid MCP Architecture implementada
- 🔌 **New**: Sistema MCP com servidores internos e externos
- 🧩 **New**: Plugin system com hot-reload dinâmico
- 📡 **New**: Event-driven architecture com bus central
- 🤖 **New**: Gemini AI 2.0 Flash integração completa
- 🏗️ **Breaking**: Migração para arquitetura hexagonal
- 🎯 **Breaking**: Comandos padronizados `xkit <command>`
- ⚡ **Performance**: Startup otimizado e cache inteligente

### v2.1.2 (2024-12-15)

- 🐛 **Fix**: README corrigido e documentação melhorada
- 📚 **Docs**: Estrutura de documentação reorganizada

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

## 🔗 Links Úteis

- [🐙 GitHub](https://github.com/rootkit-original/WindowsPowerShell)
- [📱 Telegram Bot](https://t.me/xkit_bot)
- [🤖 Gemini AI](https://ai.google.dev/)
- [🔌 MCP Protocol](https://modelcontextprotocol.io/)

---

**XKit v3.0** - *Framework híbrido MCP para desenvolvimento Windows* 🚀