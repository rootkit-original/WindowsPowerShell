"""
Telegram Service Port
Interface for Telegram notifications and bot operations
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class MessageType(Enum):
    """Telegram message types"""
    TEXT = "text"
    MARKDOWN = "markdown"
    HTML = "html"
    CODE = "code"


@dataclass
class TelegramMessage:
    """Telegram message"""
    text: str
    message_type: MessageType = MessageType.TEXT
    chat_id: Optional[str] = None
    parse_mode: Optional[str] = None
    disable_notification: bool = False


class ITelegramService(ABC):
    """Port for Telegram operations"""
    
    @abstractmethod
    async def send_message(self, message: TelegramMessage) -> bool:
        """Send a message via Telegram"""
        pass
    
    @abstractmethod
    async def send_error_notification(self, error: str, 
                                    context: Dict[str, Any] = None) -> bool:
        """Send error notification"""
        pass
    
    @abstractmethod
    async def send_success_notification(self, message: str) -> bool:
        """Send success notification"""
        pass
    
    @abstractmethod
    async def send_system_status(self, status: Dict[str, Any]) -> bool:
        """Send system status update"""
        pass
    
    @abstractmethod
    def is_configured(self) -> bool:
        """Check if Telegram is configured"""
        pass
    
    @abstractmethod
    def is_enabled(self) -> bool:
        """Check if Telegram notifications are enabled"""
        pass