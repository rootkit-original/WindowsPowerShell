"""
XKit Event Definitions
Defines all event types used throughout the XKit system
"""
import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional, List
from enum import Enum


class EventPriority(Enum):
    """Event priority levels"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


class EventStatus(Enum):
    """Event processing status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class XKitEvent(ABC):
    """Base class for all XKit events"""
    event_id: str = field(default_factory=lambda: f"evt_{asyncio.get_event_loop().time()}")
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = "unknown"
    priority: EventPriority = EventPriority.NORMAL
    status: EventStatus = EventStatus.PENDING
    metadata: Dict[str, Any] = field(default_factory=dict)
    correlation_id: Optional[str] = None  # For tracking related events
    
    @abstractmethod
    def get_event_type(self) -> str:
        """Return the event type identifier"""
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary"""
        return {
            "event_id": self.event_id,
            "event_type": self.get_event_type(),
            "timestamp": self.timestamp.isoformat(),
            "source": self.source,
            "priority": self.priority.value,
            "status": self.status.value,
            "metadata": self.metadata,
            "correlation_id": self.correlation_id
        }


# Command Events
@dataclass
class CommandExecutedEvent(XKitEvent):
    """Event fired when a command is executed"""
    command: str = ""
    args: List[str] = field(default_factory=list)
    result: Any = None
    success: bool = True
    error_message: Optional[str] = None
    execution_time: float = 0.0
    
    def get_event_type(self) -> str:
        return "command.executed"


@dataclass 
class CommandFailedEvent(XKitEvent):
    """Event fired when a command fails"""
    command: str = ""
    args: List[str] = field(default_factory=list)
    error_message: str = "Unknown error"
    error_type: str = "unknown"
    stack_trace: Optional[str] = None
    
    def get_event_type(self) -> str:
        return "command.failed"


# System Events
@dataclass
class SystemStartedEvent(XKitEvent):
    """Event fired when XKit system starts"""
    version: str = "3.0.0"
    architecture: str = "hybrid-mcp"
    components: List[str] = field(default_factory=list)
    
    def get_event_type(self) -> str:
        return "system.started"


@dataclass
class SystemShutdownEvent(XKitEvent):
    """Event fired when XKit system shuts down"""
    reason: str = "normal"
    uptime_seconds: float = 0.0
    
    def get_event_type(self) -> str:
        return "system.shutdown"


@dataclass
class SystemErrorEvent(XKitEvent):
    """Event fired when system errors occur"""
    error_message: str = "Unknown system error"
    error_type: str = "system"
    component: str = "unknown"
    stack_trace: Optional[str] = None
    recoverable: bool = True
    
    def get_event_type(self) -> str:
        return "system.error"


# Plugin Events
@dataclass
class PluginLoadedEvent(XKitEvent):
    """Event fired when a plugin is loaded"""
    plugin_name: str = "unknown"
    plugin_version: str = "1.0.0"
    load_time: float = 0.0
    
    def get_event_type(self) -> str:
        return "plugin.loaded"


@dataclass
class PluginUnloadedEvent(XKitEvent):
    """Event fired when a plugin is unloaded"""
    plugin_name: str = "unknown"
    reason: str = "manual"
    
    def get_event_type(self) -> str:
        return "plugin.unloaded"


@dataclass
class PluginErrorEvent(XKitEvent):
    """Event fired when a plugin error occurs"""
    plugin_name: str = "unknown"
    error_message: str = "Plugin error"
    error_type: str = "unknown"
    
    def get_event_type(self) -> str:
        return "plugin.error"


# MCP Events
@dataclass
class MCPServerConnectedEvent(XKitEvent):
    """Event fired when MCP server connects"""
    server_name: str = "unknown"
    server_type: str = "internal"
    connection_time: float = 0.0
    
    def get_event_type(self) -> str:
        return "mcp.server.connected"


@dataclass
class MCPServerDisconnectedEvent(XKitEvent):
    """Event fired when MCP server disconnects"""
    server_name: str = "unknown"
    reason: str = "unknown"
    was_error: bool = False
    
    def get_event_type(self) -> str:
        return "mcp.server.disconnected"


@dataclass
class MCPToolCalledEvent(XKitEvent):
    """Event fired when an MCP tool is called"""
    server_name: str = "unknown"
    tool_name: str = "unknown"
    arguments: Dict[str, Any] = field(default_factory=dict)
    result: Any = None
    success: bool = True
    execution_time: float = 0.0
    
    def get_event_type(self) -> str:
        return "mcp.tool.called"


# Git Events
@dataclass
class GitOperationEvent(XKitEvent):
    """Event fired when git operations occur"""
    operation: str = "unknown"  # commit, push, branch, etc.
    repository_path: str = "."
    branch: Optional[str] = None
    success: bool = True
    details: Dict[str, Any] = field(default_factory=dict)
    
    def get_event_type(self) -> str:
        return "git.operation"


@dataclass
class GitBranchCreatedEvent(XKitEvent):
    """Event fired when a git branch is created"""
    branch_name: str = "unknown"
    base_branch: str = "main"
    repository_path: str = "."
    branch_type: str = "feature"
    
    def get_event_type(self) -> str:
        return "git.branch.created"


# AI Events
@dataclass
class AIAnalysisRequestEvent(XKitEvent):
    """Event fired when AI analysis is requested"""
    analysis_type: str = "general"
    input_data: str = ""
    context: Dict[str, Any] = field(default_factory=dict)
    
    def get_event_type(self) -> str:
        return "ai.analysis.request"


@dataclass
class AIAnalysisCompletedEvent(XKitEvent):
    """Event fired when AI analysis is completed"""
    analysis_type: str = "general"
    result: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0
    processing_time: float = 0.0
    
    def get_event_type(self) -> str:
        return "ai.analysis.completed"


# Error Events
@dataclass
class ErrorDetectedEvent(XKitEvent):
    """Event fired when an error is detected"""
    error_message: str = "Unknown error"
    error_type: str = "general"
    component: str = "unknown"
    context: Dict[str, Any] = field(default_factory=dict)
    severity: str = "medium"
    auto_fixable: bool = False
    
    def get_event_type(self) -> str:
        return "error.detected"


@dataclass
class ErrorResolvedEvent(XKitEvent):
    """Event fired when an error is resolved"""
    original_error_id: str = "unknown"
    resolution_method: str = "manual"
    resolution_details: Dict[str, Any] = field(default_factory=dict)
    auto_resolved: bool = False
    
    def get_event_type(self) -> str:
        return "error.resolved"


# Configuration Events
@dataclass
class ConfigurationChangedEvent(XKitEvent):
    """Event fired when configuration changes"""
    config_key: str = "unknown"
    old_value: Any = None
    new_value: Any = None
    component: str = "core"
    
    def get_event_type(self) -> str:
        return "config.changed"


# Custom Event Base
@dataclass
class CustomEvent(XKitEvent):
    """Base class for custom events"""
    event_type: str = "custom"
    data: Dict[str, Any] = field(default_factory=dict)
    
    def get_event_type(self) -> str:
        return self.event_type


# Event Registry
EVENT_TYPES = {
    "command.executed": CommandExecutedEvent,
    "command.failed": CommandFailedEvent,
    "system.started": SystemStartedEvent,
    "system.shutdown": SystemShutdownEvent,
    "system.error": SystemErrorEvent,
    "plugin.loaded": PluginLoadedEvent,
    "plugin.unloaded": PluginUnloadedEvent,
    "plugin.error": PluginErrorEvent,
    "mcp.server.connected": MCPServerConnectedEvent,
    "mcp.server.disconnected": MCPServerDisconnectedEvent,
    "mcp.tool.called": MCPToolCalledEvent,
    "git.operation": GitOperationEvent,
    "git.branch.created": GitBranchCreatedEvent,
    "ai.analysis.request": AIAnalysisRequestEvent,
    "ai.analysis.completed": AIAnalysisCompletedEvent,
    "error.detected": ErrorDetectedEvent,
    "error.resolved": ErrorResolvedEvent,
    "config.changed": ConfigurationChangedEvent
}


def create_event_from_type(event_type: str, **kwargs) -> Optional[XKitEvent]:
    """Create an event instance from event type string"""
    if event_type in EVENT_TYPES:
        return EVENT_TYPES[event_type](**kwargs)
    else:
        # Return custom event
        return CustomEvent(event_type=event_type, data=kwargs)