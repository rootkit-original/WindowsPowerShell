"""
XKit Plugin Template
Template for creating new XKit v3.0 plugins

Usage:
1. Copy this file to Scripts/xkit/plugins/{your_plugin_name}_plugin.py
2. Replace all {TEMPLATE_*} placeholders with your values
3. Implement the required methods
4. Add your plugin documentation to docs/plugins/{your-plugin-name}.md

Template Variables:
- {TEMPLATE_PLUGIN_NAME} - Plugin name (kebab-case, e.g., 'my-awesome-plugin')
- {TEMPLATE_PLUGIN_CLASS} - Plugin class name (PascalCase, e.g., 'MyAwesomePlugin')
- {TEMPLATE_PLUGIN_DESCRIPTION} - Brief description of plugin functionality
- {TEMPLATE_PLUGIN_VERSION} - Plugin version (semantic versioning, e.g., '1.0.0')
- {TEMPLATE_AUTHOR_NAME} - Your name or organization
"""
import asyncio
import logging
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path

from xkit.plugins.base import XKitCorePlugin, PluginMetadata
from xkit.infrastructure.config import XKitConfigService
from xkit.core.ports.event_port import IEventService


class XKit{TEMPLATE_PLUGIN_CLASS}Plugin(XKitCorePlugin):
    """
    {TEMPLATE_PLUGIN_DESCRIPTION}
    
    This plugin provides:
    - Feature 1 description
    - Feature 2 description
    - Feature 3 description
    
    Commands:
    - {TEMPLATE_PLUGIN_NAME}-command: Description of command
    - another-command: Description of another command
    """
    
    def __init__(self):
        super().__init__(
            name="{TEMPLATE_PLUGIN_NAME}",
            version="{TEMPLATE_PLUGIN_VERSION}",
            description="{TEMPLATE_PLUGIN_DESCRIPTION}"
        )
        
        # Plugin-specific attributes
        self.config_data: Optional[Dict[str, Any]] = None
        self.is_configured = False
        
        # Services (initialized in _initialize_services)
        self.config_service: Optional[XKitConfigService] = None
        self.event_bus: Optional[IEventService] = None
    
    async def load(self) -> bool:
        """
        Load and initialize the plugin
        
        Returns:
            bool: True if plugin loaded successfully, False otherwise
        """
        try:
            # Initialize services
            await self._initialize_services()
            
            # Load configuration
            await self._load_config()
            
            # Initialize plugin-specific resources
            await self._initialize_plugin_resources()
            
            # Subscribe to events if needed
            await self._subscribe_to_events()
            
            self.logger.info(f"Plugin {self.name} v{self.version} loaded successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load plugin {self.name}: {e}")
            return False
    
    async def unload(self) -> bool:
        """
        Unload and cleanup the plugin
        
        Returns:
            bool: True if plugin unloaded successfully, False otherwise
        """
        try:
            # Cleanup plugin-specific resources
            await self._cleanup_plugin_resources()
            
            # Unsubscribe from events
            await self._unsubscribe_from_events()
            
            # Cleanup services
            await self._cleanup_services()
            
            self.logger.info(f"Plugin {self.name} unloaded successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to unload plugin {self.name}: {e}")
            return False
    
    def get_commands(self) -> Dict[str, Callable]:
        """
        Return dictionary of commands provided by this plugin
        
        Returns:
            Dict[str, Callable]: Command name -> handler mapping
        """
        return {
            "{TEMPLATE_PLUGIN_NAME}-command": self.handle_main_command,
            "another-command": self.handle_another_command,
            # Add more commands as needed
        }
    
    def get_services(self) -> Dict[str, Any]:
        """
        Return services provided by this plugin
        
        Returns:
            Dict[str, Any]: Service name -> service instance mapping
        """
        return {
            # Example: "{TEMPLATE_PLUGIN_NAME}_service": self.service_instance,
        }
    
    # ====================================
    # Plugin Initialization Methods
    # ====================================
    
    async def _initialize_services(self) -> None:
        """Initialize XKit services needed by this plugin"""
        # Get core services
        self.config_service = self.get_service("config_service")
        self.event_bus = self.get_service("event_bus")
        
        # Register services this plugin provides
        # self.register_service("my_service", self.my_service_instance)
    
    async def _load_config(self) -> None:
        """Load plugin configuration"""
        if self.config_service:
            self.config_data = await self.config_service.get_plugin_config(self.name)
            self.is_configured = self.config_data is not None
            
            if not self.is_configured:
                self.logger.warning(f"No configuration found for plugin {self.name}")
        else:
            self.logger.warning("Config service not available")
    
    async def _initialize_plugin_resources(self) -> None:
        """Initialize plugin-specific resources"""
        # TODO: Implement plugin-specific initialization
        # Examples:
        # - Initialize API clients
        # - Setup database connections
        # - Create temporary directories
        # - Load data files
        pass
    
    async def _subscribe_to_events(self) -> None:
        """Subscribe to relevant events"""
        if self.event_bus:
            # Example event subscriptions
            # await self.event_bus.subscribe("command_executed", self._on_command_executed)
            # await self.event_bus.subscribe("plugin_loaded", self._on_plugin_loaded)
            pass
    
    # ====================================
    # Plugin Cleanup Methods
    # ====================================
    
    async def _cleanup_plugin_resources(self) -> None:
        """Cleanup plugin-specific resources"""
        # TODO: Implement plugin-specific cleanup
        # Examples:
        # - Close API connections
        # - Close database connections
        # - Delete temporary files
        # - Cancel background tasks
        pass
    
    async def _unsubscribe_from_events(self) -> None:
        """Unsubscribe from events"""
        if self.event_bus:
            # Example event unsubscriptions
            # await self.event_bus.unsubscribe("command_executed", self._on_command_executed)
            pass
    
    async def _cleanup_services(self) -> None:
        """Cleanup services provided by this plugin"""
        # Unregister services
        # self.unregister_service("my_service")
        pass
    
    # ====================================
    # Command Handlers
    # ====================================
    
    async def handle_main_command(self, args: List[str]) -> Optional[str]:
        """
        Handle the main plugin command
        
        Args:
            args: List of command arguments
            
        Returns:
            Optional[str]: Command output or None for silent execution
        """
        try:
            # Validate plugin is configured
            if not self.is_configured:
                return "❌ Plugin not configured. Please check configuration."
            
            # Validate arguments
            if not args:
                return self._get_command_help()
            
            # Process command
            result = await self._process_main_command(args)
            
            return f"✅ {TEMPLATE_PLUGIN_NAME} command completed: {result}"
            
        except Exception as e:
            self.logger.error(f"Command execution failed: {e}")
            return f"❌ Command failed: {str(e)}"
    
    async def handle_another_command(self, args: List[str]) -> Optional[str]:
        """
        Handle another command provided by this plugin
        
        Args:
            args: List of command arguments
            
        Returns:
            Optional[str]: Command output or None for silent execution
        """
        try:
            # TODO: Implement command logic
            result = await self._process_another_command(args)
            return f"✅ Another command result: {result}"
            
        except Exception as e:
            self.logger.error(f"Another command failed: {e}")
            return f"❌ Command failed: {str(e)}"
    
    # ====================================
    # Event Handlers
    # ====================================
    
    async def _on_command_executed(self, event) -> None:
        """Handle command execution events"""
        # TODO: Implement event handling logic
        # Example: React to specific commands
        if event.command.startswith("git-"):
            await self._handle_git_related_event(event)
    
    async def _on_plugin_loaded(self, event) -> None:
        """Handle plugin loaded events"""
        # TODO: Implement event handling logic
        # Example: React when other plugins are loaded
        pass
    
    # ====================================
    # Helper Methods
    # ====================================
    
    async def _process_main_command(self, args: List[str]) -> str:
        """
        Process the main command logic
        
        Args:
            args: Command arguments
            
        Returns:
            str: Processing result
        """
        # TODO: Implement main command logic
        return "Main command processed successfully"
    
    async def _process_another_command(self, args: List[str]) -> str:
        """
        Process another command logic
        
        Args:
            args: Command arguments
            
        Returns:
            str: Processing result
        """
        # TODO: Implement another command logic
        return "Another command processed successfully"
    
    def _get_command_help(self) -> str:
        """
        Get help text for the plugin commands
        
        Returns:
            str: Formatted help text
        """
        return f"""
🔌 {TEMPLATE_PLUGIN_CLASS} Plugin Help

Available Commands:
  {TEMPLATE_PLUGIN_NAME}-command [args]  - Description of main command
  another-command [args]                - Description of another command

Examples:
  {TEMPLATE_PLUGIN_NAME}-command --help
  another-command example arg

For more information, see: docs/plugins/{TEMPLATE_PLUGIN_NAME}.md
"""
    
    async def _handle_git_related_event(self, event) -> None:
        """Handle Git-related events"""
        # TODO: Implement Git event handling
        pass
    
    async def health_check(self) -> bool:
        """
        Perform plugin health check
        
        Returns:
            bool: True if plugin is healthy, False otherwise
        """
        try:
            # Check if plugin is configured
            if not self.is_configured:
                return False
            
            # Check if services are available
            if not self.config_service:
                return False
            
            # TODO: Add plugin-specific health checks
            # Examples:
            # - Check API connectivity
            # - Verify database connection
            # - Test critical functionality
            
            return True
            
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return False


# ====================================
# Plugin Entry Point (if needed)
# ====================================

def create_plugin() -> XKit{TEMPLATE_PLUGIN_CLASS}Plugin:
    """
    Factory function to create plugin instance
    
    Returns:
        XKit{TEMPLATE_PLUGIN_CLASS}Plugin: Plugin instance
    """
    return XKit{TEMPLATE_PLUGIN_CLASS}Plugin()


# ====================================
# Plugin Metadata (Optional)
# ====================================

PLUGIN_INFO = {
    "name": "{TEMPLATE_PLUGIN_NAME}",
    "version": "{TEMPLATE_PLUGIN_VERSION}",
    "description": "{TEMPLATE_PLUGIN_DESCRIPTION}",
    "author": "{TEMPLATE_AUTHOR_NAME}",
    "license": "MIT",
    "homepage": "https://github.com/rootkit-original/WindowsPowerShell",
    "dependencies": [
        # List any Python package dependencies
        # "requests>=2.25.0",
        # "aiohttp>=3.8.0",
    ],
    "xkit_version": ">=3.0.0",
    "categories": ["utility", "productivity"],  # Adjust categories as needed
    "tags": ["{TEMPLATE_PLUGIN_NAME}", "automation", "productivity"]
}