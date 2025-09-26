"""
Display service implementation
"""
from typing import Optional
from ..domain.interfaces import IDisplayService
from ..domain.entities import DevelopmentContext, XKitError, XPilotAnalysis
from .container import ContainerRepository


class ConsoleDisplayService(IDisplayService):
    """Console display implementation"""
    
    def __init__(self):
        self.container_repo = ContainerRepository()
    
    def show_welcome(self, context: DevelopmentContext) -> None:
        """Show welcome message based on context"""
        print("🚀 XKit - Ambiente de desenvolvimento ativo")
        print("=" * 50)
        
        if context.is_git_project:
            self._show_git_project_info(context)
        else:
            self._show_standalone_info(context)
        
        print()
        print("💡 Digite 'xkit-help' para ver comandos disponíveis")
        print("=" * 50)
    
    def _show_git_project_info(self, context: DevelopmentContext) -> None:
        """Show information for Git projects"""
        print(f"📁 Projeto: {context.project.name}")
        
        # README information
        if context.readme and context.readme.has_content:
            if context.readme.title:
                print(f"📖 {context.readme.title}")
            if context.readme.description:
                print(f"💭 {context.readme.description}")
        
        # Technologies
        if context.project.technologies:
            print(f"🛠️  Tecnologias: {', '.join(context.project.technologies)}")
        
        # Git status
        if context.git:
            print(f"🌿 {context.git.status_summary}")
        
        # Current location
        if context.project.relative_path != '.':
            print(f"📍 Subdiretório: {context.project.relative_path}")
        
        # Container info
        if context.has_containers:
            print(f"🐳 Container: {context.container.engine_type.title()} disponível")
    
    def _show_standalone_info(self, context: DevelopmentContext) -> None:
        """Show information for standalone directories"""
        print("📂 Diretório atual (sem controle Git)")
        
        if context.project.technologies:
            print(f"🛠️  Tecnologias detectadas: {', '.join(context.project.technologies)}")
        
        if context.has_containers:
            print(f"🐳 Container: {context.container.engine_type.title()} disponível")
    
    def show_help(self, context: DevelopmentContext) -> None:
        """Show help based on context"""
        print("🔧 XKit - Comandos disponíveis:")
        print()
        
        # Basic commands
        print("📋 Comandos básicos:")
        print("  xkit-help     - Mostra esta ajuda")
        print("  xkit-status   - Status detalhado do projeto atual")
        print("  xkit-info     - Informações completas do projeto")
        print("  xkit-reload   - Recarrega configuração do PowerShell")
        print()
        
        # Git commands
        if context.is_git_project:
            print("🌿 Comandos Git:")
            print("  git status    - Status do repositório")
            print("  git branch    - Listar/gerenciar branches")
            print("  git log       - Histórico de commits")
            print()
        
        # Container commands
        if context.has_containers:
            self._show_container_help(context)
        
        # Technology-specific commands
        self._show_tech_specific_help(context)
    
    def _show_container_help(self, context: DevelopmentContext) -> None:
        """Show container-specific help"""
        engine = context.container.engine_type
        print(f"🐳 Comandos {engine.title()}:")
        
        commands = self.container_repo.get_container_commands(context.container)
        for cmd, description in commands.items():
            if engine == 'podman':
                print(f"  {engine} {cmd.replace('-', ' ')}  - {description}")
            else:
                print(f"  {engine} {cmd}      - {description}")
        print()
    
    def _show_tech_specific_help(self, context: DevelopmentContext) -> None:
        """Show technology-specific help"""
        techs = context.project.technologies
        
        if 'Python' in techs:
            print("🐍 Comandos Python:")
            print("  python -m pip install -r requirements.txt")
            print("  python -m venv venv")
            print("  python -m pytest")
            print()
        
        if 'Node.js' in techs:
            print("📦 Comandos Node.js:")
            print("  npm install   - Instalar dependências")
            print("  npm run dev   - Executar em desenvolvimento")
            print("  npm test      - Executar testes")
            print()
        
        if 'Docker' in techs:
            engine = context.container.engine_type if context.has_containers else 'docker'
            print(f"🐋 Comandos Docker (usando {engine}):")
            print(f"  {engine}-compose up    - Subir serviços")
            print(f"  {engine}-compose down  - Parar serviços")
            print(f"  {engine} build .       - Construir imagem")
            print()
    
    def show_status(self, context: DevelopmentContext) -> None:
        """Show detailed status"""
        print("📊 Status detalhado do XKit:")
        print(f"📁 Diretório atual: {context.project.path}")
        print(f"📂 Tipo de projeto: {context.project.type}")
        
        if context.is_git_project:
            print(f"📦 Repositório Git: {context.git.root_path}")
            print(f"🌿 Branch atual: {context.git.current_branch}")
            print(f"📝 Mudanças pendentes: {context.git.changes_count}")
            
            if context.project.relative_path != '.':
                print(f"📍 Localização: {context.project.relative_path}")
        
        if context.project.technologies:
            print(f"🛠️  Tecnologias detectadas: {', '.join(context.project.technologies)}")
        
        if context.readme:
            print(f"📖 README encontrado: {context.readme.file_name}")
            if context.readme.title:
                print(f"   Título: {context.readme.title}")
        
        if context.has_containers:
            print(f"🐳 Container engine: {context.container.engine_type} ({context.container.engine_path})")
        else:
            print("🐳 Nenhum container engine detectado")
    
    # Error handling display methods
    def show_error(self, error: XKitError) -> None:
        """Show error information with emojis"""
        print(f"\n{error.emoji_prefix} XKit Error Detected (#{error.id})")
        print("─" * 50)
        print(f"🚨 Error: {error.message}")
        
        if error.command:
            print(f"⚡ Command: {error.command}")
        
        if error.context:
            print(f"📍 Context: {error.context}")
        
        print(f"🕒 Time: {error.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📊 Severity: {error.severity.value.upper()}")
        print("─" * 50)
    
    def prompt_error_action(self) -> str:
        """Prompt user for error action"""
        return input("\n🤖 Want to stop and resolve with @xpilot? (y/N/s=skip/d=details): ").strip()
    
    def show_error_details(self, error: XKitError) -> None:
        """Show detailed error information"""
        print(f"\n📊 Detailed Error Information")
        print("═" * 40)
        print(f"Error ID: #{error.id}")
        print(f"Type: {error.error_type.value}")
        print(f"Severity: {error.severity.value}")
        print(f"Timestamp: {error.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Message: {error.message}")
        print(f"Command: {error.command or 'N/A'}")
        print(f"Context: {error.context or 'N/A'}")
        
        if error.git_branch:
            print(f"Git Branch: {error.git_branch}")
        
        if error.resolution_suggestions:
            print("\n💡 Suggestions:")
            for i, suggestion in enumerate(error.resolution_suggestions, 1):
                print(f"  {i}. {suggestion}")
    
    def show_skip_message(self) -> None:
        """Show skip message"""
        print("⏭️  Error skipped. Continuing...")
    
    def show_ignore_message(self) -> None:
        """Show ignore message"""
        print("❌ Error ignored. Use 'xerr' to review later.")
    
    def show_xpilot_analysis(self, error: XKitError, analysis: XPilotAnalysis) -> None:
        """Show XPilot analysis results"""
        print(f"\n🤖 @xpilot Analysis Starting...")
        print("─" * 40)
        print(f"🔍 Analysis: {analysis.summary}")
        
        if analysis.suggestions:
            print(f"\n💡 Suggested Actions:")
            for i, suggestion in enumerate(analysis.suggestions, 1):
                print(f"  • {suggestion}")
        
        print(f"\n{analysis.confidence_emoji} Confidence: {analysis.confidence:.0%}")
        
        if analysis.auto_fix_available:
            print("🔧 Auto-fix available!")
    
    def confirm_auto_fix(self) -> bool:
        """Ask user to confirm auto-fix"""
        response = input("\n🔧 Apply automatic fix? (y/N): ").strip().lower()
        return response in ['y', 'yes']
    
    def show_auto_fix_applied(self) -> None:
        """Show auto-fix applied message"""
        print("✅ Automatic fix applied successfully!")
    
    def confirm_return_to_main(self) -> bool:
        """Ask user to return to main branch"""
        response = input("\n🔄 Resolution complete. Return to main branch? (y/N): ").strip().lower()
        return response in ['y', 'yes']
    
    def show_git_error(self, error_message: str) -> None:
        """Show git operation error"""
        print(f"❌ Git operation failed: {error_message}")
        print("🔄 Continuing with analysis...")
    
    def show_no_error_message(self) -> None:
        """Show no error available message"""
        print("ℹ️  No error information available")
    
    def show_help(self, context: DevelopmentContext = None) -> None:
        """Show comprehensive help with emojis"""
        print("\n🎨 Oh My XKit v2.1.0 - Command Reference")
        print("═" * 60)
        
        print("\n📁 Git Commands:")
        print("  xstatus    - git status")
        print("  xadd       - git add")
        print("  xcommit    - git commit")
        print("  xpush      - git push")
        print("  xlog       - git log")
        print("  xbranch    - git branch")
        print("  xcheckout  - git checkout")
        
        print("\n🐳 Container Commands:")
        print("  xpodman      - podman")
        print("  xcontainers  - podman ps")
        print("  ximages      - podman images")
        
        print("\n🤖 AI & Telegram:")
        print("  question [text] - Ask AI assistant")
        print("  tg [message]    - Send Telegram message")
        
        print("\n🛡️  Error Handling:")
        print("  xerr           - Show last error details")
        print("  xfix           - Retry last error resolution")
        print("  xtest-error    - Test error handler")
        
        print("\n🔧 Enhanced Commands:")
        print("  xgit    - Git with error handling")
        print("  xpython - Python with error handling")
        print("  xdocker - Docker with error handling")
        print("  xnpm    - NPM with error handling")
        
        print("\n💡 System:")
        print("  xkit-help      - Show this help")
        print("  xkit-version   - Show version info")
        print("  xkit-reload    - Reload framework")
        print()