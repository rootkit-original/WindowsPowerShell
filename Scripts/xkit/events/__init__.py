"""
XKit Event System

Central event-driven architecture for XKit with async support,
MCP integration, and plugin communication.
"""

from .events import (
    XKitEvent, EventPriority, EventStatus,
    CommandExecutedEvent, CommandFailedEvent,
    SystemStartedEvent, SystemShutdownEvent, SystemErrorEvent,
    PluginLoadedEvent, PluginUnloadedEvent, PluginErrorEvent,
    MCPServerConnectedEvent, MCPServerDisconnectedEvent, MCPToolCalledEvent,
    GitOperationEvent, GitBranchCreatedEvent,
    AIAnalysisRequestEvent, AIAnalysisCompletedEvent,
    ErrorDetectedEvent, ErrorResolvedEvent,
    ConfigurationChangedEvent, CustomEvent,
    EVENT_TYPES, create_event_from_type
)

from .bus import EventBus, EventSubscription, EventMetrics, get_event_bus, publish_event

from .handlers import (
    EventHandler, SystemEventHandler, PluginEventHandler, MCPEventHandler,
    DEFAULT_HANDLERS, initialize_default_handlers, shutdown_handlers
)

__all__ = [
    # Core classes
    'XKitEvent', 'EventPriority', 'EventStatus', 'EventBus', 'EventHandler',
    
    # Event types
    'CommandExecutedEvent', 'CommandFailedEvent',
    'SystemStartedEvent', 'SystemShutdownEvent', 'SystemErrorEvent',
    'PluginLoadedEvent', 'PluginUnloadedEvent', 'PluginErrorEvent',
    'MCPServerConnectedEvent', 'MCPServerDisconnectedEvent', 'MCPToolCalledEvent',
    'GitOperationEvent', 'GitBranchCreatedEvent',
    'AIAnalysisRequestEvent', 'AIAnalysisCompletedEvent',
    'ErrorDetectedEvent', 'ErrorResolvedEvent',
    'ConfigurationChangedEvent', 'CustomEvent',
    
    # Utilities
    'EventSubscription', 'EventMetrics',
    'EVENT_TYPES', 'create_event_from_type',
    'get_event_bus', 'publish_event',
    
    # Handlers
    'SystemEventHandler', 'PluginEventHandler', 'MCPEventHandler',
    'DEFAULT_HANDLERS', 'initialize_default_handlers', 'shutdown_handlers'
]

# Version info
__version__ = "1.0.0"