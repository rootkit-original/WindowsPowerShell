"""
Legacy Infrastructure Adapter
Adapter for integrating with existing XKit infrastructure services
"""
import logging
from typing import Dict, List, Optional, Any

from ...core.ports import (
    IGitService, IAIService, IDisplayService, IConfigService,
    IContainerService, ITelegramService
)
from ...core.ports.git_port import GitStatus, GitBranch, BranchType
from ...core.ports.ai_port import AIAnalysisResult, ErrorContext, AnalysisType
from ...core.ports.display_port import DisplayLevel
from ...core.ports.container_port import ContainerInfo, ContainerStatus
from ...core.ports.telegram_port import TelegramMessage, MessageType


class LegacyInfrastructureAdapter:
    """Adapter that wraps existing infrastructure services to implement ports"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._git_service = None
        self._ai_service = None
        self._display_service = None
        self._config_service = None
        self._container_service = None
        self._telegram_service = None
    
    def set_git_service(self, git_service: IGitService) -> None:
        """Set the Git service implementation"""
        self._git_service = git_service
    
    def set_ai_service(self, ai_service: IAIService) -> None:
        """Set the AI service implementation"""
        self._ai_service = ai_service
    
    def set_display_service(self, display_service: IDisplayService) -> None:
        """Set the display service implementation"""
        self._display_service = display_service
    
    def set_config_service(self, config_service: IConfigService) -> None:
        """Set the config service implementation"""
        self._config_service = config_service
    
    def set_container_service(self, container_service: IContainerService) -> None:
        """Set the container service implementation"""
        self._container_service = container_service
    
    def set_telegram_service(self, telegram_service: ITelegramService) -> None:
        """Set the Telegram service implementation"""
        self._telegram_service = telegram_service
    
    async def initialize_from_legacy_infrastructure(self) -> None:
        """Initialize adapters from existing infrastructure"""
        # This would import and wrap existing infrastructure services
        # from the xkit.infrastructure module
        try:
            from ...infrastructure import (
                git, ai_service, display, environment,
                container, telegram_service
            )
            
            # Wrap existing services with port implementations
            # This is where we would create wrapper classes that implement
            # the port interfaces using the existing infrastructure
            
            self.logger.info("Legacy infrastructure adapters initialized")
            
        except ImportError as e:
            self.logger.warning(f"Could not import legacy infrastructure: {e}")
    
    def get_git_service(self) -> Optional[IGitService]:
        """Get the Git service"""
        return self._git_service
    
    def get_ai_service(self) -> Optional[IAIService]:
        """Get the AI service"""
        return self._ai_service
    
    def get_display_service(self) -> Optional[IDisplayService]:
        """Get the display service"""
        return self._display_service
    
    def get_config_service(self) -> Optional[IConfigService]:
        """Get the config service"""
        return self._config_service
    
    def get_container_service(self) -> Optional[IContainerService]:
        """Get the container service"""
        return self._container_service
    
    def get_telegram_service(self) -> Optional[ITelegramService]:
        """Get the Telegram service"""
        return self._telegram_service


# Example wrapper class for existing Git service
class LegacyGitServiceWrapper(IGitService):
    """Wrapper for existing Git service to implement IGitService port"""
    
    def __init__(self, legacy_git_service):
        self.legacy_service = legacy_git_service
        self.logger = logging.getLogger(__name__)
    
    async def get_status(self, repo_path: Optional[str] = None) -> GitStatus:
        """Get current Git repository status"""
        # This would call the existing git service and convert the result
        # to match the GitStatus dataclass
        pass
    
    async def get_current_branch(self, repo_path: Optional[str] = None) -> str:
        """Get name of current branch"""
        # Implementation using legacy service
        pass
    
    # ... other methods would be implemented similarly