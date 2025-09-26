"""
Git repository implementation
"""
import subprocess
from pathlib import Path
from typing import Optional
from ..domain.interfaces import IGitRepository
from ..domain.entities import GitInfo


class GitRepository(IGitRepository):
    """Git operations implementation"""
    
    def get_git_info(self, git_root: Path) -> Optional[GitInfo]:
        """Get Git repository information"""
        try:
            branch = self.get_current_branch(git_root)
            changes_count = self.get_changes_count(git_root)
            is_clean = changes_count == 0
            
            return GitInfo(
                root_path=git_root,
                current_branch=branch,
                changes_count=changes_count,
                is_clean=is_clean
            )
        except Exception:
            return None
    
    def get_current_branch(self, git_root: Path) -> str:
        """Get current branch name"""
        try:
            result = subprocess.run(
                ['git', 'branch', '--show-current'],
                capture_output=True,
                text=True,
                cwd=git_root
            )
            return result.stdout.strip() if result.returncode == 0 else 'unknown'
        except Exception:
            return 'unknown'
    
    def get_changes_count(self, git_root: Path) -> int:
        """Get number of uncommitted changes"""
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True,
                text=True,
                cwd=git_root
            )
            if result.returncode == 0 and result.stdout.strip():
                return len(result.stdout.strip().split('\n'))
            return 0
        except Exception:
            return 0