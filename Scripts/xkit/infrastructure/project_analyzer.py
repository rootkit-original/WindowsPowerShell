"""
Project analyzer implementation
"""
import re
from pathlib import Path
from typing import List, Optional
from ..domain.interfaces import IProjectAnalyzer, IFileSystemRepository
from ..domain.entities import ReadmeInfo, ProjectInfo


class ProjectAnalyzer(IProjectAnalyzer):
    """Project analysis implementation"""
    
    def __init__(self, file_system: IFileSystemRepository):
        self.file_system = file_system
        
        # Technology detection patterns
        self.tech_indicators = {
            'Python': ['requirements.txt', 'setup.py', 'pyproject.toml', 'Pipfile', '*.py'],
            'Node.js': ['package.json', 'package-lock.json', 'yarn.lock', 'node_modules'],
            'Docker': ['Dockerfile', 'docker-compose.yml', 'docker-compose.yaml', '.dockerignore'],
            'PowerShell': ['*.ps1', 'profile.ps1', 'Microsoft.PowerShell_profile.ps1'],
            'C#/.NET': ['*.csproj', '*.sln', 'global.json', 'appsettings.json'],
            'Java': ['pom.xml', 'build.gradle', '*.java', 'gradle.properties'],
            'Web': ['index.html', 'webpack.config.js', 'vite.config.js'],
            'TypeScript': ['tsconfig.json', '*.ts', '*.tsx'],
            'React': ['package.json'],  # Will be refined by package.json content
            'Git': ['.git', '.gitignore'],
        }
    
    def detect_technologies(self, project_path: Path) -> List[str]:
        """Detect technologies used in project"""
        detected = []
        
        for tech, patterns in self.tech_indicators.items():
            for pattern in patterns:
                if pattern.startswith('*.'):
                    # File extension pattern
                    ext = pattern[1:]
                    files = self.file_system.glob_files(project_path, f'**/*{ext}')
                    if files[:3]:  # Limit search to first 3 matches
                        detected.append(tech)
                        break
                else:
                    # Specific file pattern
                    if self.file_system.file_exists(project_path / pattern):
                        detected.append(tech)
                        break
        
        # Special detection for React (check package.json content)
        if 'Node.js' in detected:
            package_json_path = project_path / 'package.json'
            if self.file_system.file_exists(package_json_path):
                content = self.file_system.read_file(package_json_path)
                if content and ('react' in content.lower() or 'next' in content.lower()):
                    if 'React' not in detected:
                        detected.append('React')
        
        return detected
    
    def analyze_readme(self, project_path: Path) -> Optional[ReadmeInfo]:
        """Analyze README files"""
        readme_files = ['README.md', 'readme.md', 'README.txt', 'README', 'Readme.md']
        
        for readme_file in readme_files:
            readme_path = project_path / readme_file
            if self.file_system.file_exists(readme_path):
                content = self.file_system.read_file(readme_path)
                if content:
                    return self._parse_readme_content(readme_file, content)
        
        return None
    
    def _parse_readme_content(self, filename: str, content: str) -> ReadmeInfo:
        """Parse README content to extract information"""
        # Extract title (first line with #)
        title_match = re.search(r'^#\s*(.+)', content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else None
        
        # Extract first description (first paragraph after title)
        lines = content.split('\n')
        description = None
        
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('#') and not stripped.startswith('!') and not stripped.startswith('[!['):
                description = stripped
                break
        
        # Create content preview
        content_preview = content[:200] + '...' if len(content) > 200 else content
        
        return ReadmeInfo(
            file_name=filename,
            title=title,
            description=description,
            content_preview=content_preview
        )
    
    def get_project_info(self, current_path: Path) -> ProjectInfo:
        """Get basic project information"""
        technologies = self.detect_technologies(current_path)
        
        return ProjectInfo(
            name=current_path.name,
            path=current_path,
            type='standalone',
            technologies=technologies,
            relative_path='.'
        )