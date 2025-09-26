# GitHub Copilot Instructions for XKit Project

## Project Overview
XKit is an enhanced PowerShell framework with Hybrid MCP Architecture that provides:
- 🎨 Oh-my-zsh inspired experience for Windows PowerShell
- 🤖 AI-powered error handling with local @xpilot agent
- 🔌 **MCP (Model Context Protocol)** integration for extensibility
- 🧩 **Plugin System** with hot-reload capabilities
- 📡 **Event-Driven Architecture** for loose coupling
- 🏗️ **Hexagonal Architecture** with ports and adapters
- 🔧 Git workflow automation with intelligent branching
- 📱 Telegram notifications and AI assistant integration
- 🐳 Container management (Docker/Podman) support

## Architecture Philosophy
- **Python-First**: PowerShell is minimal wrapper, Python handles all logic
- **MCP Integration**: Extensible architecture through MCP servers
- **Plugin-Based**: Modular components with hot-reload support
- **Event-Driven**: Asynchronous communication via central event bus
- **Hexagonal Architecture**: Clean separation with ports and adapters
- **Error-Driven Development**: Sophisticated error handling with Git integration
- **Configuration-Based**: Absolute paths, robust configuration system
- **Emoji-Rich UX**: Python handles Unicode properly, PowerShell stays ASCII

## Key Components

### Core Structure
```
WindowsPowerShell/
├── .github/copilot-instructions.md     # This file
├── xkit-config.ps1                     # Minimal PS config with absolute paths
├── Microsoft.PowerShell_profile.ps1    # Ultra-minimal PS profile
├── Scripts/
│   ├── xkit_main.py                   # Python entry point
│   └── xkit/                          # Hybrid Architecture modules
│       ├── mcp/                       # 🔌 MCP Integration
│       │   ├── client.py             # Cliente MCP principal
│       │   ├── servers/              # Servers MCP internos
│       │   └── config.json           # Configuração de servers
│       ├── plugins/                  # 🧩 Plugin System
│       │   ├── base.py              # Interface base
│       │   ├── manager.py           # Gerenciador de plugins
│       │   └── core/                # Plugins essenciais
│       ├── events/                  # 📡 Event System
│       │   ├── bus.py              # Event bus central
│       │   ├── events.py           # Definições de eventos
│       │   └── handlers/           # Event handlers
│       ├── core/                   # 💎 Core Domain
│       │   ├── domain/             # Entidades e VOs
│       │   ├── application/        # Use cases
│       │   └── ports/              # Interfaces
│       └── adapters/               # 🔌 External Adapters
│           ├── cli/               # CLI adapter
│           └── external/          # APIs externas
└── oh-my-xkit/
    ├── oh-my-xkit.ps1                # Minimal PS framework loader
    └── plugins/                       # Thin PS wrappers calling Python
```

### Error Handling System (@xpilot)
When errors occur:
1. **Detection**: PowerShell wrappers catch errors and call Python
2. **Analysis**: Python AI agent analyzes error patterns
3. **Git Integration**: Creates error branch automatically
4. **Resolution**: Provides suggestions, auto-fixes when possible
5. **Workflow**: User can accept fixes, create tasks, or continue

## Development Guidelines

### When Working on XKit:
1. **Minimize PowerShell**: Only use PS for absolute necessities
2. **Python-Heavy**: All logic, UI, error handling in Python
3. **Hybrid Architecture**: Follow MCP/Plugin/Event-driven patterns
4. **MCP-First**: Extend via MCP servers when possible
5. **Plugin-Based**: Create modular, hot-reloadable components
6. **Event-Driven**: Use event bus for loose coupling
7. **Absolute Paths**: Always use configuration-based paths
8. **Error-First**: Every command should have error handling
9. **Rich UX**: Use emojis and colors in Python, plain text in PS

### Common Tasks:

#### Adding New Commands
- Create Python use case in `application/use_cases.py`
- Add minimal PS wrapper that calls `Invoke-XKitPython`
- Register in `xkit_main.py` action dispatcher

#### Extending Error Handling
- Add new error patterns in `infrastructure/error_handler.py`
- Extend XPilot analysis in `XPilotAgent` class
- Update display service for rich error presentation

#### MCP Server Development
- Create new server in `xkit/mcp/servers/`
- Implement MCP protocol methods (list_tools, call_tool)
- Register server in `xkit/mcp/config.json`
- Add integration tests for server functionality

#### Plugin Development
- Create plugin class extending `XKitPlugin` base
- Implement required methods (`load`, `unload`, `get_commands`)
- Add hot-reload support via `PluginManager`
- Register plugin for automatic discovery

#### Event-Driven Features
- Define new events in `xkit/events/events.py`
- Create event handlers in `xkit/events/handlers/`
- Publish events through central `EventBus`
- Subscribe to events for reactive behavior

#### Hexagonal Architecture Extensions
- Define ports in `xkit/core/ports/`
- Implement adapters in `xkit/adapters/`
- Use dependency injection for loose coupling
- Create tests using port interfaces

### Code Patterns

#### PowerShell Pattern (MINIMAL):
```powershell
function global:new-command {
    param([Parameter(ValueFromRemainingArguments)]$args)
    Invoke-XKitPython "action-name" @args
}
```

#### Python Pattern (RICH):
```python
class NewFeatureUseCase:
    def __init__(self, dependencies...):
        # Dependency injection
    
    def execute(self, params):
        # Business logic with error handling
        try:
            result = self._do_work(params)
            return result
        except Exception as e:
            self.error_handler.handle_error(str(e), "context")
```

#### MCP Server Pattern:
```python
class XKitMCPServer:
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
    
    async def list_tools(self) -> list[Tool]:
        return [Tool(name="command", description="Description")]
    
    async def call_tool(self, name: str, arguments: dict) -> str:
        # Implementation
        pass
```

#### Plugin Pattern:
```python
class CustomPlugin(XKitPlugin):
    def __init__(self):
        super().__init__("custom", "1.0.0")
    
    def load(self) -> None:
        # Initialize plugin
        pass
    
    def unload(self) -> None:
        # Cleanup plugin
        pass
    
    def get_commands(self) -> dict:
        return {"custom-cmd": self.handle_command}
```

#### Event Pattern:
```python
# Publish event
event_bus.publish(CommandExecutedEvent(
    command="git-status",
    result="success",
    timestamp=datetime.now()
))

# Subscribe to events
@event_bus.subscribe(CommandExecutedEvent)
async def handle_command_executed(event: CommandExecutedEvent):
    # Handle event
    pass
```

### Git Workflow & Commits

#### Branch Strategy:
```bash
# Feature development
git checkout -b feature/mcp-integration
git checkout -b feature/plugin-system
git checkout -b feature/event-driven

# Refactoring
git checkout -b refactor/hybrid-architecture
git checkout -b refactor/hexagonal-ports

# Bug fixes
git checkout -b fix/mcp-connection-error
git checkout -b fix/plugin-hot-reload
```

#### Semantic Commits:
```bash
# Features
git commit -m "feat(mcp): add core MCP client implementation"
git commit -m "feat(plugins): add hot-reload plugin manager"
git commit -m "feat(events): implement central event bus"

# Fixes
git commit -m "fix(mcp): resolve server connection timeout"
git commit -m "fix(plugins): handle plugin loading errors"

# Tests
git commit -m "test(mcp): add integration tests for MCP servers"
git commit -m "test(plugins): add unit tests for plugin manager"

# Documentation
git commit -m "docs(mcp): add MCP server development guide"
git commit -m "docs(migration): update migration plan with timeline"

# Refactoring
git commit -m "refactor(core): migrate to hexagonal architecture"
git commit -m "refactor(events): simplify event handler registration"
```

## Current Status
- ✅ Clean Architecture foundation implemented
- ✅ Error handling system with @xpilot agent
- ✅ Python-backed command system
- ✅ Configuration-based path management
- ✅ Rich emoji UX in Python
- 🔄 **Migrating to Hybrid MCP Architecture**
- 🚀 **MCP Integration**: Core client and servers in development
- 🧩 **Plugin System**: Hot-reload capabilities being implemented
- 📡 **Event System**: Central event bus architecture planned

## Priority Tasks (Migration to v3.0)
1. **MCP Core Implementation**: Complete MCP client and server framework
2. **Plugin System**: Convert existing modules to hot-reloadable plugins
3. **Event-Driven Architecture**: Implement central event bus for loose coupling
4. **Hexagonal Ports**: Define clean boundaries with adapters pattern
5. **Migration Testing**: Ensure backwards compatibility during transition

## Working Principles
- **Fail Fast**: Better to show clear errors than silent failures
- **User-Centric**: Rich feedback, helpful suggestions
- **Developer-Friendly**: Clean code, good separation of concerns
- **Maintainable**: Configuration-driven, testable architecture
- **Extensible**: Easy to add new features and integrations

## AI Assistant Integration
- **Gemini API**: For intelligent project analysis and suggestions  
- **Telegram Bot**: For notifications and remote interactions
- **Error Analysis**: Pattern matching and resolution suggestions
- **Context Awareness**: Understands Git, Docker, project structure

## When You Encounter Issues
1. Check `xkit-config.ps1` for path configuration
2. Verify Python dependencies and imports
3. Test Python components independently first
4. Use error handling system to debug PS integration
5. Prioritize moving logic from PS to Python

Remember: PowerShell is just the entry point. Python is the brain. 🧠