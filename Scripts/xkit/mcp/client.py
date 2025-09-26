"""
MCP Client Implementation
Advanced MCP client with connection pooling and server management
"""
import asyncio
import json
import logging
import subprocess
import tempfile
from typing import Dict, Any, List, Optional, Union, Callable
from pathlib import Path

from .protocol import MCPClient, MCPProtocol, MCPMessage, Tool, MCPError


class MCPConnectionPool:
    """Manages connections to multiple MCP servers with pooling"""
    
    def __init__(self, max_connections: int = 10):
        self.max_connections = max_connections
        self.connections: Dict[str, Dict[str, Any]] = {}
        self.active_connections = 0
        self.lock = asyncio.Lock()
    
    async def get_connection(self, server_name: str, server_config: Dict[str, Any]):
        """Get or create a connection to an MCP server"""
        async with self.lock:
            if server_name in self.connections:
                conn = self.connections[server_name]
                if conn["status"] == "active":
                    return conn
            
            if self.active_connections >= self.max_connections:
                await self._cleanup_idle_connections()
            
            conn = await self._create_connection(server_name, server_config)
            self.connections[server_name] = conn
            self.active_connections += 1
            return conn
    
    async def _create_connection(self, server_name: str, config: Dict[str, Any]):
        """Create a new connection to an MCP server"""
        connection_type = config.get("type", "stdio")
        
        if connection_type == "stdio":
            return await self._create_stdio_connection(server_name, config)
        elif connection_type == "internal":
            return await self._create_internal_connection(server_name, config)
        else:
            raise ValueError(f"Unsupported connection type: {connection_type}")
    
    async def _create_stdio_connection(self, server_name: str, config: Dict[str, Any]):
        """Create a stdio-based connection to an external MCP server"""
        command = config.get("command")
        args = config.get("args", [])
        
        if not command:
            raise ValueError(f"No command specified for server {server_name}")
        
        process = await asyncio.create_subprocess_exec(
            command, *args,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        return {
            "type": "stdio",
            "process": process,
            "status": "active",
            "server_name": server_name,
            "last_used": asyncio.get_event_loop().time()
        }
    
    async def _create_internal_connection(self, server_name: str, config: Dict[str, Any]):
        """Create a connection to an internal MCP server"""
        module_path = config.get("module")
        class_name = config.get("class")
        
        if not module_path or not class_name:
            raise ValueError(f"Module path and class name required for internal server {server_name}")
        
        # Dynamic import and instantiation
        module = __import__(module_path, fromlist=[class_name])
        server_class = getattr(module, class_name)
        server_instance = server_class()
        
        return {
            "type": "internal",
            "instance": server_instance,
            "status": "active",
            "server_name": server_name,
            "last_used": asyncio.get_event_loop().time()
        }
    
    async def _cleanup_idle_connections(self):
        """Clean up idle connections to make room for new ones"""
        current_time = asyncio.get_event_loop().time()
        idle_threshold = 300  # 5 minutes
        
        idle_connections = [
            name for name, conn in self.connections.items()
            if current_time - conn["last_used"] > idle_threshold
        ]
        
        for name in idle_connections:
            await self.close_connection(name)
    
    async def close_connection(self, server_name: str):
        """Close a specific connection"""
        if server_name in self.connections:
            conn = self.connections[server_name]
            
            if conn["type"] == "stdio" and "process" in conn:
                process = conn["process"]
                if process.returncode is None:
                    process.terminate()
                    try:
                        await asyncio.wait_for(process.wait(), timeout=5.0)
                    except asyncio.TimeoutError:
                        process.kill()
            
            del self.connections[server_name]
            self.active_connections = max(0, self.active_connections - 1)
    
    async def close_all(self):
        """Close all connections"""
        for server_name in list(self.connections.keys()):
            await self.close_connection(server_name)


class XKitMCPClient(MCPClient):
    """Enhanced MCP Client for XKit with connection pooling and configuration management"""
    
    def __init__(self, config_path: Optional[Path] = None):
        super().__init__()
        self.config_path = config_path or Path(__file__).parent / "config.json"
        self.connection_pool = MCPConnectionPool()
        self.servers_config: Dict[str, Any] = {}
        self.logger = logging.getLogger(__name__)
        self._config_loaded = False
        
        # Don't load config in __init__ to avoid async issues
        # Will be loaded on first use
    
    async def _load_config(self):
        """Load MCP servers configuration"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.servers_config = config.get("servers", {})
                    self.logger.info(f"Loaded {len(self.servers_config)} MCP server configurations")
            else:
                self.logger.warning(f"Config file not found: {self.config_path}")
                self.servers_config = {}
        except Exception as e:
            self.logger.error(f"Failed to load MCP config: {e}")
            self.servers_config = {}
        finally:
            self._config_loaded = True
    
    async def _ensure_config_loaded(self):
        """Ensure configuration is loaded before operations"""
        if not self._config_loaded:
            await self._load_config()
    
    async def _send_request(self, server_name: str, request: MCPMessage) -> MCPMessage:
        """Send request to server using connection pool"""
        await self._ensure_config_loaded()
        
        if server_name not in self.servers_config:
            raise ValueError(f"Unknown MCP server: {server_name}")
        
        server_config = self.servers_config[server_name]
        connection = await self.connection_pool.get_connection(server_name, server_config)
        
        try:
            if connection["type"] == "stdio":
                return await self._send_stdio_request(connection, request)
            elif connection["type"] == "internal":
                return await self._send_internal_request(connection, request)
            else:
                raise ValueError(f"Unsupported connection type: {connection['type']}")
        finally:
            connection["last_used"] = asyncio.get_event_loop().time()
    
    async def _send_stdio_request(self, connection: Dict[str, Any], request: MCPMessage) -> MCPMessage:
        """Send request via stdio to external process"""
        process = connection["process"]
        message_data = self.protocol.serialize_message(request) + "\n"
        
        process.stdin.write(message_data.encode('utf-8'))
        await process.stdin.drain()
        
        # Read response
        response_line = await process.stdout.readline()
        if not response_line:
            raise Exception("No response from MCP server")
        
        response_data = response_line.decode('utf-8').strip()
        return self.protocol.parse_message(response_data)
    
    async def _send_internal_request(self, connection: Dict[str, Any], request: MCPMessage) -> MCPMessage:
        """Send request to internal server instance"""
        server_instance = connection["instance"]
        return await server_instance.handle_request(request)
    
    async def list_all_tools(self) -> Dict[str, List[Tool]]:
        """List tools from all configured servers"""
        all_tools = {}
        
        for server_name in self.servers_config.keys():
            try:
                tools = await self.list_tools(server_name)
                all_tools[server_name] = tools
            except Exception as e:
                self.logger.error(f"Failed to list tools from {server_name}: {e}")
                all_tools[server_name] = []
        
        return all_tools
    
    async def find_tool(self, tool_name: str) -> Optional[tuple[str, Tool]]:
        """Find a tool by name across all servers"""
        all_tools = await self.list_all_tools()
        
        for server_name, tools in all_tools.items():
            for tool in tools:
                if tool.name == tool_name:
                    return (server_name, tool)
        
        return None
    
    async def call_tool_by_name(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Call a tool by name, automatically finding the correct server"""
        result = await self.find_tool(tool_name)
        if not result:
            raise ValueError(f"Tool not found: {tool_name}")
        
        server_name, tool = result
        return await self.call_tool(server_name, tool_name, arguments)
    
    async def health_check(self) -> Dict[str, bool]:
        """Check health of all configured servers"""
        health_status = {}
        
        for server_name in self.servers_config.keys():
            try:
                await self.list_tools(server_name)
                health_status[server_name] = True
            except Exception as e:
                self.logger.error(f"Health check failed for {server_name}: {e}")
                health_status[server_name] = False
        
        return health_status
    
    async def reload_config(self):
        """Reload server configuration"""
        await self._load_config()
    
    async def start_client(self) -> None:
        """Start the MCP client and initialize connections"""
        await self._ensure_config_loaded()
        self.logger.info("MCP Client started")
    
    async def stop_client(self) -> None:
        """Stop the MCP client"""
        await self.shutdown()
        self.logger.info("MCP Client stopped")
    
    async def shutdown(self):
        """Shutdown client and close all connections"""
        await self.connection_pool.close_all()
        self.logger.info("MCP Client shutdown complete")


# Global instance
_mcp_client: Optional[XKitMCPClient] = None


async def get_mcp_client() -> XKitMCPClient:
    """Get or create global MCP client instance"""
    global _mcp_client
    if _mcp_client is None:
        _mcp_client = XKitMCPClient()
        await _mcp_client._load_config()
    return _mcp_client


async def shutdown_mcp_client():
    """Shutdown global MCP client"""
    global _mcp_client
    if _mcp_client:
        await _mcp_client.shutdown()
        _mcp_client = None