"""
Domain entities - Core business objects
"""
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from pathlib import Path


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