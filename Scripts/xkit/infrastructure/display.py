"""
Display service implementation
"""
from ..domain.interfaces import IDisplayService
from ..domain.entities import DevelopmentContext
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