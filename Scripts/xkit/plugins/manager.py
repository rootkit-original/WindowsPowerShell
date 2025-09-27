"""
XKit Plugin Manager
Manages plugin lifecycle, dependencies, and hot-reloading
"""
import asyncio
import logging
import importlib
import sys
from typing import Dict, Any, List, Optional, Type, Set
from pathlib import Path
from collections import defaultdict

from .base import XKitPlugin, PluginMetadata, PluginStatus, PluginEvent
from .loader import PluginLoader
from .core import core_plugin_registry


class PluginDependencyError(Exception):
    """Raised when plugin dependencies cannot be resolved"""
    pass


class PluginManager:
    """Manages XKit plugins with hot-reload and dependency resolution"""
    
    def __init__(self, plugin_directories: Optional[List[Path]] = None):
        self.plugins: Dict[str, XKitPlugin] = {}
        self.plugin_directories = plugin_directories or []
        self.loader = PluginLoader()
        self.logger = logging.getLogger(__name__)
        
        # Event service (will be set externally)
        self.event_service = None
        
        # Dependency tracking
        self.dependency_graph: Dict[str, Set[str]] = defaultdict(set)
        self.reverse_dependencies: Dict[str, Set[str]] = defaultdict(set)
        
        # Service registry
        self.services: Dict[str, Any] = {}
        self.service_providers: Dict[str, str] = {}  # service_name -> plugin_name
        
        # Command registry
        self.commands: Dict[str, tuple[str, callable]] = {}  # command -> (plugin_name, handler)
        
        # Hot reload tracking
        self.file_watchers: Dict[str, Any] = {}
        self.hot_reload_enabled = True
    
    @property
    def loaded_plugins(self) -> Dict[str, XKitPlugin]:
        """Alias for plugins for backward compatibility"""
        return self.plugins
    
    async def initialize(self) -> None:
        """Initialize the plugin manager"""
        self.logger.info("Initializing Plugin Manager")
        
        # Add default plugin directories
        current_dir = Path(__file__).parent
        default_dirs = [
            current_dir / "core",
            current_dir.parent.parent.parent / "oh-my-xkit" / "plugins"
        ]
        
        for directory in default_dirs:
            if directory.exists() and directory not in self.plugin_directories:
                self.plugin_directories.append(directory)
        
        # Load core services first
        await self._initialize_core_services()
        
        # Load core plugins
        await self._load_core_plugins()
        
        self.logger.info(f"Plugin Manager initialized with {len(self.plugin_directories)} directories")
    
    async def _initialize_core_services(self) -> None:
        """Initialize core services that plugins can use"""
        self.services["logger"] = self.logger
        self.services["event_bus"] = None  # Will be set by event system
        self.services["mcp_client"] = None  # Will be set by MCP system
    
    async def _load_core_plugins(self) -> None:
        """Load core plugins automatically"""
        try:
            await core_plugin_registry.load_all_core_plugins(self)
        except Exception as e:
            self.logger.error(f"Failed to load core plugins: {e}")
        
        # Also try to load plugins from current directory
        await self._load_directory_plugins()
    
    async def _load_directory_plugins(self) -> None:
        """Load plugins from plugin directories"""
        current_dir = Path(__file__).parent
        
        # Try to load common plugins
        plugin_files = [
            "telegram_plugin.py",
            "project_analyzer_plugin.py"
        ]
        
        for plugin_file in plugin_files:
            plugin_path = current_dir / plugin_file
            if plugin_path.exists():
                try:
                    plugin_name = plugin_file.replace("_plugin.py", "").replace("_", "-")
                    self.logger.debug(f"Attempting to load {plugin_name} from {plugin_path}")
                    await self.load_plugin_from_path(plugin_name, plugin_path)
                except Exception as e:
                    self.logger.warning(f"Failed to load plugin {plugin_name}: {e}")
    
    async def load_plugin_from_path(self, plugin_name: str, plugin_path: Path) -> bool:
        """Load a plugin from a specific file path"""
        try:
            # Import the plugin module
            import importlib.util
            spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Find plugin classes in the module
            import inspect
            plugin_classes = [
                obj for name, obj in inspect.getmembers(module)
                if inspect.isclass(obj) and hasattr(obj, '__bases__') 
                and any('Plugin' in base.__name__ for base in obj.__bases__)
                and obj.__module__ == module.__name__
            ]
            
            if not plugin_classes:
                self.logger.warning(f"No plugin class found in {plugin_path}")
                return False
                
            # Instantiate and load the plugin
            plugin_class = plugin_classes[0]
            plugin = plugin_class()
            
            # Initialize plugin
            success = await plugin.load()
            if success:
                self.plugins[plugin_name] = plugin
                self.logger.info(f"Loaded plugin: {plugin_name}")
                return True
            else:
                self.logger.error(f"Failed to initialize plugin: {plugin_name}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error loading plugin {plugin_name}: {e}")
            return False
    
    async def discover_plugins(self) -> List[PluginMetadata]:
        """Discover all available plugins in plugin directories"""
        discovered = []
        
        for directory in self.plugin_directories:
            if not directory.exists():
                continue
                
            self.logger.debug(f"Scanning directory: {directory}")
            
            # Look for Python files
            for py_file in directory.rglob("*.py"):
                if py_file.stem.startswith("_"):
                    continue
                
                try:
                    metadata = await self.loader.extract_metadata(py_file)
                    if metadata:
                        discovered.append(metadata)
                        self.logger.debug(f"Found plugin: {metadata.name} v{metadata.version}")
                except Exception as e:
                    self.logger.warning(f"Failed to extract metadata from {py_file}: {e}")
        
        self.logger.info(f"Discovered {len(discovered)} plugins")
        return discovered
    
    async def load_plugin(self, plugin_name: str, plugin_path: Optional[Path] = None) -> bool:
        """Load a specific plugin"""
        if plugin_name in self.plugins:
            self.logger.warning(f"Plugin {plugin_name} is already loaded")
            return True
        
        try:
            # Load the plugin
            plugin = await self.loader.load_plugin(plugin_name, plugin_path)
            if not plugin:
                return False
            
            # Check dependencies
            if not await self._check_dependencies(plugin):
                self.logger.error(f"Dependencies not satisfied for plugin: {plugin_name}")
                return False
            
            # Initialize the plugin
            success = await plugin.load()
            if not success:
                self.logger.error(f"Failed to initialize plugin: {plugin_name}")
                return False
            
            # Register the plugin
            self.plugins[plugin_name] = plugin
            await self._register_plugin_services(plugin)
            await self._register_plugin_commands(plugin)
            
            # Update dependency tracking
            self._update_dependency_graph(plugin)
            
            # Setup hot reload if enabled
            if self.hot_reload_enabled and plugin.metadata.hot_reload:
                await self._setup_hot_reload(plugin)
            
            # Emit plugin loaded event
            await self._emit_event(PluginEvent(plugin_name, "plugin_loaded", plugin.metadata))
            
            self.logger.info(f"Successfully loaded plugin: {plugin_name} v{plugin.metadata.version}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load plugin {plugin_name}: {e}")
            return False
    
    async def unload_plugin(self, plugin_name: str, force: bool = False) -> bool:
        """Unload a specific plugin"""
        if plugin_name not in self.plugins:
            self.logger.warning(f"Plugin {plugin_name} is not loaded")
            return True
        
        plugin = self.plugins[plugin_name]
        
        try:
            # Check if other plugins depend on this one
            if not force and plugin_name in self.reverse_dependencies:
                dependents = list(self.reverse_dependencies[plugin_name])
                if dependents:
                    self.logger.error(f"Cannot unload {plugin_name}: depended on by {dependents}")
                    return False
            
            # Unload the plugin
            success = await plugin.unload()
            if not success and not force:
                self.logger.error(f"Failed to unload plugin: {plugin_name}")
                return False
            
            # Cleanup registrations
            await self._unregister_plugin_services(plugin)
            await self._unregister_plugin_commands(plugin)
            
            # Remove from tracking
            del self.plugins[plugin_name]
            self._remove_from_dependency_graph(plugin_name)
            
            # Cleanup hot reload
            if plugin_name in self.file_watchers:
                del self.file_watchers[plugin_name]
            
            # Emit plugin unloaded event
            await self._emit_event(PluginEvent(plugin_name, "plugin_unloaded"))
            
            self.logger.info(f"Successfully unloaded plugin: {plugin_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to unload plugin {plugin_name}: {e}")
            return False
    
    async def reload_plugin(self, plugin_name: str) -> bool:
        """Reload a specific plugin"""
        if plugin_name not in self.plugins:
            return await self.load_plugin(plugin_name)
        
        plugin = self.plugins[plugin_name]
        
        try:
            # Reload the plugin module
            await self.loader.reload_plugin_module(plugin_name)
            
            # Reload the plugin instance
            success = await plugin.reload()
            if success:
                # Re-register services and commands
                await self._register_plugin_services(plugin)
                await self._register_plugin_commands(plugin)
                
                # Emit plugin reloaded event
                await self._emit_event(PluginEvent(plugin_name, "plugin_reloaded", plugin.metadata))
                
                self.logger.info(f"Successfully reloaded plugin: {plugin_name}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to reload plugin {plugin_name}: {e}")
            return False
    
    async def load_all_plugins(self) -> Dict[str, bool]:
        """Load all discovered plugins in dependency order"""
        discovered = await self.discover_plugins()
        load_order = self._resolve_load_order(discovered)
        
        results = {}
        for plugin_name in load_order:
            results[plugin_name] = await self.load_plugin(plugin_name)
        
        loaded_count = sum(1 for success in results.values() if success)
        self.logger.info(f"Loaded {loaded_count}/{len(discovered)} plugins")
        
        return results
    
    def get_plugin(self, plugin_name: str) -> Optional[XKitPlugin]:
        """Get a loaded plugin by name"""
        return self.plugins.get(plugin_name)
    
    def get_service(self, service_name: str) -> Optional[Any]:
        """Get a service by name"""
        return self.services.get(service_name)
    
    def get_command_handler(self, command_name: str) -> Optional[tuple[str, callable]]:
        """Get command handler by command name"""
        return self.commands.get(command_name)
    
    async def execute_command(self, command_name: str, *args, **kwargs) -> Any:
        """Execute a command provided by a plugin"""
        handler_info = self.get_command_handler(command_name)
        if not handler_info:
            raise ValueError(f"Unknown command: {command_name}")
        
        plugin_name, handler = handler_info
        plugin = self.get_plugin(plugin_name)
        
        if not plugin or plugin.status != PluginStatus.ACTIVE:
            raise RuntimeError(f"Plugin {plugin_name} is not active")
        
        # Execute the command
        try:
            if asyncio.iscoroutinefunction(handler):
                return await handler(*args, **kwargs)
            else:
                return handler(*args, **kwargs)
        except Exception as e:
            self.logger.error(f"Command {command_name} failed: {e}")
            raise
    
    async def get_plugin_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all loaded plugins"""
        status = {}
        for name, plugin in self.plugins.items():
            status[name] = await plugin.health_check()
        return status
    
    async def _check_dependencies(self, plugin: XKitPlugin) -> bool:
        """Check if plugin dependencies are satisfied"""
        for dep in plugin.metadata.dependencies:
            if dep not in self.plugins:
                return False
            if self.plugins[dep].status != PluginStatus.ACTIVE:
                return False
        return True
    
    def _resolve_load_order(self, plugins: List[PluginMetadata]) -> List[str]:
        """Resolve plugin load order based on dependencies"""
        # Simple topological sort
        plugin_map = {p.name: p for p in plugins}
        visited = set()
        order = []
        
        def visit(name: str):
            if name in visited:
                return
            visited.add(name)
            
            if name in plugin_map:
                plugin = plugin_map[name]
                for dep in plugin.dependencies:
                    if dep in plugin_map:
                        visit(dep)
            
            order.append(name)
        
        # Sort by priority first
        sorted_plugins = sorted(plugins, key=lambda p: p.priority)
        for plugin in sorted_plugins:
            visit(plugin.name)
        
        return order
    
    def _update_dependency_graph(self, plugin: XKitPlugin) -> None:
        """Update dependency tracking graphs"""
        name = plugin.metadata.name
        
        for dep in plugin.metadata.dependencies:
            self.dependency_graph[name].add(dep)
            self.reverse_dependencies[dep].add(name)
    
    def _remove_from_dependency_graph(self, plugin_name: str) -> None:
        """Remove plugin from dependency graphs"""
        # Remove outgoing dependencies
        if plugin_name in self.dependency_graph:
            for dep in self.dependency_graph[plugin_name]:
                self.reverse_dependencies[dep].discard(plugin_name)
            del self.dependency_graph[plugin_name]
        
        # Remove incoming dependencies
        if plugin_name in self.reverse_dependencies:
            for dependent in self.reverse_dependencies[plugin_name]:
                self.dependency_graph[dependent].discard(plugin_name)
            del self.reverse_dependencies[plugin_name]
    
    async def _register_plugin_services(self, plugin: XKitPlugin) -> None:
        """Register services provided by a plugin"""
        plugin_services = plugin.get_services()
        
        for service_name, service in plugin_services.items():
            if service_name in self.services:
                self.logger.warning(f"Service {service_name} already registered, overriding")
            
            self.services[service_name] = service
            self.service_providers[service_name] = plugin.metadata.name
    
    async def _unregister_plugin_services(self, plugin: XKitPlugin) -> None:
        """Unregister services provided by a plugin"""
        plugin_name = plugin.metadata.name
        
        # Remove services provided by this plugin
        services_to_remove = [
            name for name, provider in self.service_providers.items()
            if provider == plugin_name
        ]
        
        for service_name in services_to_remove:
            if service_name in self.services:
                del self.services[service_name]
            del self.service_providers[service_name]
    
    async def _register_plugin_commands(self, plugin: XKitPlugin) -> None:
        """Register commands provided by a plugin"""
        plugin_commands = plugin.get_commands()
        
        for command_name, handler in plugin_commands.items():
            if command_name in self.commands:
                self.logger.warning(f"Command {command_name} already registered, overriding")
            
            self.commands[command_name] = (plugin.metadata.name, handler)
            
            # Also register in global command service if available
            try:
                # Access command service from the container
                if hasattr(self, '_command_service') and self._command_service:
                    self._command_service.register_command(
                        command_name, 
                        handler,
                        description=f"Plugin command from {plugin.metadata.name}",
                        category=plugin.metadata.name
                    )
            except Exception as e:
                self.logger.warning(f"Failed to register command {command_name} in command service: {e}")
    
    def set_command_service(self, command_service) -> None:
        """Set the command service reference for plugin command registration"""
        self._command_service = command_service
    
    async def _unregister_plugin_commands(self, plugin: XKitPlugin) -> None:
        """Unregister commands provided by a plugin"""
        plugin_name = plugin.metadata.name
        
        # Remove commands provided by this plugin
        commands_to_remove = [
            name for name, (provider, _) in self.commands.items()
            if provider == plugin_name
        ]
        
        for command_name in commands_to_remove:
            del self.commands[command_name]
    
    async def _setup_hot_reload(self, plugin: XKitPlugin) -> None:
        """Setup hot reload monitoring for a plugin"""
        # Placeholder for file system watching
        # In a real implementation, you'd use watchdog or similar
        pass
    
    def enable_hot_reload(self, enabled: bool = True) -> None:
        """Enable or disable hot reload for plugins"""
        self.hot_reload_enabled = enabled
        self.logger.info(f"Hot reload {'enabled' if enabled else 'disabled'}")
        
    async def async_enable_hot_reload(self, plugin_directories = None) -> None:
        """Async version for enabling hot reload with directories"""
        self.hot_reload_enabled = True
        if plugin_directories:
            self.plugin_directories.extend(plugin_directories)
        self.logger.info("Hot reload enabled")
    
    async def _emit_event(self, event: PluginEvent) -> None:
        """Emit an event to all plugins"""
        for plugin in self.plugins.values():
            try:
                await plugin.handle_event(event)
            except Exception as e:
                self.logger.error(f"Plugin {plugin.metadata.name} event handler error: {e}")
    
    async def shutdown(self) -> None:
        """Shutdown the plugin manager and unload all plugins"""
        self.logger.info("Shutting down Plugin Manager")
        
        # Unload all plugins in reverse dependency order
        unload_order = list(reversed(list(self.plugins.keys())))
        
        for plugin_name in unload_order:
            await self.unload_plugin(plugin_name, force=True)
        
        # Clear all registries
        self.plugins.clear()
        self.services.clear()
        self.service_providers.clear()
        self.commands.clear()
        
        self.logger.info("Plugin Manager shutdown complete")