# 🔧 API Reference - XKit v3.0.0

## 🏗️ Hybrid MCP Architecture API

### 🔌 MCP Integration Layer

#### MCP Client Usage
```python
from xkit.mcp.client import XKitMCPClient

# Conectar a MCP server
client = XKitMCPClient()
await client.connect_server("core-server", "stdio")

# Listar tools disponíveis
tools = await client.list_tools("core-server")

# Executar tool
result = await client.call_tool("core-server", "git-status", {})
```

#### MCP Server Development
```python
from xkit.mcp.servers.base import XKitMCPServer
from xkit.mcp.protocol import Tool, ToolResult

class CustomMCPServer(XKitMCPServer):
    def __init__(self):
        super().__init__("custom-server", "1.0.0")
    
    async def list_tools(self) -> List[Tool]:
        return [
            Tool(
                name="custom-command",
                description="Execute custom logic",
                inputSchema={
                    "type": "object", 
                    "properties": {"param": {"type": "string"}}
                }
            )
        ]
    
    async def call_tool(self, name: str, arguments: dict) -> ToolResult:
        if name == "custom-command":
            return ToolResult(content=[
                {"type": "text", "text": f"Result: {arguments.get('param')}"}
            ])
```

### 🧩 Plugin System API

#### Plugin Development
```python
from xkit.plugins.base import XKitPlugin

class GitPlugin(XKitPlugin):
    def __init__(self):
        super().__init__("git-plugin", "3.0.0")
        self.commands = {
            "git-status": self.git_status,
            "git-commit": self.git_commit
        }
    
    async def load(self) -> None:
        """Initialize plugin"""
        self.logger.info("Git plugin loaded")
        
    async def unload(self) -> None:
        """Cleanup plugin"""
        self.logger.info("Git plugin unloaded")
        
    def git_status(self, args: list) -> str:
        """Enhanced git status"""
        # Implementation here
        return "Git status result"
```

#### Plugin Manager Usage
```python
from xkit.plugins.manager import PluginManager

plugin_manager = PluginManager()

# Load plugin
await plugin_manager.load_plugin("git-plugin")

# Reload plugin (hot-reload)
await plugin_manager.reload_plugin("git-plugin")

# List loaded plugins
plugins = plugin_manager.list_plugins()
```

### 📡 Event-Driven API

#### Event System Usage
```python
from xkit.events import EventBus, SystemStartedEvent, CommandExecutedEvent

# Get event bus instance
event_bus = EventBus.get_instance()

# Publish event
await event_bus.publish(CommandExecutedEvent(
    command="git-status",
    result="success", 
    execution_time=45.2
))

# Subscribe to events
@event_bus.subscribe(CommandExecutedEvent)
async def handle_command_executed(event: CommandExecutedEvent):
    print(f"Command {event.command} executed in {event.execution_time}ms")
```

#### Custom Event Creation
```python
from xkit.events.base import XKitEvent
from dataclasses import dataclass
from datetime import datetime

@dataclass
class CustomEvent(XKitEvent):
    message: str
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
```

### 🏗️ Core Application API

#### Command Service
```python
from xkit.core.application.command_service import CommandService

command_service = CommandService()

# Execute command with error handling
result = await command_service.execute_command(
    action="git-status",
    params=["--porcelain"],
    context={"project_path": "/path/to/project"}
)
```

#### AI Service Integration
```python
from xkit.core.application.ai_service import AIService

ai_service = AIService()

# Analyze code with context
analysis = await ai_service.analyze_code(
    code="def fibonacci(n): return n if n <= 1 else fib(n-1) + fib(n-2)",
    context="Performance optimization needed"
)

# Get AI suggestions
suggestions = await ai_service.get_suggestions(
    query="How to implement Redis cache in Python?",
    project_context={"type": "flask", "db": "postgresql"}
)
```

### 🔧 Infrastructure Adapters

#### Git Adapter
```python
from xkit.adapters.git import GitAdapter

git_adapter = GitAdapter()

# Enhanced git operations
status = await git_adapter.get_status_enhanced()
branch_info = await git_adapter.create_branch_intelligent("feature/new")
```

#### Display Adapter  
```python
from xkit.adapters.display import DisplayAdapter

display = DisplayAdapter()

# Rich console output
display.success("🎉 Operation completed!")
display.warning("⚠️ Configuration needed")
display.error("❌ Critical error occurred")

# Progress indicators
with display.progress("Processing files...") as progress:
    for file in files:
        progress.update(f"Processing {file}")
```

### 🔄 Configuration API

#### Application Configuration
```python
from xkit.core.application import ApplicationConfig

config = ApplicationConfig()

# Access configuration
gemini_key = config.get_ai_config().gemini_api_key
telegram_token = config.get_telegram_config().bot_token

# Environment detection
is_dev = config.is_development_mode()
debug_enabled = config.is_debug_enabled()
```

## 📝 PowerShell Integration

### Creating New Commands

#### 1. Python Implementation
```python
# Add to xkit_main.py actions dict
async def my_custom_action(params: list) -> str:
    """Custom action implementation"""
    result = await my_business_logic(params)
    return result

# Register action
actions["my-action"] = my_custom_action
```

#### 2. PowerShell Wrapper
```powershell
# Add to profile or custom module
function global:my-command {
    param([Parameter(ValueFromRemainingArguments)]$args)
    Invoke-XKit "my-action" @args
}
```

### 🔌 Advanced PowerShell Functions

```powershell
# Modern XKit command pattern
function global:xkit-advanced {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Action,
        
        [Parameter(ValueFromRemainingArguments)]
        [string[]]$Arguments
    )
    
    # Call Python backend with error handling
    try {
        $result = python "$PSScriptRoot\Scripts\xkit_main.py" $Action @Arguments
        return $result
    }
    catch {
        Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
        # Trigger AI error analysis
        python "$PSScriptRoot\Scripts\xkit_main.py" "error-analyze" $_.Exception.Message
    }
}
```

## 🧪 Testing API

### Unit Testing
```python
import pytest
from xkit.core.application import CommandService

@pytest.fixture
def command_service():
    return CommandService()

async def test_git_status(command_service):
    result = await command_service.execute_command("git-status", [])
    assert result is not None
    assert "status" in result
```

### Integration Testing
```python
import pytest
from xkit.mcp.client import XKitMCPClient

@pytest.mark.asyncio
async def test_mcp_server_connection():
    client = XKitMCPClient()
    await client.connect_server("test-server", "stdio")
    tools = await client.list_tools("test-server")
    assert len(tools) > 0
```

---

## 🔗 Links Relacionados

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Arquitetura técnica detalhada
- **[USAGE.md](USAGE.md)** - Exemplos práticos de uso
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Guia de desenvolvimento
- **[Plugin Development Guide](plugins/README.md)** - Como criar plugins

*Para exemplos mais completos, veja o código fonte em `Scripts/xkit/`*