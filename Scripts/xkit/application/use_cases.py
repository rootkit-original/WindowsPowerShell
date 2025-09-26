"""
Application layer - Use cases and business logic orchestration
"""
from typing import Optional
from pathlib import Path
from ..domain import (
    DevelopmentContext, 
    ProjectInfo,
    IFileSystemRepository,
    IGitRepository,
    IContainerRepository,
    IProjectAnalyzer,
    IDisplayService
)


class AnalyzeProjectUseCase:
    """Use case for analyzing the current development context"""
    
    def __init__(
        self,
        file_system: IFileSystemRepository,
        git_repo: IGitRepository,
        container_repo: IContainerRepository,
        project_analyzer: IProjectAnalyzer
    ):
        self.file_system = file_system
        self.git_repo = git_repo
        self.container_repo = container_repo
        self.project_analyzer = project_analyzer

    def execute(self, current_path: Path) -> DevelopmentContext:
        """Analyze current development context"""
        
        # Get basic project info
        project_info = self.project_analyzer.get_project_info(current_path)
        
        # Try to find git repository
        git_root = self.file_system.find_git_root(current_path)
        git_info = None
        if git_root:
            git_info = self.git_repo.get_git_info(git_root)
            # Update project info for git projects
            project_info = ProjectInfo(
                name=git_root.name,
                path=git_root,
                type='git_project',
                technologies=self.project_analyzer.detect_technologies(git_root),
                relative_path=str(current_path.relative_to(git_root)) if current_path != git_root else '.'
            )
        
        # Analyze README
        readme_info = self.project_analyzer.analyze_readme(
            git_root if git_root else current_path
        )
        
        # Detect container engine
        container_info = self.container_repo.detect_container_engine()
        
        return DevelopmentContext(
            project=project_info,
            git=git_info,
            readme=readme_info,
            container=container_info
        )


class ShowWelcomeUseCase:
    """Use case for showing welcome message"""
    
    def __init__(self, display_service: IDisplayService):
        self.display_service = display_service
    
    def execute(self, context: DevelopmentContext) -> None:
        """Show welcome message based on context"""
        self.display_service.show_welcome(context)


class ShowHelpUseCase:
    """Use case for showing help information"""
    
    def __init__(self, display_service: IDisplayService):
        self.display_service = display_service
    
    def execute(self, context: DevelopmentContext) -> None:
        """Show help based on context"""
        self.display_service.show_help(context)


class ShowStatusUseCase:
    """Use case for showing detailed status"""
    
    def __init__(self, display_service: IDisplayService):
        self.display_service = display_service
    
    def execute(self, context: DevelopmentContext) -> None:
        """Show detailed status"""
        self.display_service.show_status(context)


class ShowAISuggestionsUseCase:
    """Use case for showing AI suggestions"""
    
    def __init__(self, display_service: IDisplayService):
        self.display_service = display_service
    
    def execute(self, context: DevelopmentContext) -> None:
        """Show AI suggestions"""
        if hasattr(self.display_service, 'show_ai_suggestions'):
            self.display_service.show_ai_suggestions(context)
        else:
            print("❌ Serviço de AI não disponível")


class AskAISolutionUseCase:
    """Use case for asking AI solutions"""
    
    def __init__(self, display_service: IDisplayService):
        self.display_service = display_service
    
    def execute(self, problem: str, context: DevelopmentContext) -> None:
        """Ask AI for solution"""
        if hasattr(self.display_service, 'ask_ai_solution'):
            self.display_service.ask_ai_solution(problem, context)
        else:
            print("❌ Serviço de AI não disponível")


class ExecuteContainerCommandUseCase:
    """Use case for executing container commands"""
    
    def __init__(self, container_repo: IContainerRepository):
        self.container_repo = container_repo
        
    def execute(self, command: str, args: list = None) -> bool:
        """Execute container command if engine is available"""
        container_info = self.container_repo.detect_container_engine()
        if not container_info or not container_info.is_available:
            return False
            
        # This would be implemented to execute the actual command
        # For now, just return success if container is available
        return True