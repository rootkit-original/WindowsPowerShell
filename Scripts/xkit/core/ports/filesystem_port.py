"""
Filesystem Service Port
Interface for filesystem operations
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from pathlib import Path


class IFilesystemService(ABC):
    """Port for filesystem operations"""
    
    @abstractmethod
    def read_file(self, file_path: str) -> str:
        """Read file contents"""
        pass
    
    @abstractmethod
    def write_file(self, file_path: str, content: str) -> bool:
        """Write content to file"""
        pass
    
    @abstractmethod
    def file_exists(self, file_path: str) -> bool:
        """Check if file exists"""
        pass
    
    @abstractmethod
    def list_directory(self, dir_path: str) -> List[str]:
        """List directory contents"""
        pass
    
    @abstractmethod
    def create_directory(self, dir_path: str) -> bool:
        """Create directory"""
        pass
    
    @abstractmethod
    def get_absolute_path(self, path: str) -> str:
        """Get absolute path"""
        pass