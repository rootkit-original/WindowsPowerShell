"""
Command Service Port
Interface for command execution and management
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass


@dataclass
class CommandResult:
    """Result of command execution"""
    success: bool
    output: Any = None
    error: Optional[str] = None
    execution_time: float = 0.0
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class ICommandService(ABC):
    """Port for command execution services"""
    
    @abstractmethod
    async def execute_command(self, command: str, args: List[str] = None, 
                            context: Dict[str, Any] = None) -> CommandResult:
        """Execute a command with given arguments"""
        pass
    
    @abstractmethod
    def list_available_commands(self) -> List[str]:
        """Get list of available commands"""
        pass
    
    @abstractmethod
    def get_command_help(self, command: str) -> Optional[str]:
        """Get help text for a specific command"""
        pass
    
    @abstractmethod
    def register_command(self, command: str, handler: callable, 
                        description: str = "", category: str = "general") -> bool:
        """Register a new command handler"""
        pass
    
    @abstractmethod
    def unregister_command(self, command: str) -> bool:
        """Unregister a command handler"""
        pass
    
    @abstractmethod
    def validate_command(self, command: str, args: List[str] = None) -> bool:
        """Validate command and arguments before execution"""
        pass