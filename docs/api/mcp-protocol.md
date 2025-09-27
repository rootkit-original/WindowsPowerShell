# 🔌 MCP Protocol API Reference

> **Model Context Protocol Integration for XKit v3.0**

This document provides comprehensive documentation for XKit's MCP (Model Context Protocol) implementation, including client usage, server development, and protocol details.

## 🎯 Quick Navigation

| Section | Description |
|---------|-------------|
| [MCP Client](#mcp-client) | Using the MCP client to communicate with servers |
| [Internal MCP Servers](#internal-mcp-servers) | Built-in XKit MCP servers |
| [Server Development](#server-development) | Creating custom MCP servers |
| [Protocol Details](#protocol-details) | MCP protocol implementation |
| [Configuration](#configuration) | Server configuration and setup |

## 🧩 MCP Client

### XKitMCPClient

Main client for communicating with MCP servers:

```python
from xkit.mcp.client import XKitMCPClient
import asyncio

async def main():
    # Initialize client
    client = XKitMCPClient()
    
    # Connect to server
    success = await client.connect_server("xkit-core")
    if not success:
        print("Failed to connect to server")
        return
    
    # List available tools
    tools = await client.list_tools("xkit-core")
    for tool in tools:
        print(f"🔧 {tool.name}: {tool.description}")
    
    # Execute a tool
    result = await client.call_tool(
        "xkit-core", 
        "git-status", 
        {"format": "compact"}
    )
    print(f"Result: {result}")

asyncio.run(main())
```

### Client Methods

#### `async connect_server(server_name: str) -> bool`
Connects to an MCP server by name (from configuration).

```python
# Connect to internal server
await client.connect_server("xkit-ai")

# Connect to external server (if configured)
await client.connect_server("external-filesystem")
```

#### `async disconnect_server(server_name: str) -> bool`
Disconnects from an MCP server.

#### `async list_tools(server_name: str) -> List[Tool]`
Lists all available tools from a specific server.

```python
tools = await client.list_tools("xkit-git")
for tool in tools:
    print(f"Tool: {tool.name}")
    print(f"Description: {tool.description}")
    print(f"Input Schema: {tool.inputSchema}")
```

#### `async call_tool(server_name: str, tool_name: str, arguments: dict) -> Any`
Executes a tool on the specified server.

```python
# Git status with options
result = await client.call_tool("xkit-git", "git-status", {
    "branch": True,
    "porcelain": False
})

# AI code generation
code = await client.call_tool("xkit-ai", "generate-code", {
    "language": "python",
    "description": "Function to validate email addresses",
    "include_tests": True
})
```

## 🏗️ Internal MCP Servers

XKit comes with several built-in MCP servers:

### XKit Core Server (`xkit-core`)

Provides core XKit functionality:

```python
# Available tools:
tools = [
    "system-info",      # Get system information
    "project-analyze",  # Analyze current project
    "config-get",       # Get configuration values
    "config-set",       # Set configuration values
    "plugin-list",      # List loaded plugins
    "plugin-reload",    # Reload specific plugin
]

# Usage example
info = await client.call_tool("xkit-core", "system-info", {})
plugins = await client.call_tool("xkit-core", "plugin-list", {})
```

### XKit AI Server (`xkit-ai`)

AI-powered assistance and analysis:

```python
# Available tools:
tools = [
    "analyze-error",    # Analyze error messages
    "generate-code",    # Generate code from description
    "code-review",      # Review code for improvements
    "explain-command",  # Explain command functionality
    "suggest-fix",      # Suggest fixes for issues
]

# Usage examples
analysis = await client.call_tool("xkit-ai", "analyze-error", {
    "error": "ModuleNotFoundError: No module named 'requests'",
    "context": "Python project setup"
})

code = await client.call_tool("xkit-ai", "generate-code", {
    "language": "python",
    "description": "REST API client with retry logic",
    "framework": "requests"
})
```

### XKit Git Server (`xkit-git`)

Advanced Git operations:

```python
# Available tools:
tools = [
    "git-status",       # Enhanced git status
    "git-commit",       # Intelligent commit with AI
    "git-branch",       # Branch operations
    "git-history",      # Repository history analysis
    "git-conflicts",    # Merge conflict resolution
    "git-workflow",     # Smart workflow suggestions
]

# Usage examples
status = await client.call_tool("xkit-git", "git-status", {
    "format": "detailed",
    "include_suggestions": True
})

commit = await client.call_tool("xkit-git", "git-commit", {
    "files": ["src/main.py", "tests/test_main.py"],
    "auto_message": True,
    "conventional": True
})
```

## 🛠️ Server Development

### Creating Custom MCP Servers

Base class for creating MCP servers:

```python
from xkit.mcp.protocol import MCPServer, Tool, ToolResult
from typing import List, Dict, Any

class CustomMCPServer(MCPServer):
    def __init__(self):
        super().__init__("custom-server", "1.0.0")
        self.description = "Custom functionality server"
    
    async def list_tools(self) -> List[Tool]:
        """Return list of available tools"""
        return [
            Tool(
                name="hello",
                description="Say hello with custom message",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Name to greet"},
                        "language": {"type": "string", "default": "en"}
                    },
                    "required": ["name"]
                }
            ),
            Tool(
                name="calculate",
                description="Perform calculations",
                inputSchema={
                    "type": "object", 
                    "properties": {
                        "expression": {"type": "string"},
                        "format": {"type": "string", "enum": ["decimal", "fraction"]}
                    },
                    "required": ["expression"]
                }
            )
        ]
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> ToolResult:
        """Execute a tool and return results"""
        try:
            if name == "hello":
                return await self._handle_hello(arguments)
            elif name == "calculate":
                return await self._handle_calculate(arguments)
            else:
                raise ValueError(f"Unknown tool: {name}")
                
        except Exception as e:
            return ToolResult(
                content=[{"type": "text", "text": f"Error: {str(e)}"}],
                isError=True
            )
    
    async def _handle_hello(self, args: Dict[str, Any]) -> ToolResult:
        name = args["name"]
        language = args.get("language", "en")
        
        greetings = {
            "en": f"Hello, {name}!",
            "es": f"¡Hola, {name}!",
            "fr": f"Bonjour, {name}!",
            "pt": f"Olá, {name}!"
        }
        
        greeting = greetings.get(language, greetings["en"])
        
        return ToolResult(
            content=[{
                "type": "text",
                "text": greeting
            }]
        )
    
    async def _handle_calculate(self, args: Dict[str, Any]) -> ToolResult:
        expression = args["expression"]
        format_type = args.get("format", "decimal")
        
        # Safe evaluation (implement proper parsing)
        try:
            result = eval(expression)  # Use ast.literal_eval for safety
            
            if format_type == "fraction":
                from fractions import Fraction
                result = str(Fraction(result).limit_denominator())
            
            return ToolResult(
                content=[{
                    "type": "text",
                    "text": f"{expression} = {result}"
                }]
            )
        except Exception as e:
            raise ValueError(f"Invalid expression: {expression}")
```

### Registering Custom Servers

Add your server to the MCP configuration:

```json
{
  "servers": {
    "custom-server": {
      "type": "internal",
      "module": "my_package.custom_server",
      "class": "CustomMCPServer",
      "description": "My custom MCP server",
      "enabled": true
    }
  }
}
```

### External Server Connection

Connect to external MCP servers:

```json
{
  "servers": {
    "filesystem": {
      "type": "stdio",
      "command": "npx",
      "args": ["@modelcontextprotocol/server-filesystem", "/path/to/files"],
      "description": "File system operations",
      "enabled": true
    },
    "postgres": {
      "type": "stdio", 
      "command": "uvx",
      "args": ["mcp-server-postgres", "--connection-string", "postgresql://..."],
      "description": "PostgreSQL database operations",
      "enabled": false
    }
  }
}
```

## 📡 Protocol Details

### MCPMessage Structure

```python
@dataclass
class MCPMessage:
    """Base MCP message structure"""
    jsonrpc: str = "2.0"
    id: Optional[str] = None
    method: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
    result: Optional[Any] = None
    error: Optional[MCPError] = None
```

### Tool Definition

```python
@dataclass
class Tool:
    """MCP Tool definition"""
    name: str
    description: str
    inputSchema: Dict[str, Any]  # JSON Schema for input validation
```

### Tool Result

```python
@dataclass  
class ToolResult:
    """Tool execution result"""
    content: List[Dict[str, Any]]
    isError: bool = False
    _meta: Optional[Dict[str, Any]] = None
```

### Connection Types

#### STDIO Connection
For external processes:

```python
{
  "type": "stdio",
  "command": "python",
  "args": ["-m", "my_server"],
  "cwd": "/path/to/server",
  "env": {"PYTHONPATH": "/custom/path"}
}
```

#### Internal Connection
For Python classes:

```python
{
  "type": "internal",
  "module": "my_package.server",
  "class": "MyServer",
  "config": {"custom": "settings"}
}
```

## ⚙️ Configuration

### Server Configuration File

Located at `Scripts/xkit/mcp/config.json`:

```json
{
  "version": "1.0.0",
  "description": "XKit MCP Server Configuration",
  "servers": {
    "server-name": {
      "type": "internal|stdio|http",
      "enabled": true,
      "description": "Server description",
      // Type-specific configuration
    }
  },
  "connection_pool": {
    "max_connections": 10,
    "idle_timeout": 300,
    "reconnect_attempts": 3,
    "reconnect_delay": 1.0
  },
  "logging": {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  }
}
```

### Environment Variables

- `XKIT_MCP_CONFIG` - Path to MCP configuration file
- `XKIT_MCP_LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)
- `XKIT_MCP_MAX_CONNECTIONS` - Maximum concurrent connections
- `XKIT_MCP_TIMEOUT` - Request timeout in seconds

## 🚀 Usage Examples

### Command Line Integration

```powershell
# List MCP servers
xkit mcp list-servers

# Connect to external server
xkit mcp connect --server filesystem --command "npx @modelcontextprotocol/server-filesystem"

# List tools from server
xkit mcp list-tools --server xkit-ai

# Execute tool
xkit mcp call-tool --server xkit-git --tool git-status --args '{"branch": true}'
```

### Plugin Integration

```python
from xkit.plugins.base import XKitPlugin
from xkit.mcp.client import XKitMCPClient

class MCPIntegrationPlugin(XKitPlugin):
    def __init__(self):
        super().__init__(PluginMetadata(
            name="mcp-integration",
            version="1.0.0", 
            description="MCP server integration"
        ))
        self.mcp_client = None
    
    async def load(self):
        self.mcp_client = self.get_service("mcp_client")
        
        # Register custom commands that use MCP
        self.register_command("ai-analyze", self.ai_analyze)
        self.register_command("smart-commit", self.smart_commit)
    
    async def ai_analyze(self, args: List[str]) -> str:
        """Analyze code using AI server"""
        code = " ".join(args)
        result = await self.mcp_client.call_tool(
            "xkit-ai", "analyze-code", {"code": code}
        )
        return result["analysis"]
    
    async def smart_commit(self, args: List[str]) -> str:
        """Create intelligent commit using Git + AI servers"""
        # Get git status
        status = await self.mcp_client.call_tool("xkit-git", "git-status", {})
        
        # Generate commit message with AI
        message = await self.mcp_client.call_tool(
            "xkit-ai", "generate-commit-message", 
            {"changes": status["changes"]}
        )
        
        # Perform commit
        result = await self.mcp_client.call_tool(
            "xkit-git", "git-commit", 
            {"message": message["message"], "files": args}
        )
        
        return result["summary"]
```

## 🔧 Troubleshooting

### Common Issues

1. **Server Connection Failed**
   ```python
   # Check server configuration
   client = XKitMCPClient()
   config = client.get_server_config("server-name")
   print(f"Config: {config}")
   
   # Test connection manually
   success = await client.connect_server("server-name")
   if not success:
       print("Check server configuration and dependencies")
   ```

2. **Tool Not Found**
   ```python
   # List available tools
   tools = await client.list_tools("server-name")
   available_tools = [tool.name for tool in tools]
   print(f"Available tools: {available_tools}")
   ```

3. **Invalid Arguments**
   ```python
   # Check tool schema
   tools = await client.list_tools("server-name")
   tool = next(t for t in tools if t.name == "tool-name")
   print(f"Required schema: {tool.inputSchema}")
   ```

### Debug Mode

Enable debug logging:

```python
import logging
logging.getLogger("xkit.mcp").setLevel(logging.DEBUG)

# Or set environment variable
import os
os.environ["XKIT_MCP_LOG_LEVEL"] = "DEBUG"
```

## 🔗 Related Documentation

- **[Core API](core-api.md)** - XKit Core Python API
- **[Plugin API](plugin-api.md)** - Plugin development guide
- **[CLI Commands](cli-commands.md)** - Command-line interface

---

**Last Updated**: September 2025 | **Version**: v3.0.0  
**💙 Built on the MCP Protocol by Anthropic**