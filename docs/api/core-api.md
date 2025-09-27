# 🏗️ Core API Reference

> **XKit v3.0 Python Core API Documentation**

This document provides comprehensive API reference for XKit's core Python components, following the hexagonal architecture pattern.

## 🎯 Quick Navigation

| Component | Description | Key Classes |
|-----------|-------------|-------------|
| [Application Layer](#application-layer) | Use cases and business logic | `XKitApplication`, `Container` |
| [Domain Layer](#domain-layer) | Core business entities | Domain models and value objects |
| [Ports](#ports) | Interface definitions | Abstract base classes for adapters |
| [Events](#events) | Event-driven communication | `EventBus`, `XKitEvent` |
| [Configuration](#configuration) | System configuration | `ConfigService`, `EnvironmentDetector` |

## 🏛️ Application Layer

### XKitApplication

Main application orchestrator that coordinates all system components.

```python
from xkit.core.application import XKitApplication

# Initialize application
app = XKitApplication()

# Execute command
result = await app.execute_command("git-status", ["--branch"])

# Get application status
status = app.get_status()
```

#### Methods

- `async execute_command(command: str, args: List[str]) -> CommandResult`
- `get_status() -> ApplicationStatus`
- `shutdown() -> None`
- `register_plugin(plugin: XKitPlugin) -> bool`

### Container (Dependency Injection)

Manages dependency injection and singleton services.

```python
from xkit.core.container import Container

# Get service instance
display_service = container.get_service("display_service")

# Register new service
container.register_singleton("custom_service", CustomService())

# Register factory
container.register_factory("temp_service", lambda: TempService())
```

#### Methods

- `get_service(name: str) -> Any`
- `register_singleton(name: str, instance: Any) -> None`
- `register_factory(name: str, factory: Callable) -> None`
- `has_service(name: str) -> bool`

## 🎯 Domain Layer

### Value Objects

Core value objects used throughout the system:

```python
from xkit.domain.models import CommandResult, GitStatus, ProjectInfo

# Command execution result
result = CommandResult(
    success=True,
    output="Command executed successfully",
    error=None,
    duration=0.5,
    metadata={"branch": "main"}
)

# Git repository status
git_status = GitStatus(
    branch="main",
    is_dirty=False,
    ahead=0,
    behind=0,
    staged_files=[],
    modified_files=[],
    untracked_files=[]
)
```

### Entities

Core business entities:

- `Project` - Represents a software project
- `Command` - Executable command definition
- `Plugin` - Plugin metadata and lifecycle
- `MCPServer` - MCP server configuration

## 🔌 Ports

Abstract interfaces for external adapters:

### Repository Ports

```python
from xkit.core.ports.repository_port import GitRepositoryPort

class CustomGitAdapter(GitRepositoryPort):
    async def get_status(self) -> GitStatus:
        # Implementation
        pass
    
    async def commit(self, message: str, files: List[str]) -> bool:
        # Implementation
        pass
```

### Display Port

```python
from xkit.core.ports.display_port import DisplayPort

class CustomDisplayAdapter(DisplayPort):
    def show_success(self, message: str, details: Dict = None) -> None:
        # Implementation
        pass
    
    def show_error(self, message: str, error: Exception = None) -> None:
        # Implementation
        pass
```

### AI Port

```python
from xkit.core.ports.ai_port import AIServicePort

class CustomAIAdapter(AIServicePort):
    async def analyze_error(self, error: str, context: Dict) -> AIAnalysis:
        # Implementation
        pass
    
    async def generate_code(self, prompt: str, language: str) -> str:
        # Implementation
        pass
```

## 📡 Events

### Event Bus

Central event system for loose coupling:

```python
from xkit.events.bus import EventBus
from xkit.events.events import CommandExecutedEvent

# Get event bus instance
event_bus = container.get_service("event_bus")

# Publish event
await event_bus.publish(CommandExecutedEvent(
    command="git-status",
    success=True,
    output="On branch main",
    duration=0.2
))

# Subscribe to events
@event_bus.subscribe(CommandExecutedEvent)
async def handle_command_executed(event: CommandExecutedEvent):
    print(f"Command {event.command} completed in {event.duration}s")

# Subscribe with conditions
@event_bus.subscribe(CommandExecutedEvent, 
                    condition=lambda e: not e.success)
async def handle_failed_command(event: CommandExecutedEvent):
    print(f"Command {event.command} failed!")
```

### Event Types

Core event types available:

- `CommandExecutedEvent` - Command execution completed
- `PluginLoadedEvent` - Plugin was loaded/unloaded
- `GitOperationEvent` - Git operation performed
- `ErrorOccurredEvent` - Error happened in system
- `MCPServerConnectedEvent` - MCP server connection status changed

## ⚙️ Configuration

### ConfigService

Centralized configuration management:

```python
from xkit.core.application import container

config = container.get_service("config_service")

# Get configuration values
git_path = config.get("git.executable_path")
ai_enabled = config.get("ai.enabled", default=False)

# Update configuration
config.set("display.theme", "dark")
config.save()
```

### Environment Detection

```python
from xkit.infrastructure.environment import EnvironmentDetector

detector = EnvironmentDetector()
env_info = detector.detect()

print(f"OS: {env_info.os_type}")
print(f"PowerShell: {env_info.powershell_version}")
print(f"Python: {env_info.python_version}")
print(f"Git: {env_info.git_available}")
```

## 🚀 Usage Examples

### Basic Command Execution

```python
import asyncio
from xkit.core.application import XKitApplication

async def main():
    app = XKitApplication()
    
    # Execute git status
    result = await app.execute_command("git-status", [])
    if result.success:
        print(f"✅ {result.output}")
    else:
        print(f"❌ {result.error}")

asyncio.run(main())
```

### Custom Service Integration

```python
from xkit.core.container import Container
from xkit.core.ports.display_port import DisplayPort

class CustomLogger(DisplayPort):
    def show_success(self, message: str, details: Dict = None):
        with open("xkit.log", "a") as f:
            f.write(f"SUCCESS: {message}\n")

# Register custom service
container = Container()
container.register_singleton("logger", CustomLogger())
```

### Event-Driven Plugin

```python
from xkit.plugins.base import XKitPlugin
from xkit.events.events import CommandExecutedEvent

class MonitoringPlugin(XKitPlugin):
    def __init__(self):
        super().__init__(PluginMetadata(
            name="monitoring",
            version="1.0.0",
            description="Command monitoring plugin"
        ))
    
    async def load(self):
        event_bus = self.get_service("event_bus")
        event_bus.subscribe(CommandExecutedEvent, self.on_command_executed)
    
    async def on_command_executed(self, event: CommandExecutedEvent):
        # Log command execution
        print(f"📊 Command: {event.command}, Duration: {event.duration}s")
```

## 🔗 Related Documentation

- **[MCP Protocol API](mcp-protocol.md)** - MCP client and server APIs
- **[Plugin API](plugin-api.md)** - Plugin development guide
- **[Event API](event-api.md)** - Event system detailed reference
- **[CLI Commands](cli-commands.md)** - Command-line interface reference

---

**Last Updated**: September 2025 | **Version**: v3.0.0  
**💙 Made with love by the XKit Community**