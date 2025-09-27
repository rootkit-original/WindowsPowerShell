"""
Core Plugin Auto-Loader
Automatically registers and loads core XKit plugins
"""
import logging
from pathlib import Path
from typing import List


class CorePluginRegistry:
    """Registry for core XKit plugins"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Empty for now - plugins will be loaded from directory
        self._core_plugins = []
    
    def get_core_plugins(self) -> List[type]:
        """Get list of core plugin classes"""
        return self._core_plugins
    
    async def load_all_core_plugins(self, plugin_manager) -> None:
        """Load all core plugins into the plugin manager"""
        self.logger.info("No core plugins to auto-load - using directory discovery")
    
    def get_plugin_commands(self) -> dict:
        """Get all commands from core plugins (for registration before loading)"""
        return {}


# Global registry instance
core_plugin_registry = CorePluginRegistry()