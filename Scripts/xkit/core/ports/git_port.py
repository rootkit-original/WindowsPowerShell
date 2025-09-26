"""
Git Service Port
Interface for Git operations and branch management
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class BranchType(Enum):
    """Git branch types"""
    FEATURE = "feature"
    BUGFIX = "bugfix"
    HOTFIX = "hotfix"
    RELEASE = "release"
    ERROR = "error"
    EXPERIMENT = "experiment"


@dataclass
class GitStatus:
    """Git repository status"""
    current_branch: str
    is_clean: bool
    staged_files: List[str]
    unstaged_files: List[str]
    untracked_files: List[str]
    ahead_behind: Tuple[int, int]  # (ahead, behind)
    last_commit: Optional[str] = None


@dataclass
class GitBranch:
    """Git branch information"""
    name: str
    is_current: bool
    is_remote: bool
    last_commit: Optional[str] = None
    ahead_behind: Optional[Tuple[int, int]] = None


class IGitService(ABC):
    """Port for Git operations"""
    
    @abstractmethod
    async def get_status(self, repo_path: Optional[str] = None) -> GitStatus:
        """Get current Git repository status"""
        pass
    
    @abstractmethod
    async def get_current_branch(self, repo_path: Optional[str] = None) -> str:
        """Get name of current branch"""
        pass
    
    @abstractmethod
    async def list_branches(self, repo_path: Optional[str] = None, 
                          include_remote: bool = True) -> List[GitBranch]:
        """List all branches"""
        pass
    
    @abstractmethod
    async def create_branch(self, branch_name: str, base_branch: Optional[str] = None,
                          branch_type: BranchType = BranchType.FEATURE,
                          repo_path: Optional[str] = None) -> bool:
        """Create a new branch"""
        pass
    
    @abstractmethod
    async def checkout_branch(self, branch_name: str, 
                            repo_path: Optional[str] = None) -> bool:
        """Checkout a branch"""
        pass
    
    @abstractmethod
    async def commit_changes(self, message: str, files: List[str] = None,
                           repo_path: Optional[str] = None) -> bool:
        """Commit changes"""
        pass
    
    @abstractmethod
    async def push_branch(self, branch_name: Optional[str] = None,
                        remote: str = "origin", 
                        repo_path: Optional[str] = None) -> bool:
        """Push branch to remote"""
        pass
    
    @abstractmethod
    async def pull_changes(self, branch_name: Optional[str] = None,
                         remote: str = "origin",
                         repo_path: Optional[str] = None) -> bool:
        """Pull changes from remote"""
        pass
    
    @abstractmethod
    async def get_commit_info(self, commit_hash: str,
                            repo_path: Optional[str] = None) -> Dict[str, str]:
        """Get information about a specific commit"""
        pass
    
    @abstractmethod
    def generate_branch_name(self, branch_type: BranchType, 
                           description: str) -> str:
        """Generate standardized branch name"""
        pass
    
    @abstractmethod
    async def is_git_repository(self, path: Optional[str] = None) -> bool:
        """Check if path is a Git repository"""
        pass