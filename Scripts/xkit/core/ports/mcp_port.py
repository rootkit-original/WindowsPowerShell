"""
MCP Service Port
Interface for Model Context Protocol integration
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class MCPServerInfo:
    """Information about an MCP server"""
    name: str
    version: str
    server_type: str  # internal, stdio, etc.
    status: str
    tools: List[str]
    connection_info: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.connection_info is None:
            self.connection_info = {}


@dataclass
class MCPToolCall:
    """MCP tool call request"""
    server_name: str
    tool_name: str
    arguments: Dict[str, Any]
    timeout: Optional[float] = None
    
    def __post_init__(self):
        if self.arguments is None:
            self.arguments = {}


@dataclass
class MCPToolResult:
    """Result of MCP tool execution"""
    success: bool
    result: Any = None
    error: Optional[str] = None
    execution_time: float = 0.0
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class IMCPService(ABC):
    """Port for MCP operations"""
    
    @abstractmethod
    async def start_client(self) -> bool:
        """Start MCP client"""
        pass
    
    @abstractmethod
    async def stop_client(self) -> bool:
        """Stop MCP client"""
        pass
    
    @abstractmethod
    async def connect_server(self, server_name: str,
                           config: Dict[str, Any]) -> bool:
        """Connect to an MCP server"""
        pass
    
    @abstractmethod
    async def disconnect_server(self, server_name: str) -> bool:
        """Disconnect from an MCP server"""
        pass
    
    @abstractmethod
    async def list_servers(self) -> List[MCPServerInfo]:
        """List all connected MCP servers"""
        pass
    
    @abstractmethod
    async def list_tools(self, server_name: Optional[str] = None) -> Dict[str, List[str]]:
        """List available tools from MCP servers"""
        pass
    
    @abstractmethod
    async def call_tool(self, tool_call: MCPToolCall) -> MCPToolResult:
        """Call an MCP tool"""
        pass
    
    @abstractmethod
    async def health_check(self, server_name: str) -> bool:
        """Check health of an MCP server"""
        pass
    
    @abstractmethod
    async def reload_server(self, server_name: str) -> bool:
        """Reload an MCP server"""
        pass
    
    @abstractmethod
    def get_server_config(self, server_name: str) -> Optional[Dict[str, Any]]:
        """Get configuration for an MCP server"""
        pass