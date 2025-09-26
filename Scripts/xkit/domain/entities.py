"""
Domain entities - Core business objects
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from pathlib import Path
from datetime import datetime
from enum import Enum


class ErrorSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium" 
    HIGH = "high"
    CRITICAL = "critical"


class ErrorType(Enum):
    COMMAND_NOT_FOUND = "command_not_found"
    SYNTAX_ERROR = "syntax_error"
    ACCESS_DENIED = "access_denied"
    FILE_NOT_FOUND = "file_not_found"
    GENERIC = "generic"


@dataclass
class XKitError:
    """Represents an error in the XKit system"""
    id: int
    message: str
    command: str = ""
    context: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    error_type: ErrorType = ErrorType.GENERIC
    severity: ErrorSeverity = ErrorSeverity.MEDIUM
    resolution_suggestions: List[str] = field(default_factory=list)
    auto_fix_available: bool = False
    auto_fix_script: Optional[str] = None
    git_branch: Optional[str] = None
    
    @property
    def emoji_prefix(self) -> str:
        """Get emoji based on error type"""
        emoji_map = {
            ErrorType.COMMAND_NOT_FOUND: "🔍",
            ErrorType.SYNTAX_ERROR: "📝",
            ErrorType.ACCESS_DENIED: "🔒", 
            ErrorType.FILE_NOT_FOUND: "📁",
            ErrorType.GENERIC: "⚠️"
        }
        return emoji_map.get(self.error_type, "❌")
    
    @property
    def severity_color(self) -> str:
        """Get color based on severity"""
        color_map = {
            ErrorSeverity.LOW: "yellow",
            ErrorSeverity.MEDIUM: "red",
            ErrorSeverity.HIGH: "bright_red",
            ErrorSeverity.CRITICAL: "red on white"
        }
        return color_map.get(self.severity, "red")


@dataclass
class XPilotAnalysis:
    """Analysis result from XPilot agent"""
    summary: str
    suggestions: List[str] = field(default_factory=list)
    auto_fix_available: bool = False
    auto_fix_script: Optional[str] = None
    confidence: float = 0.0  # 0-1 confidence score
    
    @property
    def confidence_emoji(self) -> str:
        if self.confidence >= 0.9:
            return "🎯"
        elif self.confidence >= 0.7:
            return "✅"
        elif self.confidence >= 0.5:
            return "🤔"
        else:
            return "❓"


@dataclass
class ProjectInfo:
    """Core project information"""
    name: str
    path: Path
    type: str  # 'git_project' or 'standalone'
    technologies: List[str]
    relative_path: str = '.'


@dataclass
class GitInfo:
    """Git repository information"""
    root_path: Path
    current_branch: str
    changes_count: int
    is_clean: bool
    
    @property
    def status_summary(self) -> str:
        status = f"Branch: {self.current_branch}"
        if not self.is_clean:
            status += f" ({self.changes_count} mudanças)"
        return status


@dataclass
class ReadmeInfo:
    """README file information"""
    file_name: str
    title: Optional[str]
    description: Optional[str]
    content_preview: str
    
    @property
    def has_content(self) -> bool:
        return bool(self.title or self.description)


@dataclass
class ContainerInfo:
    """Container engine information"""
    engine_type: str  # 'podman', 'docker'
    engine_path: Path
    is_available: bool
    has_compose: bool = False
    
    def get_command(self, cmd: str, args: List[str] = None) -> List[str]:
        """Build container command"""
        command = [str(self.engine_path), cmd]
        if args:
            command.extend(args)
        return command
    
    def get_compose_command(self, cmd: str, args: List[str] = None) -> List[str]:
        """Build compose command"""
        if not self.has_compose:
            return []
        
        if self.engine_type == 'podman':
            command = ['podman-compose', cmd]
        else:
            command = ['docker', 'compose', cmd]
        
        if args:
            command.extend(args)
        return command


@dataclass
class DevelopmentContext:
    """Complete development context"""
    project: ProjectInfo
    git: Optional[GitInfo] = None
    readme: Optional[ReadmeInfo] = None
    container: Optional[ContainerInfo] = None
    
    @property
    def is_git_project(self) -> bool:
        return self.project.type == 'git_project' and self.git is not None
    
    @property
    def has_containers(self) -> bool:
        return self.container is not None and self.container.is_available
    
    @property
    def display_name(self) -> str:
        """Get the best display name for the project"""
        if self.readme and self.readme.title:
            return self.readme.title
        return self.project.name