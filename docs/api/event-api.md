# 📡 Event System API Reference

> **XKit v3.0 Event-Driven Architecture API**

This document provides comprehensive API reference for XKit's event-driven architecture, enabling loose coupling and reactive programming patterns.

## 🎯 Quick Navigation

| Section | Description |
|---------|-------------|
| [Event Bus](#event-bus) | Central event communication hub |
| [Event Types](#event-types) | Built-in and custom event definitions |
| [Publishing Events](#publishing-events) | Creating and dispatching events |
| [Subscribing to Events](#subscribing-to-events) | Event handling and filtering |
| [Event Patterns](#event-patterns) | Common event-driven patterns |
| [Performance](#performance) | Optimization and best practices |

## 🚌 Event Bus

The Event Bus is the central communication hub for all event-driven interactions in XKit.

### Core Features

- **Asynchronous Processing** - Non-blocking event handling
- **Priority Support** - Events can have different priority levels
- **Conditional Filtering** - Subscribe to events with custom conditions
- **Event History** - Optional event history tracking
- **Metrics Collection** - Performance monitoring and statistics
- **Wildcard Subscriptions** - Listen to all events or patterns

### Basic Usage

```python
from xkit.events.bus import EventBus
from xkit.events.events import XKitEvent

# Get event bus instance (usually from container)
event_bus = container.get_service("event_bus")

# Publish an event
await event_bus.publish(XKitEvent(
    event_type="custom-event",
    data={"message": "Hello World"}
))

# Subscribe to events
@event_bus.subscribe("custom-event")
async def handle_custom_event(event: XKitEvent):
    print(f"Received: {event.data['message']}")

# Subscribe with priority
@event_bus.subscribe("important-event", priority=EventPriority.HIGH)
async def handle_important_event(event: XKitEvent):
    print("High priority event handled first")

# Subscribe with conditions
@event_bus.subscribe("command-event", condition=lambda e: e.data.get("success", False))
async def handle_successful_command(event: XKitEvent):
    print("Only successful commands handled")
```

### EventBus Methods

#### `async publish(event: XKitEvent, priority: EventPriority = EventPriority.NORMAL) -> bool`

Publishes an event to all subscribers.

```python
# Simple event
await event_bus.publish(XKitEvent("user-action", {"action": "login"}))

# High priority event  
await event_bus.publish(
    XKitEvent("system-alert", {"level": "critical"}),
    priority=EventPriority.HIGH
)

# Event with metadata
event = XKitEvent("data-processed", {"records": 100})
event.add_metadata("source", "database")
event.add_metadata("timestamp", time.time())
await event_bus.publish(event)
```

#### `subscribe(event_type: str, handler: Callable, **options) -> str`

Subscribes to events of a specific type.

```python
# Basic subscription
subscription_id = event_bus.subscribe("git-operation", handle_git_event)

# Subscription with options
subscription_id = event_bus.subscribe(
    "command-executed",
    handle_command,
    priority=EventPriority.HIGH,      # Handler priority
    once=True,                        # Unsubscribe after first event
    condition=lambda e: e.success,    # Only handle successful events
    subscriber_id="my-plugin"         # Custom subscriber identifier
)

# Wildcard subscription (all events)
event_bus.subscribe("*", handle_all_events)

# Pattern subscription (events starting with "git-")
event_bus.subscribe("git-*", handle_git_events)
```

#### `unsubscribe(subscription_id: str) -> bool`

Removes a subscription.

```python
# Unsubscribe specific subscription
success = event_bus.unsubscribe(subscription_id)

# Unsubscribe all subscriptions for a subscriber
event_bus.unsubscribe_all("my-plugin")
```

#### `get_metrics() -> EventMetrics`

Returns event processing metrics.

```python
metrics = event_bus.get_metrics()
print(f"Total events: {metrics.total_events}")
print(f"Average processing time: {metrics.average_processing_time}ms")
print(f"Events by type: {metrics.events_by_type}")
```

## 🎭 Event Types

### Base Event Class

All events inherit from `XKitEvent`:

```python
from xkit.events.events import XKitEvent, EventPriority

class CustomEvent(XKitEvent):
    def __init__(self, custom_data: dict):
        super().__init__(
            event_type="custom-event",
            data=custom_data,
            priority=EventPriority.NORMAL
        )
        
        # Add custom validation
        self.validate_data()
    
    def validate_data(self):
        if "required_field" not in self.data:
            raise ValueError("required_field is missing")
```

### Built-in Event Types

#### CommandExecutedEvent

Triggered when XKit commands are executed:

```python
from xkit.events.events import CommandExecutedEvent

# Published automatically by command system
event = CommandExecutedEvent(
    command="git-status",
    args=["--branch"],
    success=True,
    output="On branch main",
    error=None,
    duration=0.25,
    metadata={"branch": "main", "files_changed": 0}
)

# Subscribe to command events
@event_bus.subscribe("CommandExecutedEvent")
async def on_command_executed(event: CommandExecutedEvent):
    if event.success:
        print(f"✅ {event.command} completed in {event.duration}s")
    else:
        print(f"❌ {event.command} failed: {event.error}")
```

#### GitOperationEvent

Git-specific operations:

```python
from xkit.events.events import GitOperationEvent

event = GitOperationEvent(
    operation="commit",
    repository_path="/path/to/repo",
    branch="main",
    success=True,
    details={
        "message": "feat: add new feature",
        "files": ["src/main.py", "tests/test_main.py"],
        "commit_hash": "abc123"
    }
)

@event_bus.subscribe("GitOperationEvent")
async def on_git_operation(event: GitOperationEvent):
    if event.operation == "commit" and event.success:
        # Notify about successful commit
        notification_service.send(
            f"📝 Committed to {event.branch}: {event.details['message']}"
        )
```

#### PluginLifecycleEvent

Plugin loading/unloading events:

```python
from xkit.events.events import PluginLifecycleEvent

event = PluginLifecycleEvent(
    plugin_name="git-enhanced",
    lifecycle_event="loaded",
    plugin_version="1.2.0",
    metadata={"commands": ["smart-commit", "ai-review"]}
)

@event_bus.subscribe("PluginLifecycleEvent")
async def on_plugin_lifecycle(event: PluginLifecycleEvent):
    if event.lifecycle_event == "loaded":
        print(f"🔌 Plugin {event.plugin_name} v{event.plugin_version} loaded")
    elif event.lifecycle_event == "unloaded":
        print(f"🔌 Plugin {event.plugin_name} unloaded")
```

#### MCPServerEvent

MCP server connection events:

```python
from xkit.events.events import MCPServerEvent

event = MCPServerEvent(
    server_name="xkit-ai",
    event_type="connected",
    server_info={
        "version": "1.0.0",
        "tools_count": 5,
        "connection_type": "internal"
    }
)

@event_bus.subscribe("MCPServerEvent")
async def on_mcp_server_event(event: MCPServerEvent):
    if event.event_type == "connected":
        tools_count = event.server_info.get("tools_count", 0)
        print(f"🔗 MCP server {event.server_name} connected with {tools_count} tools")
```

#### ErrorOccurredEvent

System error notifications:

```python
from xkit.events.events import ErrorOccurredEvent

event = ErrorOccurredEvent(
    error_type="CommandExecutionError",
    error_message="Git command failed",
    context={
        "command": "git-push",
        "working_directory": "/path/to/repo",
        "user": "john_doe"
    },
    severity="medium",
    exception=original_exception
)

@event_bus.subscribe("ErrorOccurredEvent")
async def on_error(event: ErrorOccurredEvent):
    # Log error
    logger.error(f"Error in {event.context['command']}: {event.error_message}")
    
    # Suggest fix if available
    if hasattr(ai_service, 'suggest_fix'):
        suggestion = await ai_service.suggest_fix(
            event.error_message, 
            event.context
        )
        if suggestion:
            display_service.show_info(f"💡 Suggestion: {suggestion}")
```

## 📤 Publishing Events

### Simple Event Publishing

```python
# Create and publish basic event
event = XKitEvent("user-login", {"username": "john", "timestamp": time.time()})
await event_bus.publish(event)

# One-liner publishing
await event_bus.publish(XKitEvent("system-startup", {"version": "3.0.0"}))

# Publishing with priority
await event_bus.publish(
    XKitEvent("critical-alert", {"message": "System overload"}),
    priority=EventPriority.HIGH
)
```

### Event Builder Pattern

```python
from xkit.events.builder import EventBuilder

# Fluent interface for creating events
event = (EventBuilder()
    .type("data-processed")
    .data({"records": 1000, "table": "users"})
    .priority(EventPriority.NORMAL)
    .metadata("source", "etl-pipeline")
    .metadata("batch_id", "batch_123")
    .build())

await event_bus.publish(event)
```

### Batch Publishing

```python
# Publish multiple events efficiently
events = [
    XKitEvent("record-processed", {"id": i}) 
    for i in range(100)
]

await event_bus.publish_batch(events)

# Publish with different priorities
priority_events = [
    (XKitEvent("urgent", {"id": 1}), EventPriority.HIGH),
    (XKitEvent("normal", {"id": 2}), EventPriority.NORMAL),
    (XKitEvent("low", {"id": 3}), EventPriority.LOW)
]

await event_bus.publish_batch_with_priority(priority_events)
```

## 📥 Subscribing to Events

### Decorator-Based Subscription

```python
from xkit.events.decorators import event_handler

class MyEventHandler:
    @event_handler("command-executed")
    async def handle_command(self, event: CommandExecutedEvent):
        print(f"Command executed: {event.command}")
    
    @event_handler("git-*", priority=EventPriority.HIGH)
    async def handle_git_events(self, event: GitOperationEvent):
        print(f"Git operation: {event.operation}")
    
    @event_handler("error-occurred", condition=lambda e: e.severity == "critical")
    async def handle_critical_errors(self, event: ErrorOccurredEvent):
        # Send alert for critical errors
        alert_service.send_critical_alert(event.error_message)
```

### Class-Based Subscription

```python
from xkit.events.subscriber import EventSubscriber

class GitMonitor(EventSubscriber):
    def __init__(self):
        super().__init__("git-monitor")
        self.commit_count = 0
        self.push_count = 0
    
    async def setup_subscriptions(self):
        # Subscribe to Git events
        await self.subscribe("GitOperationEvent", self.on_git_operation)
        
        # Subscribe to specific Git operations
        await self.subscribe(
            "GitOperationEvent", 
            self.on_commit,
            condition=lambda e: e.operation == "commit" and e.success
        )
        
        await self.subscribe(
            "GitOperationEvent",
            self.on_push,
            condition=lambda e: e.operation == "push"
        )
    
    async def on_git_operation(self, event: GitOperationEvent):
        print(f"📊 Git operation: {event.operation} on {event.branch}")
    
    async def on_commit(self, event: GitOperationEvent):
        self.commit_count += 1
        message = event.details.get("message", "")
        print(f"📝 Commit #{self.commit_count}: {message}")
    
    async def on_push(self, event: GitOperationEvent):
        self.push_count += 1
        print(f"🚀 Push #{self.push_count} to {event.branch}")
    
    def get_statistics(self):
        return {
            "commits": self.commit_count,
            "pushes": self.push_count
        }

# Register the subscriber
git_monitor = GitMonitor()
await git_monitor.setup_subscriptions()
```

### Conditional Subscriptions

```python
# Subscribe only to failed commands
@event_bus.subscribe("CommandExecutedEvent", condition=lambda e: not e.success)
async def handle_failed_commands(event: CommandExecutedEvent):
    error_analysis = await ai_service.analyze_error(event.error, event.command)
    display_service.show_error(f"Command failed: {error_analysis}")

# Subscribe to Git events on specific branch
@event_bus.subscribe(
    "GitOperationEvent", 
    condition=lambda e: e.branch == "main"
)
async def handle_main_branch_operations(event: GitOperationEvent):
    # Special handling for main branch
    if event.operation == "push":
        await trigger_deployment_pipeline()

# Subscribe to plugin events for specific plugins
@event_bus.subscribe(
    "PluginLifecycleEvent",
    condition=lambda e: e.plugin_name in ["git-enhanced", "ai-assistant"]
)
async def handle_core_plugin_events(event: PluginLifecycleEvent):
    print(f"Core plugin event: {event.plugin_name} {event.lifecycle_event}")
```

## 🎨 Event Patterns

### Request-Response Pattern

```python
class RequestResponseHandler:
    def __init__(self):
        self.pending_requests = {}
    
    async def send_request(self, request_data: dict) -> dict:
        request_id = str(uuid.uuid4())
        
        # Create future for response
        response_future = asyncio.Future()
        self.pending_requests[request_id] = response_future
        
        # Publish request
        await event_bus.publish(XKitEvent("data-request", {
            "request_id": request_id,
            "data": request_data
        }))
        
        # Wait for response
        try:
            response = await asyncio.wait_for(response_future, timeout=30.0)
            return response
        finally:
            self.pending_requests.pop(request_id, None)
    
    @event_bus.subscribe("data-response")
    async def handle_response(self, event: XKitEvent):
        request_id = event.data.get("request_id")
        if request_id in self.pending_requests:
            future = self.pending_requests[request_id]
            future.set_result(event.data.get("response"))

# Data processor that responds to requests
@event_bus.subscribe("data-request")
async def handle_data_request(event: XKitEvent):
    request_id = event.data["request_id"]
    request_data = event.data["data"]
    
    # Process request
    response_data = await process_data(request_data)
    
    # Send response
    await event_bus.publish(XKitEvent("data-response", {
        "request_id": request_id,
        "response": response_data
    }))
```

### Observer Pattern

```python
class FileWatcher:
    def __init__(self, path: str):
        self.path = path
        self.watchers = []
        
    async def start_watching(self):
        while True:
            # Check for file changes
            changes = await self._check_changes()
            
            if changes:
                # Notify observers via events
                await event_bus.publish(XKitEvent("file-changed", {
                    "path": self.path,
                    "changes": changes,
                    "timestamp": time.time()
                }))
            
            await asyncio.sleep(1)

# Multiple observers can subscribe
@event_bus.subscribe("file-changed")
async def auto_compile(event: XKitEvent):
    if event.data["path"].endswith(".py"):
        await run_linter(event.data["path"])

@event_bus.subscribe("file-changed")
async def auto_backup(event: XKitEvent):
    await backup_file(event.data["path"])

@event_bus.subscribe("file-changed")
async def notify_team(event: XKitEvent):
    await send_notification(f"File changed: {event.data['path']}")
```

### Saga Pattern (Distributed Transactions)

```python
class DeploymentSaga:
    def __init__(self):
        self.saga_id = str(uuid.uuid4())
        self.state = "started"
        
    async def execute_deployment(self, deployment_config: dict):
        try:
            # Step 1: Build
            await self._publish_step("build-started", deployment_config)
            build_result = await self._wait_for_completion("build-completed")
            
            if not build_result["success"]:
                await self._rollback("build-failed")
                return False
            
            # Step 2: Test
            await self._publish_step("test-started", build_result)
            test_result = await self._wait_for_completion("test-completed")
            
            if not test_result["success"]:
                await self._rollback("test-failed")
                return False
            
            # Step 3: Deploy
            await self._publish_step("deploy-started", test_result)
            deploy_result = await self._wait_for_completion("deploy-completed")
            
            if deploy_result["success"]:
                await self._publish_step("deployment-succeeded", deploy_result)
                return True
            else:
                await self._rollback("deploy-failed")
                return False
                
        except Exception as e:
            await self._rollback("saga-error", str(e))
            return False
    
    async def _publish_step(self, event_type: str, data: dict):
        await event_bus.publish(XKitEvent(event_type, {
            "saga_id": self.saga_id,
            **data
        }))
    
    async def _wait_for_completion(self, event_type: str) -> dict:
        # Implementation for waiting for specific completion event
        pass
    
    async def _rollback(self, reason: str, error: str = None):
        await event_bus.publish(XKitEvent("deployment-rollback", {
            "saga_id": self.saga_id,
            "reason": reason,
            "error": error
        }))

# Step handlers
@event_bus.subscribe("build-started")
async def handle_build(event: XKitEvent):
    # Execute build process
    success = await build_application(event.data)
    
    await event_bus.publish(XKitEvent("build-completed", {
        "saga_id": event.data["saga_id"],
        "success": success
    }))

@event_bus.subscribe("deployment-rollback")
async def handle_rollback(event: XKitEvent):
    # Implement rollback logic
    await rollback_deployment(event.data["saga_id"])
```

## ⚡ Performance Optimization

### Event Batching

```python
# Configure event bus for batching
event_bus = EventBus(
    batch_size=100,           # Process events in batches of 100
    batch_timeout=0.1,        # Process batch every 100ms
    max_queue_size=10000      # Maximum queue size
)

# Batch publishing for high-throughput scenarios
async def process_large_dataset(records: List[dict]):
    events = []
    
    for record in records:
        events.append(XKitEvent("record-processed", record))
        
        # Publish in batches of 1000
        if len(events) >= 1000:
            await event_bus.publish_batch(events)
            events = []
    
    # Publish remaining events
    if events:
        await event_bus.publish_batch(events)
```

### Memory Management

```python
# Configure event history retention
event_bus.configure_history(
    max_events=10000,         # Keep last 10,000 events
    max_age_hours=24,         # Keep events for 24 hours
    cleanup_interval=3600     # Cleanup every hour
)

# Disable event history for high-frequency events
await event_bus.publish(
    XKitEvent("high-frequency-event", data),
    save_to_history=False
)
```

### Async Processing

```python
# Process events asynchronously without blocking
@event_bus.subscribe("heavy-processing-event")
async def handle_heavy_processing(event: XKitEvent):
    # Delegate to background task
    asyncio.create_task(process_heavy_task(event.data))

# Use thread pool for CPU-intensive tasks
import concurrent.futures

@event_bus.subscribe("cpu-intensive-event")
async def handle_cpu_intensive(event: XKitEvent):
    loop = asyncio.get_event_loop()
    executor = concurrent.futures.ThreadPoolExecutor()
    
    result = await loop.run_in_executor(
        executor,
        cpu_intensive_function,
        event.data
    )
    
    # Publish result
    await event_bus.publish(XKitEvent("processing-completed", {"result": result}))
```

## 📊 Monitoring and Debugging

### Event Metrics

```python
# Get detailed metrics
metrics = event_bus.get_metrics()

print(f"📊 Event System Metrics:")
print(f"  Total Events: {metrics.total_events}")
print(f"  Processed: {metrics.processed_events}")
print(f"  Failed: {metrics.failed_events}")
print(f"  Avg Processing Time: {metrics.average_processing_time:.2f}ms")

# Events by type
print(f"  Events by Type:")
for event_type, count in metrics.events_by_type.items():
    print(f"    {event_type}: {count}")

# Events by priority
print(f"  Events by Priority:")
for priority, count in metrics.events_by_priority.items():
    print(f"    {priority}: {count}")
```

### Event Tracing

```python
# Enable event tracing
event_bus.enable_tracing(
    trace_all=True,                    # Trace all events
    trace_slow_events=True,            # Highlight slow events
    slow_threshold_ms=100,             # Consider >100ms as slow
    max_trace_events=1000              # Keep last 1000 traces
)

# Get event traces
traces = event_bus.get_event_traces()
for trace in traces[-10:]:  # Last 10 events
    print(f"Event: {trace.event_type}")
    print(f"  Processing Time: {trace.processing_time_ms}ms")
    print(f"  Handlers: {trace.handler_count}")
    print(f"  Success: {trace.success}")
```

### Debug Mode

```python
# Enable debug mode for verbose logging
event_bus.enable_debug_mode(
    log_all_events=True,               # Log all published events
    log_subscription_changes=True,     # Log subscription add/remove
    log_handler_execution=True,        # Log handler execution
    log_performance=True               # Log performance metrics
)

# Custom event debugging
@event_bus.subscribe("*")  # Subscribe to all events
async def debug_event_handler(event: XKitEvent):
    if event.event_type != "debug-event":  # Avoid recursion
        print(f"🔍 DEBUG: {event.event_type} - {event.data}")
        
        # Publish debug event
        await event_bus.publish(XKitEvent("debug-event", {
            "original_type": event.event_type,
            "timestamp": time.time(),
            "data_size": len(str(event.data))
        }))
```

## 🔗 Related Documentation

- **[Core API](core-api.md)** - XKit Core Python API
- **[Plugin API](plugin-api.md)** - Plugin development guide
- **[MCP Protocol](mcp-protocol.md)** - MCP integration guide
- **[CLI Commands](cli-commands.md)** - Command-line interface reference

---

**Last Updated**: September 2025 | **Version**: v3.0.0  
**💙 Made with love by the XKit Community**