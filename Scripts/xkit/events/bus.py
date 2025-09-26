"""
XKit Event Bus
Central event bus for async event-driven communication
"""
import asyncio
import logging
from typing import Dict, List, Callable, Any, Optional, Set
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from weakref import WeakSet

from .events import XKitEvent, EventPriority, EventStatus


@dataclass
class EventSubscription:
    """Represents an event subscription"""
    event_type: str
    handler: Callable[[XKitEvent], Any]
    subscriber_id: str
    priority: EventPriority = EventPriority.NORMAL
    once: bool = False  # If True, unsubscribe after first event
    condition: Optional[Callable[[XKitEvent], bool]] = None  # Optional filter
    created_at: datetime = field(default_factory=datetime.now)
    call_count: int = 0
    last_called: Optional[datetime] = None


@dataclass
class EventMetrics:
    """Event processing metrics"""
    total_events: int = 0
    processed_events: int = 0
    failed_events: int = 0
    average_processing_time: float = 0.0
    events_by_type: Dict[str, int] = field(default_factory=dict)
    events_by_priority: Dict[str, int] = field(default_factory=dict)


class EventBus:
    """Central event bus for XKit with async support and advanced features"""
    
    def __init__(self, max_queue_size: int = 10000, enable_history: bool = True):
        self.max_queue_size = max_queue_size
        self.enable_history = enable_history
        
        # Subscription management
        self.subscriptions: Dict[str, List[EventSubscription]] = defaultdict(list)
        self.wildcard_subscriptions: List[EventSubscription] = []
        self.subscriber_ids: Set[str] = set()
        
        # Event processing
        self.event_queue: asyncio.Queue = asyncio.Queue(maxsize=max_queue_size)
        self.processing_task: Optional[asyncio.Task] = None
        self.is_running = False
        
        # Event history
        self.event_history: List[XKitEvent] = []
        self.max_history_size = 1000
        
        # Metrics
        self.metrics = EventMetrics()
        
        # Middleware
        self.middleware: List[Callable[[XKitEvent], XKitEvent]] = []
        
        # Logging
        self.logger = logging.getLogger(__name__)
        
        # Cleanup tracking
        self.dead_subscriptions: WeakSet = WeakSet()
    
    async def start(self) -> None:
        """Start the event bus processing"""
        if self.is_running:
            return
        
        self.is_running = True
        self.processing_task = asyncio.create_task(self._process_events())
        self.logger.info("Event Bus started")
    
    async def stop(self) -> None:
        """Stop the event bus processing"""
        if not self.is_running:
            return
        
        self.is_running = False
        
        if self.processing_task:
            self.processing_task.cancel()
            try:
                await self.processing_task
            except asyncio.CancelledError:
                pass
        
        self.logger.info("Event Bus stopped")
    
    def subscribe(self, 
                  event_type: str, 
                  handler: Callable[[XKitEvent], Any],
                  subscriber_id: str,
                  priority: EventPriority = EventPriority.NORMAL,
                  once: bool = False,
                  condition: Optional[Callable[[XKitEvent], bool]] = None) -> str:
        """Subscribe to events of a specific type"""
        
        subscription = EventSubscription(
            event_type=event_type,
            handler=handler,
            subscriber_id=subscriber_id,
            priority=priority,
            once=once,
            condition=condition
        )
        
        if event_type == "*":
            self.wildcard_subscriptions.append(subscription)
        else:
            self.subscriptions[event_type].append(subscription)
        
        self.subscriber_ids.add(subscriber_id)
        
        # Sort by priority (higher priority first)
        if event_type != "*":
            self.subscriptions[event_type].sort(key=lambda s: s.priority.value, reverse=True)
        else:
            self.wildcard_subscriptions.sort(key=lambda s: s.priority.value, reverse=True)
        
        self.logger.debug(f"Subscribed {subscriber_id} to {event_type} events")
        return f"{subscriber_id}_{event_type}"
    
    def unsubscribe(self, event_type: str, subscriber_id: str) -> bool:
        """Unsubscribe from events of a specific type"""
        removed = False
        
        if event_type == "*":
            self.wildcard_subscriptions = [
                sub for sub in self.wildcard_subscriptions 
                if sub.subscriber_id != subscriber_id
            ]
            removed = True
        else:
            original_count = len(self.subscriptions[event_type])
            self.subscriptions[event_type] = [
                sub for sub in self.subscriptions[event_type] 
                if sub.subscriber_id != subscriber_id
            ]
            removed = len(self.subscriptions[event_type]) < original_count
        
        if removed:
            self.logger.debug(f"Unsubscribed {subscriber_id} from {event_type} events")
        
        return removed
    
    def unsubscribe_all(self, subscriber_id: str) -> int:
        """Unsubscribe a subscriber from all events"""
        removed_count = 0
        
        # Remove from wildcard subscriptions
        original_wildcard_count = len(self.wildcard_subscriptions)
        self.wildcard_subscriptions = [
            sub for sub in self.wildcard_subscriptions 
            if sub.subscriber_id != subscriber_id
        ]
        removed_count += original_wildcard_count - len(self.wildcard_subscriptions)
        
        # Remove from specific event subscriptions
        for event_type in list(self.subscriptions.keys()):
            original_count = len(self.subscriptions[event_type])
            self.subscriptions[event_type] = [
                sub for sub in self.subscriptions[event_type] 
                if sub.subscriber_id != subscriber_id
            ]
            removed_count += original_count - len(self.subscriptions[event_type])
            
            # Clean up empty subscription lists
            if not self.subscriptions[event_type]:
                del self.subscriptions[event_type]
        
        # Remove from subscriber tracking
        self.subscriber_ids.discard(subscriber_id)
        
        self.logger.debug(f"Unsubscribed {subscriber_id} from all events ({removed_count} subscriptions)")
        return removed_count
    
    async def publish(self, event: XKitEvent) -> None:
        """Publish an event to the event bus"""
        if not self.is_running:
            await self.start()
        
        try:
            # Apply middleware
            for middleware in self.middleware:
                event = middleware(event)
            
            # Add to queue
            await self.event_queue.put(event)
            
            # Update metrics
            self.metrics.total_events += 1
            event_type = event.get_event_type()
            self.metrics.events_by_type[event_type] = self.metrics.events_by_type.get(event_type, 0) + 1
            self.metrics.events_by_priority[event.priority.name] = self.metrics.events_by_priority.get(event.priority.name, 0) + 1
            
            self.logger.debug(f"Published event: {event_type} (ID: {event.event_id})")
            
        except asyncio.QueueFull:
            self.logger.error(f"Event queue full, dropping event: {event.get_event_type()}")
            self.metrics.failed_events += 1
    
    async def publish_and_wait(self, event: XKitEvent, timeout: float = 5.0) -> List[Any]:
        """Publish an event and wait for all handlers to complete"""
        if not self.is_running:
            await self.start()
        
        # Process event synchronously
        return await self._dispatch_event(event, timeout=timeout)
    
    def add_middleware(self, middleware: Callable[[XKitEvent], XKitEvent]) -> None:
        """Add middleware to process events before dispatch"""
        self.middleware.append(middleware)
    
    def remove_middleware(self, middleware: Callable[[XKitEvent], XKitEvent]) -> bool:
        """Remove middleware"""
        try:
            self.middleware.remove(middleware)
            return True
        except ValueError:
            return False
    
    async def _process_events(self) -> None:
        """Main event processing loop"""
        while self.is_running:
            try:
                # Get next event with timeout
                event = await asyncio.wait_for(self.event_queue.get(), timeout=1.0)
                
                # Process the event
                await self._dispatch_event(event)
                
                # Mark task done
                self.event_queue.task_done()
                
            except asyncio.TimeoutError:
                # Timeout is normal, continue processing
                continue
            except Exception as e:
                self.logger.error(f"Error processing event: {e}")
    
    async def _dispatch_event(self, event: XKitEvent, timeout: Optional[float] = None) -> List[Any]:
        """Dispatch an event to all matching subscribers"""
        start_time = asyncio.get_event_loop().time()
        results = []
        
        try:
            event.status = EventStatus.PROCESSING
            
            # Get matching subscriptions
            matching_subscriptions = self._get_matching_subscriptions(event)
            
            if not matching_subscriptions:
                self.logger.debug(f"No subscribers for event: {event.get_event_type()}")
                event.status = EventStatus.COMPLETED
                return results
            
            # Process subscriptions
            tasks = []
            for subscription in matching_subscriptions:
                task = asyncio.create_task(self._handle_subscription(event, subscription))
                tasks.append(task)
            
            # Wait for all handlers with timeout
            if timeout:
                done, pending = await asyncio.wait_for(
                    asyncio.gather(*tasks, return_exceptions=True),
                    timeout=timeout
                )
                results.extend(done)
            else:
                results = await asyncio.gather(*tasks, return_exceptions=True)
            
            event.status = EventStatus.COMPLETED
            
            # Add to history
            if self.enable_history:
                self._add_to_history(event)
            
        except Exception as e:
            self.logger.error(f"Error dispatching event {event.event_id}: {e}")
            event.status = EventStatus.FAILED
            self.metrics.failed_events += 1
            
        finally:
            # Always increment processed events and update timing
            self.metrics.processed_events += 1
            processing_time = asyncio.get_event_loop().time() - start_time
            self._update_processing_time(processing_time)
        
        return results
    
    def _get_matching_subscriptions(self, event: XKitEvent) -> List[EventSubscription]:
        """Get all subscriptions that match the event"""
        matching = []
        event_type = event.get_event_type()
        
        # Add specific subscriptions
        for subscription in self.subscriptions.get(event_type, []):
            if self._subscription_matches(subscription, event):
                matching.append(subscription)
        
        # Add wildcard subscriptions
        for subscription in self.wildcard_subscriptions:
            if self._subscription_matches(subscription, event):
                matching.append(subscription)
        
        return matching
    
    def _subscription_matches(self, subscription: EventSubscription, event: XKitEvent) -> bool:
        """Check if a subscription matches an event"""
        # Check condition if provided
        if subscription.condition and not subscription.condition(event):
            return False
        
        return True
    
    async def _handle_subscription(self, event: XKitEvent, subscription: EventSubscription) -> Any:
        """Handle a single subscription for an event"""
        try:
            # Update subscription stats
            subscription.call_count += 1
            subscription.last_called = datetime.now()
            
            # Call the handler
            if asyncio.iscoroutinefunction(subscription.handler):
                result = await subscription.handler(event)
            else:
                result = subscription.handler(event)
            
            # Handle once subscriptions
            if subscription.once:
                self.unsubscribe(subscription.event_type, subscription.subscriber_id)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Handler error for {subscription.subscriber_id}: {e}")
            return e
    
    def _add_to_history(self, event: XKitEvent) -> None:
        """Add event to history with size limit"""
        self.event_history.append(event)
        
        if len(self.event_history) > self.max_history_size:
            self.event_history.pop(0)
    
    def _update_processing_time(self, processing_time: float) -> None:
        """Update average processing time metrics"""
        if self.metrics.processed_events == 0:
            # Avoid division by zero - this shouldn't happen but be safe
            self.logger.warning("Attempting to update processing time with zero processed events")
            return
            
        if self.metrics.processed_events == 1:
            self.metrics.average_processing_time = processing_time
        else:
            # Calculate rolling average
            total_time = self.metrics.average_processing_time * (self.metrics.processed_events - 1)
            total_time += processing_time
            self.metrics.average_processing_time = total_time / self.metrics.processed_events
    
    def get_metrics(self) -> EventMetrics:
        """Get event bus metrics"""
        return self.metrics
    
    def get_subscriptions(self, event_type: Optional[str] = None) -> Dict[str, List[EventSubscription]]:
        """Get current subscriptions"""
        if event_type:
            return {event_type: self.subscriptions.get(event_type, [])}
        
        result = dict(self.subscriptions)
        if self.wildcard_subscriptions:
            result["*"] = self.wildcard_subscriptions
        
        return result
    
    def get_event_history(self, 
                         event_type: Optional[str] = None, 
                         since: Optional[datetime] = None,
                         limit: Optional[int] = None) -> List[XKitEvent]:
        """Get event history with optional filtering"""
        events = self.event_history
        
        if event_type:
            events = [e for e in events if e.get_event_type() == event_type]
        
        if since:
            events = [e for e in events if e.timestamp >= since]
        
        if limit:
            events = events[-limit:]
        
        return events
    
    def clear_history(self) -> None:
        """Clear event history"""
        self.event_history.clear()
        self.logger.info("Event history cleared")
    
    async def wait_for_event(self, 
                           event_type: str, 
                           timeout: Optional[float] = None,
                           condition: Optional[Callable[[XKitEvent], bool]] = None) -> Optional[XKitEvent]:
        """Wait for a specific event to occur"""
        future = asyncio.Future()
        subscription_id = f"wait_{asyncio.get_event_loop().time()}"
        
        def handler(event: XKitEvent):
            if not future.done():
                future.set_result(event)
        
        self.subscribe(event_type, handler, subscription_id, once=True, condition=condition)
        
        try:
            if timeout:
                return await asyncio.wait_for(future, timeout=timeout)
            else:
                return await future
        except asyncio.TimeoutError:
            self.unsubscribe(event_type, subscription_id)
            return None


# Global event bus instance
_event_bus: Optional[EventBus] = None


def get_event_bus() -> EventBus:
    """Get or create global event bus instance"""
    global _event_bus
    if _event_bus is None:
        _event_bus = EventBus()
    return _event_bus


async def publish_event(event: XKitEvent) -> None:
    """Convenience function to publish event to global bus"""
    bus = get_event_bus()
    await bus.publish(event)