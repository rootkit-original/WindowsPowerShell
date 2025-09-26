"""
File system repository implementation
"""
import os
from pathlib import Path
from typing import Optional, List
from ..domain.interfaces import IFileSystemRepository


class FileSystemRepository(IFileSystemRepository):
    """File system operations implementation"""
    
    def find_git_root(self, start_path: Path) -> Optional[Path]:
        """Find the root of a git repository"""
        current = Path(start_path).resolve()
        while current.parent != current:
            if (current / '.git').exists():
                return current
            current = current.parent
        return None
    
    def read_file(self, file_path: Path) -> Optional[str]:
        """Read file content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            return None
    
    def file_exists(self, file_path: Path) -> bool:
        """Check if file exists"""
        return file_path.exists()
    
    def glob_files(self, path: Path, pattern: str) -> List[Path]:
        """Find files matching pattern"""
        try:
            return list(path.glob(pattern))
        except Exception:
            return []