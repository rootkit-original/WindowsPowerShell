"""
Domain layer - Core business logic and entities
"""
from .entities import (
    ProjectInfo,
    GitInfo, 
    ReadmeInfo,
    ContainerInfo,
    DevelopmentContext,
    XKitError,
    XPilotAnalysis,
    ErrorSeverity,
    ErrorType
)

from .interfaces import (
    IFileSystemRepository,
    IGitRepository,
    IContainerRepository,
    IProjectAnalyzer,
    ICommandExecutor,
    IDisplayService,
    IErrorHandler,
    IGitBranchManager,
    IXPilotAgent
)

__all__ = [
    'ProjectInfo',
    'GitInfo',
    'ReadmeInfo', 
    'ContainerInfo',
    'DevelopmentContext',
    'IFileSystemRepository',
    'IGitRepository',
    'IContainerRepository',
    'IProjectAnalyzer',
    'ICommandExecutor',
    'IDisplayService'
]