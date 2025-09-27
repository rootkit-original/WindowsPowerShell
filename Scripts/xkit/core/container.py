"""
XKit Dependency Injection Container
Manages service registration and resolution
"""
import logging
from typing import Dict, Type, Any, Optional, Callable
from abc import ABC


class XKitContainer:
    """Dependency injection container for XKit services"""
    
    def __init__(self):
        self._services: Dict[Type, Any] = {}
        self._factories: Dict[Type, Callable] = {}
        self._singletons: Dict[Type, Any] = {}
        self._initialized = False
        self.logger = logging.getLogger(__name__)
    
    def register_singleton(self, interface: Type, implementation: Any) -> None:
        """Register a singleton service"""
        self._singletons[interface] = implementation
        self.logger.debug(f"Registered singleton: {interface.__name__} -> {type(implementation).__name__}")
    
    def register_factory(self, interface: Type, factory: Callable) -> None:
        """Register a factory function for creating services"""
        self._factories[interface] = factory
        self.logger.debug(f"Registered factory: {interface.__name__}")
    
    def register_instance(self, interface: Type, instance: Any) -> None:
        """Register a specific instance"""
        self._services[interface] = instance
        self.logger.debug(f"Registered instance: {interface.__name__} -> {type(instance).__name__}")
    
    def get_service(self, interface: Type) -> Any:
        """Get a service instance"""
        if not self._initialized:
            raise RuntimeError("Container not initialized. Call initialize() first.")
        
        # Check if already instantiated
        if interface in self._services:
            return self._services[interface]
        
        # Check singletons
        if interface in self._singletons:
            instance = self._singletons[interface]
            self._services[interface] = instance
            return instance
        
        # Check factories
        if interface in self._factories:
            factory = self._factories[interface]
            instance = factory()
            self._services[interface] = instance
            return instance
        
        raise ValueError(f"Service not registered: {interface.__name__}")
    
    def has_service(self, interface: Type) -> bool:
        """Check if a service is registered"""
        return (interface in self._services or 
                interface in self._singletons or 
                interface in self._factories)
    
    async def initialize(self) -> None:
        """Initialize the container and all registered services"""
        if self._initialized:
            return
        
        self.logger.info("Initializing dependency container...")
        
        # Initialize any services that need async initialization
        for interface, instance in self._singletons.items():
            if hasattr(instance, 'initialize') and callable(instance.initialize):
                try:
                    await instance.initialize()
                    self.logger.debug(f"Initialized service: {interface.__name__}")
                except Exception as e:
                    self.logger.error(f"Failed to initialize {interface.__name__}: {e}")
                    raise
        
        self._initialized = True
        self.logger.info(f"Container initialized with {len(self._singletons)} singletons, {len(self._factories)} factories")
    
    async def cleanup(self) -> None:
        """Cleanup all services"""
        self.logger.info("Cleaning up dependency container...")
        
        # Cleanup services in reverse order
        for interface, instance in reversed(list(self._services.items())):
            if hasattr(instance, 'cleanup') and callable(instance.cleanup):
                try:
                    await instance.cleanup()
                    self.logger.debug(f"Cleaned up service: {interface.__name__}")
                except Exception as e:
                    self.logger.error(f"Failed to cleanup {interface.__name__}: {e}")
        
        # Cleanup singletons
        for interface, instance in reversed(list(self._singletons.items())):
            if hasattr(instance, 'cleanup') and callable(instance.cleanup):
                try:
                    await instance.cleanup()
                    self.logger.debug(f"Cleaned up singleton: {interface.__name__}")
                except Exception as e:
                    self.logger.error(f"Failed to cleanup singleton {interface.__name__}: {e}")
        
        self._services.clear()
        self._initialized = False
        self.logger.info("Container cleanup complete")
    
    def list_services(self) -> Dict[str, str]:
        """List all registered services"""
        services = {}
        
        for interface in self._services:
            services[interface.__name__] = "instance"
        
        for interface in self._singletons:
            services[interface.__name__] = "singleton"
        
        for interface in self._factories:
            services[interface.__name__] = "factory"
        
        return services
    
    def get_status(self) -> Dict[str, Any]:
        """Get container status"""
        return {
            "initialized": self._initialized,
            "service_count": len(self._services),
            "singleton_count": len(self._singletons),
            "factory_count": len(self._factories),
            "services": self.list_services()
        }


# Global container instance for backward compatibility
# This will be initialized by the main application
container: Optional[XKitContainer] = None


def set_global_container(container_instance: XKitContainer) -> None:
    """Set the global container instance"""
    global container
    container = container_instance


def get_global_container() -> Optional[XKitContainer]:
    """Get the global container instance"""
    return container