"""
Display service implementation for XKit v3.0
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
        print("🚀 XKit v3.0 - Hybrid MCP Architecture")
        print("=" * 50)
        
        if context.is_git_project:
            self._show_git_project_info(context)
        else:
            self._show_standalone_info(context)
            
        print()
        print("💡 Digite 'xkit-help' para ver comandos disponíveis")
        print()

    def _show_git_project_info(self, context: DevelopmentContext) -> None:
        """Show git project specific info"""
        print(f"📂 Projeto: {context.current_directory}")
        if hasattr(context, 'branch_name') and context.branch_name:
            print(f"🌿 Branch: {context.branch_name}")
        
        # Container info
        container_info = self.container_repo.detect_container_files(context.current_directory)
        if container_info:
            if container_info.get('dockerfile_exists'):
                print("🐳 Docker detectado")
            if container_info.get('compose_exists'):
                print("🐙 Docker Compose detectado")
            if container_info.get('podman_exists'):
                print("🦭 Podman detectado")
        
        # Tech stack
        if hasattr(context, 'tech_stack') and context.tech_stack:
            print("🛠️  Stack:", ", ".join(context.tech_stack))

    def _show_standalone_info(self, context: DevelopmentContext) -> None:
        """Show standalone directory info"""
        print(f"📁 Diretório: {context.current_directory}")
        print("ℹ️  Não é um projeto Git")
        
        container_info = self.container_repo.detect_container_files(context.current_directory)
        if container_info and any(container_info.values()):
            print("🐳 Containers detectados neste diretório")

    def show_help(self, context: DevelopmentContext = None) -> None:
        """Show help based on context"""
        print("📖 XKit v3.0 - Comandos Disponíveis")
        print("=" * 40)
        
        # V3.0 commands
        print("\n🎯 XKit v3.0:")
        print("  xkit-status      - Status do sistema híbrido")
        print("  xkit-help        - Esta ajuda")
        print("  mcp-status       - Status do MCP")
        print("  plugin-list      - Listar plugins")
        print("  events-status    - Status do sistema de eventos")
        
        # Legacy commands  
        print("\n🌿 Git:")
        print("  git-status       - Status detalhado do Git")
        print("  quick-commit     - Commit rápido com mensagem")
        print("  smart-branch     - Criar branch inteligente")
        
        # Container commands
        print("\n🐳 Containers:")
        print("  docker-status    - Status dos containers")
        print("  compose-up       - Subir containers")
        print("  compose-down     - Parar containers")
        
        print("\n💡 Use 'xpilot' quando encontrar erros - o AI vai ajudar!")

    def show_status(self, context: DevelopmentContext) -> None:
        """Show current status"""
        print("📊 Status do XKit v3.0")
        print("=" * 30)
        
        print(f"📂 Diretório: {context.current_directory}")
        print("🏗️  Arquitetura: Híbrida MCP")
        
        if context.is_git_project:
            print("🌿 Projeto Git: Sim")
            if hasattr(context, 'branch_name') and context.branch_name:
                print(f"   Branch atual: {context.branch_name}")
        else:
            print("🌿 Projeto Git: Não")
        
        print("\n💡 Sistema v3.0 operacional!")

    def show_error(self, error: XKitError) -> None:
        """Show error information"""
        print("❌ Erro Detectado")
        print("=" * 30)
        print(f"🔍 Comando: {error.command}")
        print(f"📍 Contexto: {error.context}")
        print(f"💬 Mensagem: {error.message}")
        
        if hasattr(error, 'error_code') and error.error_code:
            print(f"🔢 Código: {error.error_code}")
        
        if hasattr(error, 'suggestions') and error.suggestions:
            print("\n💡 Sugestões:")
            for i, suggestion in enumerate(error.suggestions, 1):
                print(f"   {i}. {suggestion}")
        
        print()


# Alias for v3.0 compatibility
DisplayService = ConsoleDisplayService
