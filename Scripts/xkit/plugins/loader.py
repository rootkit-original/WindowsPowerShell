"""
XKit Plugin Loader
Handles loading and reloading of plugin modules with metadata extraction
"""
import asyncio
import importlib
import importlib.util
import inspect
import sys
from typing import Dict, Any, List, Optional, Type
from pathlib import Path
import ast
import logging

from .base import XKitPlugin, PluginMetadata


class PluginLoader:
    """Handles loading and reloading of plugin modules"""
    
    def __init__(self):
        self.loaded_modules: Dict[str, Any] = {}
        self.module_paths: Dict[str, Path] = {}
        self.logger = logging.getLogger(__name__)
    
    async def extract_metadata(self, plugin_path: Path) -> Optional[PluginMetadata]:
        """Extract plugin metadata from Python file"""
        try:
            # Parse the file to extract metadata
            with open(plugin_path, 'r', encoding='utf-8') as f:
                source = f.read()
            
            tree = ast.parse(source)
            metadata_dict = {}
            
            # Look for module-level variables
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            name = target.id
                            if name.startswith('PLUGIN_'):
                                try:
                                    value = ast.literal_eval(node.value)
                                    metadata_dict[name] = value
                                except (ValueError, TypeError):
                                    pass
            
            # Extract from docstring or variables
            plugin_name = metadata_dict.get('PLUGIN_NAME')
            if not plugin_name:
                plugin_name = plugin_path.stem.replace('_', '-')
            
            return PluginMetadata(
                name=plugin_name,
                version=metadata_dict.get('PLUGIN_VERSION', '1.0.0'),
                description=metadata_dict.get('PLUGIN_DESCRIPTION', f'XKit plugin: {plugin_name}'),
                author=metadata_dict.get('PLUGIN_AUTHOR', 'Unknown'),
                dependencies=metadata_dict.get('PLUGIN_DEPENDENCIES', []),
                provides=metadata_dict.get('PLUGIN_PROVIDES', [plugin_name]),
                requires=metadata_dict.get('PLUGIN_REQUIRES', []),
                hot_reload=metadata_dict.get('PLUGIN_HOT_RELOAD', True),
                priority=metadata_dict.get('PLUGIN_PRIORITY', 100)
            )
            
        except Exception as e:
            self.logger.error(f"Failed to extract metadata from {plugin_path}: {e}")
            return None
    
    async def load_plugin(self, plugin_name: str, plugin_path: Optional[Path] = None) -> Optional[XKitPlugin]:
        """Load a plugin from file or module name"""
        try:
            if plugin_path:
                # Load from specific file path
                module = await self._load_module_from_path(plugin_name, plugin_path)
            else:
                # Load from module name
                module = await self._load_module_from_name(plugin_name)
            
            if not module:
                return None
            
            # Find plugin class in module
            plugin_class = self._find_plugin_class(module)
            if not plugin_class:
                self.logger.error(f"No plugin class found in {plugin_name}")
                return None
            
            # Create plugin instance
            plugin = plugin_class()
            
            # Store module reference
            self.loaded_modules[plugin_name] = module
            if plugin_path:
                self.module_paths[plugin_name] = plugin_path
            
            return plugin
            
        except Exception as e:
            self.logger.error(f"Failed to load plugin {plugin_name}: {e}")
            return None
    
    async def _load_module_from_path(self, plugin_name: str, plugin_path: Path) -> Optional[Any]:
        """Load module from file path"""
        try:
            spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
            if not spec or not spec.loader:
                return None
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Add to sys.modules for importlib compatibility
            sys.modules[plugin_name] = module
            
            return module
            
        except Exception as e:
            self.logger.error(f"Failed to load module from {plugin_path}: {e}")
            return None
    
    async def _load_module_from_name(self, plugin_name: str) -> Optional[Any]:
        """Load module from module name"""
        try:
            return importlib.import_module(plugin_name)
        except ImportError as e:
            self.logger.error(f"Failed to import module {plugin_name}: {e}")
            return None
    
    def _find_plugin_class(self, module: Any) -> Optional[Type[XKitPlugin]]:
        """Find XKitPlugin subclass in module"""
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if (issubclass(obj, XKitPlugin) and 
                obj is not XKitPlugin and 
                obj.__module__ == module.__name__):
                return obj
        return None
    
    async def reload_plugin_module(self, plugin_name: str) -> bool:
        """Reload a plugin module"""
        try:
            if plugin_name not in self.loaded_modules:
                self.logger.warning(f"Module {plugin_name} not loaded, cannot reload")
                return False
            
            module = self.loaded_modules[plugin_name]
            
            # Reload the module
            importlib.reload(module)
            
            self.logger.debug(f"Reloaded module: {plugin_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to reload module {plugin_name}: {e}")
            return False
    
    async def unload_plugin_module(self, plugin_name: str) -> bool:
        """Unload a plugin module"""
        try:
            if plugin_name in self.loaded_modules:
                del self.loaded_modules[plugin_name]
            
            if plugin_name in self.module_paths:
                del self.module_paths[plugin_name]
            
            if plugin_name in sys.modules:
                del sys.modules[plugin_name]
            
            self.logger.debug(f"Unloaded module: {plugin_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to unload module {plugin_name}: {e}")
            return False
    
    def get_loaded_modules(self) -> Dict[str, Any]:
        """Get dictionary of loaded modules"""
        return self.loaded_modules.copy()
    
    def is_module_loaded(self, plugin_name: str) -> bool:
        """Check if a module is loaded"""
        return plugin_name in self.loaded_modules
    
    async def validate_plugin_class(self, plugin_class: Type[XKitPlugin]) -> List[str]:
        """Validate a plugin class implementation"""
        issues = []
        
        # Check required methods
        required_methods = ['load', 'unload', 'get_commands']
        for method_name in required_methods:
            if not hasattr(plugin_class, method_name):
                issues.append(f"Missing required method: {method_name}")
            else:
                method = getattr(plugin_class, method_name)
                if not callable(method):
                    issues.append(f"Method {method_name} is not callable")
        
        # Check if class has proper constructor
        try:
            sig = inspect.signature(plugin_class.__init__)
            # Should accept at least self parameter
            if len(sig.parameters) < 1:
                issues.append("Constructor should accept at least self parameter")
        except Exception as e:
            issues.append(f"Cannot inspect constructor: {e}")
        
        return issues