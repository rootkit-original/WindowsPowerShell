"""
Domain interfaces - Contracts for data access and external services
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Dict
from pathlib import Path
from .entities import (
    GitInfo, ReadmeInfo, ProjectInfo, ContainerInfo, DevelopmentContext,
    XKitError, XPilotAnalysis, ErrorType, ErrorSeverity
)


class IFileSystemRepository(ABC):
    """Interface for file system operations"""
    
    @abstractmethod
    def find_git_root(self, start_path: Path) -> Optional[Path]:
        """Find the root of a git repository"""
        pass
    
    @abstractmethod
    def read_file(self, file_path: Path) -> Optional[str]:
        """Read file content"""
        pass
    
    @abstractmethod
    def file_exists(self, file_path: Path) -> bool:
        """Check if file exists"""
        pass
    
    @abstractmethod
    def glob_files(self, path: Path, pattern: str) -> List[Path]:
        """Find files matching pattern"""
        pass


class IGitRepository(ABC):
    """Interface for Git operations"""
    
    @abstractmethod
    def get_git_info(self, git_root: Path) -> Optional[GitInfo]:
        """Get Git repository information"""
        pass
    
    @abstractmethod
    def get_current_branch(self, git_root: Path) -> str:
        """Get current branch name"""
        pass
    
    @abstractmethod
    def get_changes_count(self, git_root: Path) -> int:
        """Get number of uncommitted changes"""
        pass


class IContainerRepository(ABC):
    """Interface for container operations"""
    
    @abstractmethod
    def detect_container_engine(self) -> Optional[ContainerInfo]:
        """Detect available container engine"""
        pass
    
    @abstractmethod
    def is_engine_available(self, engine_path: Path) -> bool:
        """Check if container engine is available"""
        pass


class IProjectAnalyzer(ABC):
    """Interface for project analysis"""
    
    @abstractmethod
    def detect_technologies(self, project_path: Path) -> List[str]:
        """Detect technologies used in project"""
        pass
    
    @abstractmethod
    def analyze_readme(self, project_path: Path) -> Optional[ReadmeInfo]:
        """Analyze README files"""
        pass
    
    @abstractmethod
    def get_project_info(self, current_path: Path) -> ProjectInfo:
        """Get basic project information"""
        pass


class ICommandExecutor(ABC):
    """Interface for command execution"""
    
    @abstractmethod
    def execute_command(self, command: List[str], cwd: Optional[Path] = None) -> tuple[str, int]:
        """Execute shell command"""
        pass
    
    @abstractmethod
    def has_command(self, command: str) -> bool:
        """Check if command is available"""
        pass


class IDisplayService(ABC):
    """Interface for display operations"""
    
    @abstractmethod
    def show_welcome(self, context: 'DevelopmentContext') -> None:
        """Show welcome message"""
        pass
    
    @abstractmethod
    def show_help(self, context: 'DevelopmentContext') -> None:
        """Show help information"""
        pass
    
    @abstractmethod
    def show_status(self, context: 'DevelopmentContext') -> None:
        """Show detailed status"""
        pass


class IErrorHandler(ABC):
    """Interface for error handling operations"""
    
    @abstractmethod
    def create_error(self, message: str, command: str = "", context: str = "") -> XKitError:
        """Create a new error instance"""
        pass
    
    @abstractmethod
    def analyze_error(self, error: XKitError) -> XPilotAnalysis:
        """Analyze error and provide resolution suggestions"""
        pass
    
    @abstractmethod
    def store_error(self, error: XKitError) -> None:
        """Store error for tracking"""
        pass
    
    @abstractmethod
    def get_last_error(self) -> Optional[XKitError]:
        """Get the most recent error"""
        pass
    
    @abstractmethod
    def get_error_count(self) -> int:
        """Get total error count"""
        pass


class IGitBranchManager(ABC):
    """Interface for Git branch operations"""
    
    @abstractmethod
    def create_error_branch(self, error: XKitError) -> str:
        """Create a new branch for error resolution"""
        pass
    
    @abstractmethod
    def commit_error_report(self, error: XKitError, branch_name: str) -> bool:
        """Commit error report to branch"""
        pass
    
    @abstractmethod
    def switch_to_previous_branch(self) -> bool:
        """Switch back to previous branch"""
        pass


class IXPilotAgent(ABC):
    """Interface for XPilot AI agent"""
    
    @abstractmethod
    def analyze_error(self, error: XKitError) -> XPilotAnalysis:
        """Analyze error and provide intelligent suggestions"""
        pass
    
    @abstractmethod
    def generate_auto_fix(self, error: XKitError) -> Optional[str]:
        """Generate automatic fix script if possible"""
        pass