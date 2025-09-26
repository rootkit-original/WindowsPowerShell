"""
XKit Event Handlers
Base classes and utilities for event handlers
"""
import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass

from ..events import XKitEvent, EventPriority
from ..bus import EventBus


class EventHandler(ABC):
    """Abstract base class for event handlers"""
    
    def __init__(self, handler_id: str, priority: EventPriority = EventPriority.NORMAL):
        self.handler_id = handler_id
        self.priority = priority
        self.logger = logging.getLogger(f"{__name__}.{handler_id}")
        self.subscriptions: List[str] = []
    
    @abstractmethod
    async def handle_event(self, event: XKitEvent) -> Any:
        """Handle an event - implement in subclasses"""
        pass
    
    @abstractmethod
    def get_supported_events(self) -> List[str]:
        """Return list of event types this handler supports"""
        pass
    
    async def initialize(self, event_bus: EventBus) -> None:
        """Initialize handler and subscribe to events"""
        supported_events = self.get_supported_events()
        
        for event_type in supported_events:
            subscription_id = event_bus.subscribe(
                event_type=event_type,
                handler=self.handle_event,
                subscriber_id=self.handler_id,
                priority=self.priority
            )
            self.subscriptions.append(subscription_id)
        
        self.logger.info(f"Handler {self.handler_id} initialized with {len(supported_events)} subscriptions")
    
    async def shutdown(self, event_bus: EventBus) -> None:
        """Shutdown handler and unsubscribe from events"""
        event_bus.unsubscribe_all(self.handler_id)
        self.subscriptions.clear()
        self.logger.info(f"Handler {self.handler_id} shutdown complete")


class SystemEventHandler(EventHandler):
    """Handler for core system events"""
    
    def __init__(self):
        super().__init__("system_handler", EventPriority.HIGH)
    
    def get_supported_events(self) -> List[str]:
        return [
            "system.started",
            "system.shutdown", 
            "system.error"
        ]
    
    async def handle_event(self, event: XKitEvent) -> Any:
        event_type = event.get_event_type()
        
        if event_type == "system.started":
            return await self._handle_system_started(event)
        elif event_type == "system.shutdown":
            return await self._handle_system_shutdown(event)
        elif event_type == "system.error":
            return await self._handle_system_error(event)
    
    async def _handle_system_started(self, event: XKitEvent) -> None:
        """Handle system started event"""
        self.logger.info(f"XKit system started: {event.metadata.get('version', 'unknown')}")
        # Could notify external systems, log to file, etc.
    
    async def _handle_system_shutdown(self, event: XKitEvent) -> None:
        """Handle system shutdown event"""
        reason = event.metadata.get('reason', 'unknown')
        self.logger.info(f"XKit system shutting down: {reason}")
        # Could cleanup resources, save state, etc.
    
    async def _handle_system_error(self, event: XKitEvent) -> None:
        """Handle system error event"""
        error_msg = event.metadata.get('error_message', 'unknown error')
        component = event.metadata.get('component', 'unknown')
        self.logger.error(f"System error in {component}: {error_msg}")
        # Could trigger recovery mechanisms, send alerts, etc.


class PluginEventHandler(EventHandler):
    """Handler for plugin lifecycle events"""
    
    def __init__(self):
        super().__init__("plugin_handler", EventPriority.NORMAL)
        self.plugin_stats: Dict[str, Dict[str, Any]] = {}
    
    def get_supported_events(self) -> List[str]:
        return [
            "plugin.loaded",
            "plugin.unloaded",
            "plugin.error"
        ]
    
    async def handle_event(self, event: XKitEvent) -> Any:
        event_type = event.get_event_type()
        
        if event_type == "plugin.loaded":
            return await self._handle_plugin_loaded(event)
        elif event_type == "plugin.unloaded":
            return await self._handle_plugin_unloaded(event)
        elif event_type == "plugin.error":
            return await self._handle_plugin_error(event)
    
    async def _handle_plugin_loaded(self, event: XKitEvent) -> None:
        """Handle plugin loaded event"""
        plugin_name = event.metadata.get('plugin_name', 'unknown')
        plugin_version = event.metadata.get('plugin_version', '1.0.0')
        load_time = event.metadata.get('load_time', 0.0)
        
        self.plugin_stats[plugin_name] = {
            'version': plugin_version,
            'loaded_at': event.timestamp,
            'load_time': load_time,
            'error_count': 0
        }
        
        self.logger.info(f"Plugin loaded: {plugin_name} v{plugin_version} ({load_time:.3f}s)")
    
    async def _handle_plugin_unloaded(self, event: XKitEvent) -> None:
        """Handle plugin unloaded event"""
        plugin_name = event.metadata.get('plugin_name', 'unknown')
        reason = event.metadata.get('reason', 'manual')
        
        if plugin_name in self.plugin_stats:
            del self.plugin_stats[plugin_name]
        
        self.logger.info(f"Plugin unloaded: {plugin_name} (reason: {reason})")
    
    async def _handle_plugin_error(self, event: XKitEvent) -> None:
        """Handle plugin error event"""
        plugin_name = event.metadata.get('plugin_name', 'unknown')
        error_msg = event.metadata.get('error_message', 'unknown error')
        
        if plugin_name in self.plugin_stats:
            self.plugin_stats[plugin_name]['error_count'] += 1
        
        self.logger.error(f"Plugin error in {plugin_name}: {error_msg}")
    
    def get_plugin_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get current plugin statistics"""
        return self.plugin_stats.copy()


class MCPEventHandler(EventHandler):
    """Handler for MCP-related events"""
    
    def __init__(self):
        super().__init__("mcp_handler", EventPriority.NORMAL)
        self.server_connections: Dict[str, Dict[str, Any]] = {}
    
    def get_supported_events(self) -> List[str]:
        return [
            "mcp.server.connected",
            "mcp.server.disconnected", 
            "mcp.tool.called"
        ]
    
    async def handle_event(self, event: XKitEvent) -> Any:
        event_type = event.get_event_type()
        
        if event_type == "mcp.server.connected":
            return await self._handle_server_connected(event)
        elif event_type == "mcp.server.disconnected":
            return await self._handle_server_disconnected(event)
        elif event_type == "mcp.tool.called":
            return await self._handle_tool_called(event)
    
    async def _handle_server_connected(self, event: XKitEvent) -> None:
        """Handle MCP server connected event"""
        server_name = event.metadata.get('server_name', 'unknown')
        server_type = event.metadata.get('server_type', 'unknown')
        connection_time = event.metadata.get('connection_time', 0.0)
        
        self.server_connections[server_name] = {
            'type': server_type,
            'connected_at': event.timestamp,
            'connection_time': connection_time,
            'tool_calls': 0
        }
        
        self.logger.info(f"MCP server connected: {server_name} ({server_type}) in {connection_time:.3f}s")
    
    async def _handle_server_disconnected(self, event: XKitEvent) -> None:
        """Handle MCP server disconnected event"""
        server_name = event.metadata.get('server_name', 'unknown')
        reason = event.metadata.get('reason', 'unknown')
        was_error = event.metadata.get('was_error', False)
        
        if server_name in self.server_connections:
            del self.server_connections[server_name]
        
        level = logging.ERROR if was_error else logging.INFO
        self.logger.log(level, f"MCP server disconnected: {server_name} (reason: {reason})")
    
    async def _handle_tool_called(self, event: XKitEvent) -> None:
        """Handle MCP tool called event"""
        server_name = event.metadata.get('server_name', 'unknown')
        tool_name = event.metadata.get('tool_name', 'unknown')
        success = event.metadata.get('success', True)
        execution_time = event.metadata.get('execution_time', 0.0)
        
        if server_name in self.server_connections:
            self.server_connections[server_name]['tool_calls'] += 1
        
        level = logging.INFO if success else logging.WARNING
        self.logger.log(level, f"MCP tool called: {server_name}.{tool_name} ({execution_time:.3f}s)")
    
    def get_server_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get current MCP server statistics"""
        return self.server_connections.copy()


# Registry of available handlers
DEFAULT_HANDLERS = [
    SystemEventHandler,
    PluginEventHandler,
    MCPEventHandler
]


async def initialize_default_handlers(event_bus: EventBus) -> List[EventHandler]:
    """Initialize all default event handlers"""
    handlers = []
    
    for handler_class in DEFAULT_HANDLERS:
        try:
            handler = handler_class()
            await handler.initialize(event_bus)
            handlers.append(handler)
        except Exception as e:
            logging.error(f"Failed to initialize handler {handler_class.__name__}: {e}")
    
    return handlers


async def shutdown_handlers(handlers: List[EventHandler], event_bus: EventBus) -> None:
    """Shutdown all event handlers"""
    for handler in handlers:
        try:
            await handler.shutdown(event_bus)
        except Exception as e:
            logging.error(f"Error shutting down handler {handler.handler_id}: {e}")