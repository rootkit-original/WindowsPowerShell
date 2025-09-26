"""
Display Service Port
Interface for display and UI operations
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from enum import Enum


class DisplayLevel(Enum):
    """Display message levels"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"


class IDisplayService(ABC):
    """Port for display operations"""
    
    @abstractmethod
    def display_message(self, message: str, level: DisplayLevel = DisplayLevel.INFO) -> None:
        """Display a message"""
        pass
    
    @abstractmethod
    def display_error(self, error: str, details: Optional[str] = None) -> None:
        """Display an error message"""
        pass
    
    @abstractmethod
    def display_success(self, message: str) -> None:
        """Display a success message"""
        pass
    
    @abstractmethod
    def display_table(self, data: List[Dict[str, Any]], headers: List[str] = None) -> None:
        """Display data in table format"""
        pass
    
    @abstractmethod
    def display_progress(self, current: int, total: int, message: str = "") -> None:
        """Display progress indicator"""
        pass
    
    @abstractmethod
    def clear_screen(self) -> None:
        """Clear the display"""
        pass