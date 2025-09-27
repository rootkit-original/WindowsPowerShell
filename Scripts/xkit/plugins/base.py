"""
XKit Plugin Base Classes
Defines the interface and base functionality for XKit plugins
"""
import asyncio
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum


class PluginStatus(Enum):
    """Plugin status enumeration"""
    UNLOADED = "unloaded"
    LOADING = "loading"
    LOADED = "loaded"
    ACTIVE = "active"
    ERROR = "error"
    UNLOADING = "unloading"


@dataclass
class PluginMetadata:
    """Plugin metadata information"""
    name: str
    version: str
    description: str
    author: str
    dependencies: List[str]
    provides: List[str]  # Services/commands this plugin provides
    requires: List[str]  # Services this plugin requires
    hot_reload: bool = True
    priority: int = 100  # Loading priority (lower = higher priority)


class PluginEvent:
    """Base class for plugin events"""
    def __init__(self, plugin_name: str, event_type: str, data: Any = None):
        self.plugin_name = plugin_name
        self.event_type = event_type
        self.data = data
        self.timestamp = asyncio.get_event_loop().time()


class XKitPlugin(ABC):
    """Abstract base class for all XKit plugins"""
    
    def __init__(self, metadata: PluginMetadata):
        self.metadata = metadata
        self.status = PluginStatus.UNLOADED
        self.error_message: Optional[str] = None
        self.event_handlers: Dict[str, List[Callable]] = {}
        self.services: Dict[str, Any] = {}
        self.commands: Dict[str, Callable] = {}
    
    @abstractmethod
    async def load(self) -> bool:
        """Load the plugin. Return True if successful."""
        pass
    
    @abstractmethod
    async def unload(self) -> bool:
        """Unload the plugin. Return True if successful."""
        pass
    
    async def reload(self) -> bool:
        """Reload the plugin. Default implementation unloads then loads."""
        if self.status == PluginStatus.ACTIVE:
            await self.unload()
        return await self.load()
    
    @abstractmethod
    def get_commands(self) -> Dict[str, Callable]:
        """Return dictionary of commands provided by this plugin"""
        pass
    
    def get_services(self) -> Dict[str, Any]:
        """Return dictionary of services provided by this plugin"""
        return self.services.copy()
    
    def register_service(self, name: str, service: Any) -> None:
        """Register a service provided by this plugin"""
        self.services[name] = service
    
    def unregister_service(self, name: str) -> None:
        """Unregister a service"""
        if name in self.services:
            del self.services[name]
    
    def register_event_handler(self, event_type: str, handler: Callable) -> None:
        """Register an event handler"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
    
    def unregister_event_handler(self, event_type: str, handler: Callable) -> None:
        """Unregister an event handler"""
        if event_type in self.event_handlers:
            try:
                self.event_handlers[event_type].remove(handler)
            except ValueError:
                pass
    
    async def handle_event(self, event: PluginEvent) -> None:
        """Handle an event if we have handlers for it"""
        handlers = self.event_handlers.get(event.event_type, [])
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)
            except Exception as e:
                self.error_message = f"Event handler error: {str(e)}"
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform a health check on the plugin"""
        return {
            "plugin": self.metadata.name,
            "status": self.status.value,
            "error": self.error_message,
            "services": list(self.services.keys()),
            "commands": list(self.commands.keys()),
            "healthy": self.status == PluginStatus.ACTIVE and not self.error_message
        }
    
    def set_status(self, status: PluginStatus, error_message: Optional[str] = None) -> None:
        """Set plugin status and error message"""
        self.status = status
        if error_message:
            self.error_message = error_message
        elif status != PluginStatus.ERROR:
            self.error_message = None


class XKitCorePlugin(XKitPlugin):
    """Base class for core XKit plugins with common functionality"""
    
    def __init__(self, name: str, version: str = "1.0.0", description: str = ""):
        metadata = PluginMetadata(
            name=name,
            version=version,
            description=description or f"Core {name} plugin",
            author="XKit Framework",
            dependencies=[],
            provides=[name],
            requires=[],
            hot_reload=True,
            priority=50  # Core plugins have higher priority
        )
        super().__init__(metadata)
    
    @property
    def name(self) -> str:
        """Convenience property for plugin name"""
        return self.metadata.name
        
    @property  
    def version(self) -> str:
        """Convenience property for plugin version"""
        return self.metadata.version
        
    @property
    def description(self) -> str:
        """Convenience property for plugin description"""
        return self.metadata.description
    
    async def load(self) -> bool:
        """Default load implementation for core plugins"""
        try:
            self.set_status(PluginStatus.LOADING)
            
            # Register commands
            self.commands = self.get_commands()
            
            # Initialize services
            await self._initialize_services()
            
            self.set_status(PluginStatus.ACTIVE)
            return True
            
        except Exception as e:
            self.set_status(PluginStatus.ERROR, str(e))
            return False
    
    async def unload(self) -> bool:
        """Default unload implementation for core plugins"""
        try:
            self.set_status(PluginStatus.UNLOADING)
            
            # Cleanup services
            await self._cleanup_services()
            
            # Clear commands and services
            self.commands.clear()
            self.services.clear()
            
            self.set_status(PluginStatus.UNLOADED)
            return True
            
        except Exception as e:
            self.set_status(PluginStatus.ERROR, str(e))
            return False
    
    async def _initialize_services(self) -> None:
        """Initialize plugin services - override in subclasses"""
        pass
    
    async def _cleanup_services(self) -> None:
        """Cleanup plugin services - override in subclasses"""
        pass