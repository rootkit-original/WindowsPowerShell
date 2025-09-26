"""
XKit Application
Main application class with dependency injection
"""
import asyncio
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from .container import XKitContainer
from .ports import (
    ICommandService, IGitService, IAIService, IEventService,
    IPluginService, IMCPService, IDisplayService, IConfigService
)
from ..events import (
    SystemStartedEvent, SystemShutdownEvent, publish_event
)


@dataclass
class ApplicationConfig:
    """Application configuration"""
    debug: bool = False
    log_level: str = "INFO"
    plugin_directories: List[str] = None
    mcp_config_path: Optional[str] = None
    enable_hot_reload: bool = True
    enable_events: bool = True
    
    def __post_init__(self):
        if self.plugin_directories is None:
            self.plugin_directories = []


class XKitApplication:
    """Main XKit application with hexagonal architecture"""
    
    def __init__(self, config: ApplicationConfig, container: XKitContainer):
        self.config = config
        self.container = container
        self.logger = logging.getLogger(__name__)
        self.is_running = False
        self._startup_tasks = []
        self._shutdown_tasks = []
        
        # Configure logging
        logging.basicConfig(
            level=getattr(logging, config.log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    async def start(self) -> None:
        """Start the XKit application"""
        if self.is_running:
            return
        
        try:
            self.logger.info("Starting XKit application...")
            
            # Initialize container
            await self.container.initialize()
            
            # Start core services
            await self._start_core_services()
            
            # Load plugins
            await self._load_plugins()
            
            # Start MCP client
            await self._start_mcp_client()
            
            # Run startup tasks
            await self._run_startup_tasks()
            
            self.is_running = True
            
            # Publish system started event
            if self.config.enable_events:
                event = SystemStartedEvent(
                    source="xkit.application",
                    metadata={
                        "version": "3.0.0",
                        "architecture": "hybrid-mcp",
                        "components": self._get_active_components()
                    }
                )
                await publish_event(event)
            
            self.logger.info("XKit application started successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to start XKit application: {e}")
            await self.stop()
            raise
    
    async def stop(self) -> None:
        """Stop the XKit application"""
        if not self.is_running:
            return
        
        try:
            self.logger.info("Stopping XKit application...")
            
            # Publish system shutdown event
            if self.config.enable_events:
                event = SystemShutdownEvent(
                    source="xkit.application",
                    metadata={"reason": "normal"}
                )
                await publish_event(event)
            
            # Run shutdown tasks
            await self._run_shutdown_tasks()
            
            # Stop services in reverse order
            await self._stop_mcp_client()
            await self._unload_plugins()
            await self._stop_core_services()
            
            # Cleanup container
            await self.container.cleanup()
            
            self.is_running = False
            self.logger.info("XKit application stopped")
            
        except Exception as e:
            self.logger.error(f"Error during application shutdown: {e}")
    
    async def execute_command(self, command: str, args: List[str] = None) -> Any:
        """Execute a command through the application"""
        if not self.is_running:
            raise RuntimeError("Application is not running")
        
        command_service = self.container.get_service(ICommandService)
        return await command_service.execute_command(command, args or [])
    
    def get_service(self, service_type) -> Any:
        """Get a service from the container"""
        return self.container.get_service(service_type)
    
    def register_startup_task(self, task_func) -> None:
        """Register a task to run during startup"""
        self._startup_tasks.append(task_func)
    
    def register_shutdown_task(self, task_func) -> None:
        """Register a task to run during shutdown"""
        self._shutdown_tasks.append(task_func)
    
    async def _start_core_services(self) -> None:
        """Start core services"""
        self.logger.debug("Starting core services...")
        
        # Start event service first
        if self.config.enable_events:
            event_service = self.container.get_service(IEventService)
            if hasattr(event_service, 'start'):
                await event_service.start()
        
        # Initialize display service
        display_service = self.container.get_service(IDisplayService)
        if hasattr(display_service, 'initialize'):
            await display_service.initialize()
        
        # Load configuration
        config_service = self.container.get_service(IConfigService)
        if hasattr(config_service, 'reload_config'):
            config_service.reload_config()
        
        self.logger.debug("Core services started")
    
    async def _stop_core_services(self) -> None:
        """Stop core services"""
        self.logger.debug("Stopping core services...")
        
        # Stop event service last
        if self.config.enable_events:
            event_service = self.container.get_service(IEventService)
            if hasattr(event_service, 'stop'):
                await event_service.stop()
    
    async def _load_plugins(self) -> None:
        """Load plugins"""
        if not self.config.plugin_directories:
            return
        
        self.logger.debug("Loading plugins...")
        plugin_service = self.container.get_service(IPluginService)
        
        for plugin_dir in self.config.plugin_directories:
            try:
                # This would be implemented by the plugin service
                if hasattr(plugin_service, 'load_plugins_from_directory'):
                    await plugin_service.load_plugins_from_directory(plugin_dir)
            except Exception as e:
                self.logger.error(f"Failed to load plugins from {plugin_dir}: {e}")
        
        # Enable hot reload if configured
        if self.config.enable_hot_reload:
            if hasattr(plugin_service, 'async_enable_hot_reload'):
                await plugin_service.async_enable_hot_reload(self.config.plugin_directories)
            elif hasattr(plugin_service, 'enable_hot_reload'):
                plugin_service.enable_hot_reload(True)
    
    async def _unload_plugins(self) -> None:
        """Unload all plugins"""
        self.logger.debug("Unloading plugins...")
        plugin_service = self.container.get_service(IPluginService)
        
        plugins = plugin_service.list_plugins()
        for plugin in plugins:
            try:
                await plugin_service.unload_plugin(plugin.name)
            except Exception as e:
                self.logger.error(f"Failed to unload plugin {plugin.name}: {e}")
    
    async def _start_mcp_client(self) -> None:
        """Start MCP client"""
        self.logger.debug("Starting MCP client...")
        mcp_service = self.container.get_service(IMCPService)
        await mcp_service.start_client()
    
    async def _stop_mcp_client(self) -> None:
        """Stop MCP client"""
        self.logger.debug("Stopping MCP client...")
        mcp_service = self.container.get_service(IMCPService)
        await mcp_service.stop_client()
    
    async def _run_startup_tasks(self) -> None:
        """Run registered startup tasks"""
        for task in self._startup_tasks:
            try:
                if asyncio.iscoroutinefunction(task):
                    await task()
                else:
                    task()
            except Exception as e:
                self.logger.error(f"Startup task failed: {e}")
    
    async def _run_shutdown_tasks(self) -> None:
        """Run registered shutdown tasks"""
        for task in self._shutdown_tasks:
            try:
                if asyncio.iscoroutinefunction(task):
                    await task()
                else:
                    task()
            except Exception as e:
                self.logger.error(f"Shutdown task failed: {e}")
    
    def _get_active_components(self) -> List[str]:
        """Get list of active components"""
        components = ["core", "events"]
        
        if self.config.plugin_directories:
            components.append("plugins")
        
        if self.config.mcp_config_path:
            components.append("mcp")
        
        return components
    
    def get_status(self) -> Dict[str, Any]:
        """Get application status"""
        return {
            "running": self.is_running,
            "version": "3.0.0",
            "architecture": "hybrid-mcp",
            "components": self._get_active_components(),
            "debug": self.config.debug,
            "log_level": self.config.log_level,
            "hot_reload": self.config.enable_hot_reload,
            "events": self.config.enable_events
        }