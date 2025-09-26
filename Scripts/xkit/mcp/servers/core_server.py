"""
Core MCP Server
Provides core XKit functionality through MCP protocol
"""
import asyncio
from typing import Dict, Any, List, Optional
from pathlib import Path
import sys

from ..protocol import MCPServer, Tool


class XKitCoreServer(MCPServer):
    """Core XKit functionality MCP server"""
    
    def __init__(self):
        super().__init__("xkit-core", "1.0.0")
        self.xkit_root = Path(__file__).parent.parent.parent.parent
    
    async def list_tools(self) -> List[Tool]:
        """List available core tools"""
        return [
            Tool(
                name="system-info",
                description="Get XKit system information and status",
                input_schema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            Tool(
                name="list-commands",
                description="List all available XKit commands",
                input_schema={
                    "type": "object", 
                    "properties": {
                        "category": {
                            "type": "string",
                            "description": "Filter by command category",
                            "enum": ["git", "ai", "container", "telegram", "all"]
                        }
                    },
                    "required": []
                }
            ),
            Tool(
                name="execute-command",
                description="Execute a core XKit command",
                input_schema={
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string", 
                            "description": "Command to execute"
                        },
                        "args": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Command arguments"
                        }
                    },
                    "required": ["command"]
                }
            ),
            Tool(
                name="get-config",
                description="Get XKit configuration values",
                input_schema={
                    "type": "object",
                    "properties": {
                        "key": {
                            "type": "string",
                            "description": "Configuration key to retrieve"
                        }
                    },
                    "required": []
                }
            )
        ]
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a tool with given arguments"""
        if name == "system-info":
            return await self._get_system_info()
        elif name == "list-commands":
            category = arguments.get("category", "all")
            return await self._list_commands(category)
        elif name == "execute-command":
            command = arguments.get("command")
            args = arguments.get("args", [])
            return await self._execute_command(command, args)
        elif name == "get-config":
            key = arguments.get("key")
            return await self._get_config(key)
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    async def _get_system_info(self) -> Dict[str, Any]:
        """Get system information"""
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        
        return {
            "name": "XKit",
            "version": "3.0.0-hybrid",
            "architecture": "Hybrid MCP Architecture",
            "python_version": python_version,
            "platform": sys.platform,
            "xkit_root": str(self.xkit_root),
            "components": {
                "mcp_integration": "✅ Active",
                "plugin_system": "🔄 In Development", 
                "event_system": "🔄 In Development",
                "error_handler": "✅ Active",
                "ai_assistant": "✅ Active",
                "git_integration": "✅ Active"
            },
            "status": "🚀 Hybrid Architecture Implementation"
        }
    
    async def _list_commands(self, category: str) -> Dict[str, Any]:
        """List available commands by category"""
        all_commands = {
            "core": [
                "xkit-status", "xkit-info", "xkit-help", "xkit-version"
            ],
            "git": [
                "git-status", "git-commit", "git-push", "git-branch", "git-merge"
            ],
            "ai": [
                "ai-analyze", "ai-suggest", "ai-help", "ai-chat"
            ],
            "container": [
                "docker-status", "docker-list", "docker-exec"
            ],
            "telegram": [
                "tg-send", "tg-status", "tg-config"
            ]
        }
        
        if category == "all":
            return {
                "categories": list(all_commands.keys()),
                "commands": all_commands,
                "total_commands": sum(len(cmds) for cmds in all_commands.values())
            }
        elif category in all_commands:
            return {
                "category": category,
                "commands": all_commands[category],
                "count": len(all_commands[category])
            }
        else:
            return {"error": f"Unknown category: {category}"}
    
    async def _execute_command(self, command: str, args: List[str]) -> Dict[str, Any]:
        """Execute a core command"""
        # This would integrate with the existing XKit command system
        # For now, return a placeholder
        return {
            "command": command,
            "args": args,
            "status": "executed",
            "message": f"Command '{command}' executed via MCP",
            "note": "Integration with existing command system pending"
        }
    
    async def _get_config(self, key: Optional[str] = None) -> Dict[str, Any]:
        """Get configuration values"""
        # This would integrate with XKit configuration system
        base_config = {
            "xkit_version": "3.0.0-hybrid",
            "architecture": "hybrid-mcp",
            "python_first": True,
            "powershell_minimal": True,
            "mcp_enabled": True,
            "plugins_enabled": True,
            "events_enabled": True
        }
        
        if key:
            return {
                "key": key,
                "value": base_config.get(key, None),
                "found": key in base_config
            }
        
        return {
            "config": base_config,
            "source": "core_server",
            "count": len(base_config)
        }