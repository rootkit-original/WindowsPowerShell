"""
Config Service Port
Interface for configuration management
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List


class IConfigService(ABC):
    """Port for configuration operations"""
    
    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        pass
    
    @abstractmethod
    def set(self, key: str, value: Any) -> bool:
        """Set configuration value"""
        pass
    
    @abstractmethod
    def get_section(self, section: str) -> Dict[str, Any]:
        """Get entire configuration section"""
        pass
    
    @abstractmethod
    def has_key(self, key: str) -> bool:
        """Check if configuration key exists"""
        pass
    
    @abstractmethod
    def list_keys(self, section: Optional[str] = None) -> List[str]:
        """List available configuration keys"""
        pass
    
    @abstractmethod
    def save_config(self) -> bool:
        """Save configuration to disk"""
        pass
    
    @abstractmethod
    def reload_config(self) -> bool:
        """Reload configuration from disk"""
        pass