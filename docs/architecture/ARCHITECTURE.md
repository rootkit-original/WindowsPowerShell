# XKit v3.0 - Arquitetura Híbrida MCP

## 🏗️ Hybrid MCP Architecture Overview

O XKit v3.0 implementa uma arquitetura híbrida baseada no Model Context Protocol (MCP), combinando:

- **🔌 MCP Integration** - Servidores MCP internos e externos
- **🧩 Plugin System** - Sistema modular com hot-reload
- **📡 Event-Driven** - Bus de eventos para comunicação assíncrona
- **🏗️ Hexagonal Architecture** - Ports and Adapters pattern
- **🤖 AI-First** - Gemini 2.0 Flash como core inteligente
- **⚡ Python-Centric** - PowerShell como wrapper mínimo

## 📐 Estrutura Hexagonal

```text
Scripts/xkit/
├── core/                           # 💎 Core Domain
│   ├── application/               # Application Services
│   │   ├── __init__.py
│   │   ├── command_service.py     # Command orchestration
│   │   ├── ai_service.py          # AI analysis service
│   │   └── plugin_service.py      # Plugin management
│   ├── domain/                    # Business Logic
│   │   ├── __init__.py
│   │   ├── entities.py            # Domain entities
│   │   ├── interfaces.py          # Domain contracts
│   │   └── value_objects.py       # Value objects
│   └── ports/                     # Interface Contracts
│       ├── __init__.py
│       ├── ai_port.py             # AI service interface
│       ├── git_port.py            # Git operations interface
│       └── display_port.py        # Display interface
├── adapters/                       # 🔌 External Adapters
│   ├── cli/                       # CLI Adapter
│   │   ├── __init__.py
│   │   ├── command_parser.py      # Command parsing
│   │   └── output_formatter.py    # Output formatting
│   └── external/                  # External Services
│       ├── __init__.py
│       ├── gemini_adapter.py      # Gemini AI adapter
│       ├── git_adapter.py         # Git operations
│       └── telegram_adapter.py    # Telegram notifications
├── mcp/                           # 🔌 MCP Integration Layer
│   ├── __init__.py
│   ├── client.py                  # MCP client protocol
│   ├── protocol.py                # MCP protocol implementation
│   ├── config.json                # MCP servers configuration
│   └── servers/                   # Internal MCP Servers
│       ├── __init__.py
│       ├── git_server.py          # Git operations server
│       ├── ai_server.py           # AI analysis server
│       └── project_server.py      # Project analysis server
├── plugins/                       # 🧩 Plugin System
│   ├── __init__.py
│   ├── base.py                    # Plugin interface
│   ├── manager.py                 # Plugin manager
│   ├── loader.py                  # Dynamic loading
│   └── registry.py                # Plugin registry
├── events/                        # 📡 Event System
│   ├── __init__.py
│   ├── bus.py                     # Central event bus
│   ├── events.py                  # Event definitions
│   └── handlers/                  # Event handlers
│       ├── __init__.py
│       ├── command_handler.py     # Command events
│       ├── error_handler.py       # Error events
│       └── plugin_handler.py      # Plugin events
└── infrastructure/                # 🛠️ Legacy Infrastructure
    ├── __init__.py                # (Kept for compatibility)
    ├── ai_service.py              # → Moving to adapters/
    ├── git.py                     # → Moving to adapters/
    └── display.py                 # → Moving to adapters/
```

## 🎯 Core Domain Layer

### Domain Entities

```python
# core/domain/entities.py
@dataclass
class XKitContext:
    """Contexto completo do XKit v3.0"""
    project: ProjectInfo
    mcp_status: MCPStatus
    plugins: List[PluginInfo]
    ai_session: Optional[AISession] = None
    git: Optional[GitInfo] = None

@dataclass
class MCPStatus:
    """Status do sistema MCP"""
    servers: List[MCPServer]
    active_connections: int
    tools_available: List[MCPTool]
    
@dataclass  
class PluginInfo:
    """Informações de plugin"""
    name: str
    version: str
    loaded: bool
    hot_reload: bool
    commands: List[str]

@dataclass
class AISession:
    """Sessão ativa de IA"""
    model: str
    context: List[str]
    active: bool
    tokens_used: int
```

### Domain Interfaces

```python
# core/ports/ai_port.py
class AIPort(ABC):
    @abstractmethod
    async def analyze(self, context: str) -> AIResponse:
        pass
    
    @abstractmethod
    async def explain_code(self, code: str) -> str:
        pass
    
    @abstractmethod
    async def suggest_improvements(self, project_type: str) -> List[str]:
        pass

# core/ports/git_port.py
class GitPort(ABC):
    @abstractmethod
    def get_status(self) -> GitStatus:
        pass
    
    @abstractmethod
    def create_branch(self, name: str) -> bool:
        pass
    
    @abstractmethod
    def get_current_branch(self) -> str:
        pass
```

## 🔌 MCP Integration Layer

### MCP Client Protocol

```python
# mcp/client.py
class MCPClient:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.servers = {}
        self.active_connections = []
    
    async def connect_server(self, server_name: str) -> bool:
        """Conecta a um servidor MCP"""
        server_config = self.config.get(server_name)
        if not server_config:
            return False
        
        connection = await self._establish_connection(server_config)
        self.servers[server_name] = connection
        return True
    
    async def list_tools(self, server_name: str) -> List[MCPTool]:
        """Lista ferramentas disponíveis de um servidor"""
        server = self.servers.get(server_name)
        if not server:
            return []
        
        return await server.list_tools()
    
    async def call_tool(self, server_name: str, tool_name: str, 
                       arguments: dict) -> MCPResponse:
        """Executa uma ferramenta em um servidor MCP"""
        server = self.servers.get(server_name)
        if not server:
            raise MCPServerNotFound(server_name)
        
        return await server.call_tool(tool_name, arguments)
```

### Internal MCP Servers

```python
# mcp/servers/git_server.py
class GitMCPServer(MCPServer):
    def __init__(self):
        super().__init__("xkit-git", "1.0.0")
        self.git_adapter = GitAdapter()
    
    async def list_tools(self) -> List[MCPTool]:
        return [
            MCPTool(
                name="git-status",
                description="Get git repository status",
                input_schema={}
            ),
            MCPTool(
                name="git-create-branch", 
                description="Create new git branch",
                input_schema={"branch_name": {"type": "string"}}
            )
        ]
    
    async def call_tool(self, name: str, arguments: dict) -> str:
        if name == "git-status":
            status = self.git_adapter.get_status()
            return self._format_git_status(status)
        
        elif name == "git-create-branch":
            branch_name = arguments.get("branch_name")
            success = self.git_adapter.create_branch(branch_name)
            return f"✅ Branch {branch_name} created" if success else "❌ Failed"
        
        raise MCPToolNotFound(name)
```

## 🧩 Plugin System

### Plugin Architecture

```python
# plugins/base.py
class XKitPlugin(ABC):
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        self.loaded = False
        self.commands = {}
        self.event_handlers = {}
    
    @abstractmethod
    def load(self) -> None:
        """Carrega o plugin"""
        pass
    
    @abstractmethod
    def unload(self) -> None:
        """Descarrega o plugin"""
        pass
    
    def register_command(self, command: str, handler: Callable):
        """Registra um comando do plugin"""
        self.commands[command] = handler
    
    def register_event_handler(self, event_type: str, handler: Callable):
        """Registra um manipulador de eventos"""
        self.event_handlers[event_type] = handler

# plugins/manager.py
class PluginManager:
    def __init__(self, plugin_dir: Path):
        self.plugin_dir = plugin_dir
        self.loaded_plugins = {}
        self.registry = PluginRegistry()
    
    def load_plugin(self, plugin_name: str) -> bool:
        """Carrega um plugin dinamicamente"""
        try:
            plugin_module = self._import_plugin(plugin_name)
            plugin_class = self._get_plugin_class(plugin_module)
            
            plugin_instance = plugin_class()
            plugin_instance.load()
            
            self.loaded_plugins[plugin_name] = plugin_instance
            self.registry.register(plugin_instance)
            
            # Publish plugin loaded event
            event_bus.publish(PluginLoadedEvent(plugin_name))
            
            return True
        except Exception as e:
            logger.error(f"Failed to load plugin {plugin_name}: {e}")
            return False
    
    def hot_reload_plugin(self, plugin_name: str) -> bool:
        """Hot reload de um plugin"""
        if plugin_name in self.loaded_plugins:
            self.unload_plugin(plugin_name)
        
        return self.load_plugin(plugin_name)
```

## 📡 Event-Driven Architecture

### Event Bus System

```python
# events/bus.py
class EventBus:
    def __init__(self):
        self._subscribers = defaultdict(list)
        self._middleware = []
    
    def subscribe(self, event_type: Type[Event], 
                 handler: Callable[[Event], Awaitable[None]]):
        """Subscribe to an event type"""
        self._subscribers[event_type].append(handler)
    
    async def publish(self, event: Event):
        """Publish an event to all subscribers"""
        # Apply middleware
        for middleware in self._middleware:
            event = await middleware(event)
        
        # Notify subscribers
        handlers = self._subscribers[type(event)]
        await asyncio.gather(
            *[handler(event) for handler in handlers],
            return_exceptions=True
        )
    
    def add_middleware(self, middleware: Callable[[Event], Awaitable[Event]]):
        """Add event middleware"""
        self._middleware.append(middleware)

# events/events.py
@dataclass
class CommandExecutedEvent(Event):
    command: str
    arguments: Dict[str, Any]
    result: Any
    execution_time: float
    timestamp: datetime

@dataclass
class PluginLoadedEvent(Event):
    plugin_name: str
    plugin_version: str
    commands_registered: List[str]
    timestamp: datetime

@dataclass
class AIAnalysisEvent(Event):
    query: str
    response: str
    model_used: str
    tokens_consumed: int
    timestamp: datetime
```

### Event Handlers

```python
# events/handlers/command_handler.py
class CommandEventHandler:
    def __init__(self, logger: LoggerPort):
        self.logger = logger
    
    @event_bus.subscribe(CommandExecutedEvent)
    async def handle_command_executed(self, event: CommandExecutedEvent):
        """Log command execution"""
        self.logger.info(
            f"Command executed: {event.command} "
            f"({event.execution_time:.2f}ms)"
        )
        
        # Performance monitoring
        if event.execution_time > 1000:  # > 1s
            self.logger.warning(
                f"Slow command detected: {event.command}"
            )

# events/handlers/plugin_handler.py  
class PluginEventHandler:
    def __init__(self, display: DisplayPort):
        self.display = display
    
    @event_bus.subscribe(PluginLoadedEvent)
    async def handle_plugin_loaded(self, event: PluginLoadedEvent):
        """Display plugin loaded notification"""
        self.display.success(
            f"🧩 Plugin {event.plugin_name} v{event.plugin_version} loaded"
        )
        
        if event.commands_registered:
            commands = ", ".join(event.commands_registered)
            self.display.info(f"Commands registered: {commands}")
```

## ⚡ Performance & Optimization

### Startup Optimization

- **Lazy Loading**: Plugins carregados sob demanda
- **MCP Connection Pooling**: Reutilização de conexões
- **Event Bus Async**: Processamento assíncrono de eventos
- **Cache Strategy**: Cache inteligente para operações Git e AI

### Memory Management

- **Plugin Lifecycle**: Garbage collection automático de plugins
- **Event Buffer**: Buffer limitado para eventos
- **MCP Cleanup**: Limpeza automática de conexões inativas

### Hot-Reload Performance

```python
# Optimized hot-reload with minimal disruption
class OptimizedPluginLoader:
    async def hot_reload_plugin(self, plugin_name: str) -> bool:
        # 1. Create new plugin instance
        new_plugin = await self._create_plugin_instance(plugin_name)
        
        # 2. Transfer state from old plugin (if exists)
        if plugin_name in self.loaded_plugins:
            old_plugin = self.loaded_plugins[plugin_name]
            await self._transfer_state(old_plugin, new_plugin)
        
        # 3. Atomic replacement
        self.loaded_plugins[plugin_name] = new_plugin
        
        # 4. Clean up old plugin
        if 'old_plugin' in locals():
            await old_plugin.cleanup()
        
        return True
```

## 🔧 Configuration & Deployment

### MCP Configuration

```json
// mcp/config.json
{
  "servers": {
    "filesystem": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-filesystem", "/path/to/allowed/files"],
      "env": {}
    },
    "github": {
      "command": "npx", 
      "args": ["@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "xkit-internal": {
      "type": "internal",
      "class": "XKitInternalServer",
      "config": {
        "git_enabled": true,
        "ai_enabled": true,
        "project_analysis": true
      }
    }
  },
  "client": {
    "timeout": 5000,
    "retry_attempts": 3,
    "connection_pool_size": 10
  }
}
```

### Development Environment

```python
# Development configuration for hot-reload
DEVELOPMENT_CONFIG = {
    "plugins": {
        "auto_reload": True,
        "watch_files": True,
        "reload_on_change": ["*.py", "*.json"]
    },
    "mcp": {
        "development_mode": True,
        "verbose_logging": True,
        "mock_external_servers": True
    },
    "ai": {
        "cache_responses": True,
        "development_model": "gemini-1.5-flash-latest",
        "max_context_tokens": 1000000
    }
}
```

## 🚀 Migration Path

### From v2.1 to v3.0

1. **Phase 1**: MCP Core Implementation
   - Implement MCP client and protocol
   - Create internal MCP servers
   - Maintain v2.1 compatibility layer

2. **Phase 2**: Plugin System Migration
   - Convert existing modules to plugins
   - Implement hot-reload capability
   - Test plugin isolation

3. **Phase 3**: Event-Driven Refactor
   - Implement central event bus
   - Convert synchronous calls to events
   - Add event-based error handling

4. **Phase 4**: Hexagonal Architecture
   - Define ports and contracts
   - Implement adapters
   - Remove infrastructure dependencies from core

5. **Phase 5**: Performance Optimization
   - Optimize startup time
   - Implement caching strategies
   - Fine-tune hot-reload performance

---

**XKit v3.0 Hybrid MCP Architecture** - *Extensible, performant, and developer-friendly* 🏗️