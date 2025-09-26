"""
XKit Core Ports
Defines interfaces for clean architecture boundaries
"""

from .command_port import ICommandService
from .git_port import IGitService
from .ai_port import IAIService
from .filesystem_port import IFilesystemService
from .display_port import IDisplayService
from .config_port import IConfigService
from .container_port import IContainerService
from .telegram_port import ITelegramService
from .event_port import IEventService
from .plugin_port import IPluginService
from .mcp_port import IMCPService

__all__ = [
    'ICommandService',
    'IGitService', 
    'IAIService',
    'IFilesystemService',
    'IDisplayService',
    'IConfigService',
    'IContainerService',
    'ITelegramService',
    'IEventService',
    'IPluginService',
    'IMCPService'
]