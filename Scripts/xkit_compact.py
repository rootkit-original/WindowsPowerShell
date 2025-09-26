#!/usr/bin/env python3
"""
XKit v2.1 - Kit de desenvolvimento inteligente com AI e interface compacta
Sistema contextual estilo oh-my-zsh com Gemini AI e Telegram
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório do módulo xkit ao path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

try:
    from xkit.domain import DevelopmentContext
    from xkit.application import (
        AnalyzeProjectUseCase,
        ShowWelcomeUseCase,
        ShowHelpUseCase,
        ShowStatusUseCase,
        ShowAISuggestionsUseCase,
        AskAISolutionUseCase
    )
    from xkit.infrastructure import (
        FileSystemRepository,
        GitRepository,
        ContainerRepository,
        ProjectAnalyzer,
        CompactDisplayService
    )
except ImportError as e:
    print(f"❌ Erro ao importar módulos do XKit: {e}")
    print("🚀 XKit está rodando em modo básico!")
    sys.exit(0)


class XKitCompactApplication:
    """Main application class com interface compacta"""
    
    def __init__(self):
        # Set environment variables if not already set
        self._set_default_env_vars()
        
        # Infrastructure layer
        self.file_system = FileSystemRepository()
        self.git_repo = GitRepository()
        self.container_repo = ContainerRepository()
        self.project_analyzer = ProjectAnalyzer(self.file_system)
        self.display_service = CompactDisplayService()
        
        # Application layer (use cases)
        self.analyze_project = AnalyzeProjectUseCase(
            self.file_system,
            self.git_repo,
            self.container_repo,
            self.project_analyzer
        )
        self.show_welcome = ShowWelcomeUseCase(self.display_service)
        self.show_help = ShowHelpUseCase(self.display_service)
        self.show_status = ShowStatusUseCase(self.display_service)
        self.show_ai_suggestions = ShowAISuggestionsUseCase(self.display_service)
        self.ask_ai_solution = AskAISolutionUseCase(self.display_service)
        
        # Current context
        self.context: DevelopmentContext = None
    
    def _set_default_env_vars(self):
        """Define variáveis de ambiente padrão se não existirem"""
        defaults = {
            'GEMINI_API_KEY': 'AIzaSyCvzBo-iK-KBdwedZYSHyoHcMzsYqEArC4',
            'TELEGRAM_TOKEN': '7261193755:AAH5AmzbRwT0eS77FksbBUSt_V6r3pn1iF0',
            'ADMIN_ID': '7335391186'
        }
        
        for key, value in defaults.items():
            if not os.getenv(key):
                os.environ[key] = value
    
    def initialize(self) -> None:
        """Initialize the application by analyzing current context"""
        current_path = Path.cwd()
        self.context = self.analyze_project.execute(current_path)
    
    def run_command(self, command: str, *args) -> None:
        """Execute a command"""
        if not self.context:
            self.initialize()
        
        command = command.lower()
        
        if command in ['help', '--help', '-h']:
            self.show_help.execute(self.context)
        elif command == 'status':
            self.show_status.execute(self.context)
        elif command == 'info':
            self.show_welcome.execute(self.context)
        elif command == 'ai':
            self.show_ai_suggestions.execute(self.context)
        elif command == 'solve' and args:
            problem = ' '.join(args)
            self.ask_ai_solution.execute(problem, self.context)
        else:
            print(f"❌ Comando desconhecido: {command}")
            print("💡 Use 'python xkit_compact.py help' para ver comandos")
    
    def run_welcome(self) -> None:
        """Run welcome message (default mode) - compact style"""
        if not self.context:
            self.initialize()
        self.show_welcome.execute(self.context)


def main():
    """Main entry point"""
    app = XKitCompactApplication()
    
    if len(sys.argv) > 1:
        # Command mode
        command = sys.argv[1]
        args = sys.argv[2:] if len(sys.argv) > 2 else []
        app.run_command(command, *args)
    else:
        # Compact welcome mode (default)
        app.run_welcome()


if __name__ == "__main__":
    main()