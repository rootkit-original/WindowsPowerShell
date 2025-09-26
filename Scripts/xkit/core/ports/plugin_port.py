"""
Plugin Service Port
Interface for plugin management operations
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class PluginInfo:
    """Information about a plugin"""
    name: str
    version: str
    description: str
    status: str  # loaded, unloaded, error
    dependencies: List[str]
    commands: List[str]
    services: List[str]
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class IPluginService(ABC):
    """Port for plugin operations"""
    
    @abstractmethod
    async def load_plugin(self, plugin_path: str) -> bool:
        """Load a plugin from file"""
        pass
    
    @abstractmethod
    async def unload_plugin(self, plugin_name: str) -> bool:
        """Unload a plugin"""
        pass
    
    @abstractmethod
    async def reload_plugin(self, plugin_name: str) -> bool:
        """Reload a plugin"""
        pass
    
    @abstractmethod
    def list_plugins(self) -> List[PluginInfo]:
        """List all loaded plugins"""
        pass
    
    @abstractmethod
    def get_plugin_info(self, plugin_name: str) -> Optional[PluginInfo]:
        """Get information about a specific plugin"""
        pass
    
    @abstractmethod
    async def enable_hot_reload(self, plugin_paths: List[str]) -> bool:
        """Enable hot reload for plugin directories"""
        pass
    
    @abstractmethod
    def get_plugin_commands(self, plugin_name: str) -> List[str]:
        """Get commands provided by a plugin"""
        pass