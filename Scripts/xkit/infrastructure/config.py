"""
Configuration Service Implementation
"""
import json
from typing import Any, Dict, Optional, List
from pathlib import Path

from ..core.ports import IConfigService


class XKitConfigService(IConfigService):
    """Simple configuration service for XKit v3.0"""
    
    def __init__(self, config_file: Optional[Path] = None):
        self.config_file = config_file or Path.home() / ".xkit" / "config.json"
        self.config: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                # Default configuration
                self.config = {
                    "system": {
                        "debug": False,
                        "log_level": "INFO"
                    },
                    "mcp": {
                        "enabled": True,
                        "max_connections": 10
                    },
                    "plugins": {
                        "auto_load": True,
                        "directories": []
                    },
                    "display": {
                        "emojis": True,
                        "colors": True
                    }
                }
                self._ensure_config_dir()
                self.save_config()
        except Exception:
            # Fallback to empty config
            self.config = {}
    
    def _ensure_config_dir(self) -> None:
        """Ensure configuration directory exists"""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation"""
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> bool:
        """Set configuration value using dot notation"""
        keys = key.split('.')
        config = self.config
        
        try:
            # Navigate to parent
            for k in keys[:-1]:
                if k not in config:
                    config[k] = {}
                config = config[k]
            
            # Set the value
            config[keys[-1]] = value
            return True
        except Exception:
            return False
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """Get entire configuration section"""
        return self.get(section, {})
    
    def has_key(self, key: str) -> bool:
        """Check if configuration key exists"""
        return self.get(key) is not None
    
    def list_keys(self, section: Optional[str] = None) -> List[str]:
        """List available configuration keys"""
        if section:
            config_section = self.get_section(section)
            return list(config_section.keys()) if config_section else []
        else:
            return list(self.config.keys())
    
    def save_config(self) -> bool:
        """Save configuration to disk"""
        try:
            self._ensure_config_dir()
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def reload_config(self) -> bool:
        """Reload configuration from disk"""
        try:
            self._load_config()
            return True
        except Exception:
            return False


# Alias for v3.0 compatibility
ConfigService = XKitConfigService