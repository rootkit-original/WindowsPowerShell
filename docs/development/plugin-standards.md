# 🔧 Plugin Development Standards

> **Comprehensive guidelines for XKit v3.0 plugin development**

## 🎯 **Overview**

This document defines the standards, conventions, and best practices for developing plugins in the XKit v3.0 ecosystem. Following these guidelines ensures consistency, maintainability, and seamless integration with the XKit architecture.

## 📁 **Plugin Structure Standards**

### **File Organization**
```
Scripts/xkit/plugins/
├── base.py                    ← Core plugin interfaces (DO NOT MODIFY)
├── manager.py                 ← Plugin manager (DO NOT MODIFY)
├── loader.py                  ← Plugin loader (DO NOT MODIFY)
├── your_plugin_name.py        ← Your plugin implementation
├── core/                      ← Essential system plugins
│   ├── __init__.py
│   └── system_plugin.py
└── integrations/              ← Third-party integration plugins
    ├── __init__.py
    └── integration_plugin.py
```

### **Naming Conventions**

#### **Files and Modules**
- **Plugin Files**: `{plugin_name}_plugin.py` (e.g., `telegram_plugin.py`)
- **Classes**: `XKit{PluginName}Plugin` (e.g., `XKitTelegramPlugin`)
- **Methods**: `snake_case` following PEP 8
- **Constants**: `UPPER_CASE_WITH_UNDERSCORES`

#### **Plugin Naming**
- **Plugin Name**: Use kebab-case for registration (e.g., `"telegram-bot"`)
- **Display Name**: Use human-readable format (e.g., `"Telegram Bot Integration"`)
- **Version**: Follow semantic versioning (e.g., `"1.2.3"`)

## 🏗️ **Plugin Architecture Standards**

### **Base Class Implementation**

All plugins **MUST** inherit from `XKitCorePlugin`:

```python
from xkit.plugins.base import XKitCorePlugin, PluginMetadata

class XKitMyPlugin(XKitCorePlugin):
    def __init__(self):
        super().__init__(
            name="my-plugin",
            version="1.0.0",
            description="Description of what your plugin does"
        )
    
    async def load(self) -> bool:
        """Initialize plugin - REQUIRED"""
        # Plugin initialization logic
        await self._initialize_services()
        self.logger.info(f"Plugin {self.name} loaded successfully")
        return True
    
    async def unload(self) -> bool:
        """Cleanup plugin - REQUIRED"""
        # Cleanup logic
        await self._cleanup_services()
        self.logger.info(f"Plugin {self.name} unloaded")
        return True
    
    def get_commands(self) -> Dict[str, Callable]:
        """Return plugin commands - REQUIRED"""
        return {
            "my-command": self.handle_my_command,
            "another-command": self.handle_another_command
        }
```

### **Required Plugin Interface**

Every plugin **MUST** implement these methods:

| Method | Purpose | Returns |
|--------|---------|---------|
| `async load() -> bool` | Initialize plugin resources | `True` if successful |
| `async unload() -> bool` | Cleanup plugin resources | `True` if successful |
| `get_commands() -> Dict[str, Callable]` | Return available commands | Command name → handler mapping |

### **Optional Plugin Features**

Plugins **MAY** implement these features:

| Feature | Method | Purpose |
|---------|---------|---------|
| **Services** | `get_services() -> Dict[str, Any]` | Provide services to other plugins |
| **Event Handling** | `_subscribe_to_events()` | React to system events |
| **Configuration** | `_load_config()` | Load plugin-specific configuration |
| **Health Checks** | `async health_check() -> bool` | Plugin health monitoring |

## 🔧 **Command Implementation Standards**

### **Command Handler Pattern**

```python
async def handle_command_name(self, args: List[str]) -> Optional[str]:
    """
    Handle the 'command-name' command
    
    Args:
        args: List of command arguments
    
    Returns:
        Optional[str]: Command output or None for silent execution
    
    Raises:
        PluginError: When command execution fails
    """
    try:
        # Validate arguments
        if not args:
            return "❌ Command requires arguments"
        
        # Process command
        result = await self._process_command(args)
        
        # Return formatted output
        return f"✅ Command completed: {result}"
        
    except Exception as e:
        self.logger.error(f"Command failed: {e}")
        raise PluginError(f"Command execution failed: {e}")
```

### **Command Documentation**
Each command **MUST** have:
- Clear docstring with purpose, arguments, and return value
- Input validation
- Error handling with appropriate logging
- Consistent output formatting with emojis for UX

### **Command Naming**
- Use kebab-case: `my-command`, `analyze-project`
- Be descriptive: `git-status` not `gs`
- Group related commands: `plugin-list`, `plugin-load`, `plugin-reload`

## 🔄 **Event Integration Standards**

### **Event Subscription**
```python
async def _initialize_services(self) -> None:
    """Initialize plugin services"""
    # Get event bus service
    self.event_bus = self.get_service("event_bus")
    
    # Subscribe to relevant events
    if self.event_bus:
        await self.event_bus.subscribe("command_executed", self._on_command_executed)
        await self.event_bus.subscribe("plugin_loaded", self._on_plugin_loaded)

async def _on_command_executed(self, event):
    """Handle command execution events"""
    if event.command.startswith("git-"):
        # React to git commands
        await self._handle_git_event(event)
```

### **Event Publishing**
```python
from xkit.events.events import PluginEvent

async def _publish_plugin_event(self, event_type: str, data: Dict[str, Any]):
    """Publish plugin-specific events"""
    if self.event_bus:
        event = PluginEvent(
            plugin_name=self.name,
            event_type=event_type,
            data=data
        )
        await self.event_bus.publish(event)
```

## 🗂️ **Service Integration Standards**

### **Using Core Services**
```python
async def _initialize_services(self) -> None:
    """Access XKit core services"""
    # Required services
    self.logger = self.get_service("logger")          # Always available
    self.config = self.get_service("config_service")  # Configuration
    self.display = self.get_service("display_service") # UI output
    
    # Optional services (check availability)
    self.event_bus = self.get_service("event_bus")    # Event system
    self.mcp_client = self.get_service("mcp_client")  # MCP integration
```

### **Providing Services**
```python
async def _initialize_services(self) -> None:
    """Provide services to other plugins"""
    # Register services this plugin provides
    self.register_service("my_custom_service", self.my_service_instance)
    self.register_service("data_processor", self.data_processor)

def get_services(self) -> Dict[str, Any]:
    """Return services provided by this plugin"""
    return {
        "my_custom_service": self.my_service_instance,
        "data_processor": self.data_processor
    }
```

## ⚙️ **Configuration Standards**

### **Configuration Structure**
```python
# config/plugins/my_plugin.json
{
    "enabled": true,
    "settings": {
        "api_key": "${MY_PLUGIN_API_KEY}",
        "timeout": 30,
        "max_retries": 3
    },
    "commands": {
        "my-command": {
            "enabled": true,
            "default_args": ["--verbose"]
        }
    }
}
```

### **Configuration Loading**
```python
async def _load_config(self) -> Dict[str, Any]:
    """Load plugin configuration"""
    config_service = self.get_service("config_service")
    if config_service:
        return await config_service.get_plugin_config(self.name)
    return {}
```

## 🧪 **Testing Standards**

### **Unit Testing Pattern**
```python
import pytest
from unittest.mock import AsyncMock, MagicMock
from xkit.plugins.your_plugin import XKitYourPlugin

@pytest.mark.asyncio
async def test_plugin_loading():
    """Test plugin loads successfully"""
    plugin = XKitYourPlugin()
    
    # Mock services
    plugin.get_service = MagicMock()
    plugin.get_service.return_value = MagicMock()
    
    # Test loading
    result = await plugin.load()
    assert result is True
    assert plugin.status == PluginStatus.LOADED

@pytest.mark.asyncio
async def test_command_execution():
    """Test command execution"""
    plugin = XKitYourPlugin()
    await plugin.load()
    
    # Test command
    result = await plugin.handle_my_command(["test", "args"])
    assert result is not None
    assert "✅" in result  # Check for success indicator
```

### **Integration Testing**
```python
@pytest.mark.asyncio
async def test_plugin_integration():
    """Test plugin integration with plugin manager"""
    from xkit.plugins.manager import PluginManager
    
    manager = PluginManager()
    await manager.initialize()
    
    # Load plugin
    success = await manager.load_plugin("my-plugin")
    assert success
    
    # Test plugin functionality
    plugin = manager.get_plugin("my-plugin")
    commands = plugin.get_commands()
    assert "my-command" in commands
```

## 📊 **Quality Standards**

### **Code Quality Requirements**
- **Type Hints**: All public methods must have type hints
- **Docstrings**: All classes and public methods must be documented
- **Error Handling**: Robust exception handling with logging
- **Logging**: Appropriate log levels (DEBUG, INFO, WARNING, ERROR)
- **Performance**: Commands should complete within 5 seconds for typical operations

### **Code Formatting**
```python
# Use black formatter with line length 100
# Configure in pyproject.toml:
[tool.black]
line-length = 100
target-version = ['py39']
```

### **Linting Standards**
```python
# Configure flake8 in setup.cfg:
[flake8]
max-line-length = 100
ignore = E203, W503  # Black compatibility
exclude = __pycache__, .git, build, dist
```

## 🚀 **Performance Guidelines**

### **Plugin Loading**
- Plugins should load in < 1 second
- Use lazy loading for heavy resources
- Initialize services asynchronously
- Avoid blocking operations in `load()`

### **Command Execution**
- Commands should respond in < 2 seconds
- Use async/await for I/O operations
- Implement progress indicators for long operations
- Cache expensive computations

### **Memory Management**
- Release resources in `unload()`
- Avoid memory leaks in event handlers
- Use weak references for callbacks
- Monitor memory usage in long-running operations

## 📝 **Documentation Requirements**

### **Plugin Documentation**
Each plugin **MUST** have:
- `docs/plugins/{plugin-name}.md` documentation file
- README section in the plugin file
- Command help text
- Configuration examples
- Usage examples

### **Documentation Template**
```markdown
# 🔌 {Plugin Name} Plugin

> **{Brief description of plugin functionality}**

## 📋 Features
- Feature 1
- Feature 2

## ⚙️ Configuration
```json
{config example}
```

## 🛠️ Commands
| Command | Description | Usage |
|---------|-------------|-------|
| `command-name` | Description | `command-name [args]` |

## 📖 Examples
{Usage examples}
```

## 🔗 **Related Standards**

- **[Code Organization Guide](./code-organization.md)** - Project structure standards
- **[Testing Guidelines](../development/testing.md)** - Testing strategies
- **[API Documentation](../api/plugin-api.md)** - Plugin API reference
- **[Architecture Overview](../architecture/plugin-system.md)** - Plugin system design

---

**Document Version**: v1.0  
**Last Updated**: September 27, 2025  
**Maintained by**: @rootkit-original

> 💡 **These standards are living guidelines** - Submit PRs to improve them based on community feedback!