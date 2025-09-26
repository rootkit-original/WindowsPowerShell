"""
Event Service Adapter
Adapter that implements IEventService using the event bus
"""
import asyncio
import logging
from typing import Callable, List, Optional, Any

from ...core.ports.event_port import IEventService, EventPriority
from ...events import get_event_bus, XKitEvent


class EventServiceAdapter(IEventService):
    """Event service adapter using XKit event bus"""
    
    def __init__(self):
        self.event_bus = get_event_bus()
        self.logger = logging.getLogger(__name__)
        self._subscriber_prefix = "event_adapter"
    
    async def initialize(self) -> None:
        """Initialize the event service"""
        await self.event_bus.start()
        self.logger.info("Event service adapter initialized")
    
    async def cleanup(self) -> None:
        """Cleanup the event service"""
        await self.event_bus.stop()
        self.logger.info("Event service adapter cleaned up")
    
    async def publish(self, event: Any) -> None:  # XKitEvent
        """Publish an event"""
        await self.event_bus.publish(event)
    
    def subscribe(self, event_type: str, 
                  handler: Callable[[Any], Any],  # Callable[[XKitEvent], Any]
                  subscriber_id: str,
                  priority: EventPriority = EventPriority.NORMAL) -> str:
        """Subscribe to events"""
        # Convert our EventPriority enum to the event bus EventPriority
        from ...events.events import EventPriority as BusEventPriority
        
        bus_priority = {
            EventPriority.LOW: BusEventPriority.LOW,
            EventPriority.NORMAL: BusEventPriority.NORMAL,
            EventPriority.HIGH: BusEventPriority.HIGH,
            EventPriority.CRITICAL: BusEventPriority.CRITICAL
        }[priority]
        
        return self.event_bus.subscribe(
            event_type=event_type,
            handler=handler,
            subscriber_id=f"{self._subscriber_prefix}_{subscriber_id}",
            priority=bus_priority
        )
    
    def unsubscribe(self, event_type: str, subscriber_id: str) -> bool:
        """Unsubscribe from events"""
        return self.event_bus.unsubscribe(event_type, f"{self._subscriber_prefix}_{subscriber_id}")
    
    async def wait_for_event(self, event_type: str, 
                           timeout: Optional[float] = None) -> Optional[Any]:  # Optional[XKitEvent]
        """Wait for a specific event"""
        return await self.event_bus.wait_for_event(event_type, timeout)
    
    def get_metrics(self):
        """Get event bus metrics"""
        return self.event_bus.get_metrics()
    
    def get_subscriptions(self, event_type: Optional[str] = None):
        """Get current subscriptions"""
        return self.event_bus.get_subscriptions(event_type)