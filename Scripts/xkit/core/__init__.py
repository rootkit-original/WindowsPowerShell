"""
XKit Core Domain
Hexagonal Architecture Core with Ports and Adapters
"""

from .application import XKitApplication
from .container import XKitContainer
from .ports import (
    ICommandService, IGitService, IAIService, IFilesystemService,
    IDisplayService, IConfigService, IContainerService, ITelegramService,
    IEventService, IPluginService, IMCPService
)

__all__ = [
    'XKitApplication',
    'XKitContainer',
    'ICommandService', 'IGitService', 'IAIService', 'IFilesystemService',
    'IDisplayService', 'IConfigService', 'IContainerService', 'ITelegramService',
    'IEventService', 'IPluginService', 'IMCPService'
]

__version__ = "3.0.0"