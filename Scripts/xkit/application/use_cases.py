"""
Application layer - Use cases and business logic orchestration
"""
from typing import Optional
from pathlib import Path
from ..domain import (
    DevelopmentContext, 
    ProjectInfo,
    XKitError,
    XPilotAnalysis,
    IFileSystemRepository,
    IGitRepository,
    IContainerRepository,
    IProjectAnalyzer,
    IDisplayService,
    IErrorHandler,
    IGitBranchManager,
    IXPilotAgent
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


class HandleErrorUseCase:
    """Use case for handling errors in the XKit system"""
    
    def __init__(
        self,
        error_handler: IErrorHandler,
        display_service: IDisplayService,
        git_branch_manager: IGitBranchManager,
        xpilot_agent: IXPilotAgent
    ):
        self.error_handler = error_handler
        self.display_service = display_service
        self.git_branch_manager = git_branch_manager
        self.xpilot_agent = xpilot_agent
    
    def execute(self, message: str, command: str = "", context: str = "") -> None:
        """Handle error with full XPilot resolution workflow"""
        # Create error instance
        error = self.error_handler.create_error(message, command, context)
        
        # Store error for tracking
        self.error_handler.store_error(error)
        
        # Show error details with emojis
        self.display_service.show_error(error)
        
        # Ask user for action
        user_choice = self.display_service.prompt_error_action()
        
        if user_choice.lower() in ['y', 'yes']:
            self._start_xpilot_resolution(error)
        elif user_choice.lower() in ['d', 'details']:
            self.display_service.show_error_details(error)
            # Recurse for another choice
            self.execute(message, command, context)
        elif user_choice.lower() in ['s', 'skip']:
            self.display_service.show_skip_message()
        else:
            self.display_service.show_ignore_message()
    
    def _start_xpilot_resolution(self, error: XKitError) -> None:
        """Start XPilot resolution process"""
        try:
            # Create error branch
            branch_name = self.git_branch_manager.create_error_branch(error)
            error.git_branch = branch_name
            
            # Commit error report
            self.git_branch_manager.commit_error_report(error, branch_name)
            
            # Analyze with XPilot
            analysis = self.xpilot_agent.analyze_error(error)
            
            # Show analysis results
            self.display_service.show_xpilot_analysis(error, analysis)
            
            # Apply auto-fix if available and user agrees
            if analysis.auto_fix_available:
                if self.display_service.confirm_auto_fix():
                    self._apply_auto_fix(error, analysis)
            
            # Ask if user wants to return to main branch
            if self.display_service.confirm_return_to_main():
                self.git_branch_manager.switch_to_previous_branch()
                
        except Exception as e:
            self.display_service.show_git_error(str(e))
            # Continue with analysis without git operations
            analysis = self.xpilot_agent.analyze_error(error)
            self.display_service.show_xpilot_analysis(error, analysis)
    
    def _apply_auto_fix(self, error: XKitError, analysis: XPilotAnalysis) -> None:
        """Apply automatic fix"""
        if analysis.auto_fix_script:
            # This would execute the fix script
            self.display_service.show_auto_fix_applied()


class ShowErrorDetailsUseCase:
    """Use case for showing detailed error information"""
    
    def __init__(self, error_handler: IErrorHandler, display_service: IDisplayService):
        self.error_handler = error_handler
        self.display_service = display_service
    
    def execute(self) -> None:
        """Show details of the last error"""
        error = self.error_handler.get_last_error()
        if error:
            self.display_service.show_error_details(error)
        else:
            self.display_service.show_no_error_message()


class RetryLastErrorUseCase:
    """Use case for retrying the last error resolution"""
    
    def __init__(self, handle_error_use_case: HandleErrorUseCase, error_handler: IErrorHandler):
        self.handle_error_use_case = handle_error_use_case
        self.error_handler = error_handler
    
    def execute(self) -> None:
        """Retry resolution of the last error"""
        error = self.error_handler.get_last_error()
        if error:
            self.handle_error_use_case.execute(error.message, error.command, error.context)
        else:
            print("ℹ️  No recent error to retry")