"""
Event Service Port
Interface for event bus operations
"""
from abc import ABC, abstractmethod
from typing import Callable, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

# Import types locally to avoid circular imports
class EventPriority(Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


class IEventService(ABC):
    """Port for event operations"""
    
    @abstractmethod
    async def publish(self, event: Any) -> None:  # XKitEvent
        """Publish an event"""
        pass
    
    @abstractmethod
    def subscribe(self, event_type: str, 
                  handler: Callable[[Any], Any],  # Callable[[XKitEvent], Any]
                  subscriber_id: str,
                  priority: EventPriority = EventPriority.NORMAL) -> str:
        """Subscribe to events"""
        pass
    
    @abstractmethod
    def unsubscribe(self, event_type: str, subscriber_id: str) -> bool:
        """Unsubscribe from events"""
        pass
    
    @abstractmethod
    async def wait_for_event(self, event_type: str, 
                           timeout: Optional[float] = None) -> Optional[Any]:  # Optional[XKitEvent]
        """Wait for a specific event"""
        pass