"""
Compact Display Service - Interface compacta similar ao oh-my-zsh
"""
from ..domain.interfaces import IDisplayService
from ..domain.entities import DevelopmentContext
from .ai_service import GeminiAIService
from .telegram_service import TelegramService
from .environment import EnvironmentDetector


class CompactDisplayService(IDisplayService):
    """Display service compacto e intuitivo"""
    
    def __init__(self):
        self.ai_service = GeminiAIService()
        self.telegram_service = TelegramService()
        self.env_detector = EnvironmentDetector()
    
    def show_welcome(self, context: DevelopmentContext) -> None:
        """Mostra boas-vindas compactas"""
        env_info = self.env_detector.detect()
        
        # Header compacto
        self._print_compact_header(context, env_info)
        
        # Detecta e reporta anomalias
        self._check_and_report_anomalies(context)
        
        # Sugestões AI (se disponível)
        self._show_ai_suggestions(context)
    
    def _print_compact_header(self, context: DevelopmentContext, env_info) -> None:
        """Imprime cabeçalho compacto"""
        # Linha principal - estilo oh-my-zsh
        line_parts = []
        
        # Environment icon
        line_parts.append(f"{env_info.icon}")
        
        # Project info
        if context.is_git_project:
            # Git project format: 📁project-name 🌿branch-name status
            git_status = "✓" if context.git.is_clean else f"±{context.git.changes_count}"
            line_parts.append(f"📁{context.project.name}")
            line_parts.append(f"🌿{context.git.current_branch} {git_status}")
        else:
            # Non-git format: 📂folder-name
            line_parts.append(f"📂{context.project.name}")
        
        # Container status
        if context.has_containers:
            container_icon = "🐳" if context.container.engine_type == "docker" else "📦"
            line_parts.append(f"{container_icon}{context.container.engine_type}")
        
        # Tech stack (max 3)
        if context.project.technologies:
            tech_icons = self._get_tech_icons()
            tech_display = []
            
            for tech in context.project.technologies[:3]:
                icon = tech_icons.get(tech, "🛠️")
                tech_display.append(f"{icon}")
            
            if tech_display:
                line_parts.append("".join(tech_display))
        
        # Print compact line
        print(" ".join(line_parts))
        
        # Environment context (if not standard Windows)
        if env_info.type != 'windows':
            context_line = f"   {env_info.display_name}"
            if env_info.container_type:
                context_line += f" • {env_info.container_type}"
            print(f"   \033[90m{context_line}\033[0m")
    
    def _get_tech_icons(self) -> dict:
        """Ícones para tecnologias"""
        return {
            'Python': '🐍',
            'Node.js': '📦',
            'React': '⚛️',
            'TypeScript': '📘',
            'Docker': '🐳',
            'Java': '☕',
            'C#/.NET': '💜',
            'PowerShell': '💙',
            'Web': '🌐',
            'Git': '📝'
        }
    
    def _check_and_report_anomalies(self, context: DevelopmentContext) -> None:
        """Verifica anomalias e reporta via Telegram"""
        if not self.ai_service.is_available():
            return
            
        anomalies = self.ai_service.detect_anomalies(context)
        
        if anomalies:
            # Mostra alerta compacto
            print(f"   \033[93m⚠️  {len(anomalies)} anomalia(s) detectada(s)\033[0m")
            
            # Envia via Telegram (se configurado)
            if self.telegram_service.is_available():
                self.telegram_service.send_anomaly_alert(anomalies, context.project.name)
    
    def _show_ai_suggestions(self, context: DevelopmentContext) -> None:
        """Mostra sugestões da AI"""
        if not self.ai_service.is_available():
            print("   \033[90m💡 xkit-help para comandos\033[0m")
            return
        
        suggestions = self.ai_service.analyze_project_context(context)
        if suggestions:
            # Mostra primeira linha da sugestão
            first_line = suggestions.split('\n')[0][:60]
            print(f"   \033[94m🤖 {first_line}...\033[0m")
            print("   \033[90m💡 xkit-ai para sugestões completas\033[0m")
        else:
            print("   \033[90m💡 xkit-help para comandos\033[0m")
    
    def show_help(self, context: DevelopmentContext) -> None:
        """Mostra ajuda compacta"""
        print("🔧 \033[1mXKit v2.0 - Comandos\033[0m")
        print()
        
        # Comandos básicos
        commands = [
            ("xkit-help", "Esta ajuda"),
            ("xkit-status", "Status detalhado"),
            ("xkit-ai", "Sugestões da IA"),
            ("xkit-reload", "Recarregar perfil")
        ]
        
        for cmd, desc in commands:
            print(f"  \033[96m{cmd:<12}\033[0m {desc}")
        
        # Comandos contextuais
        if context.is_git_project:
            print(f"\n🌿 \033[1mGit ({context.git.current_branch})\033[0m")
            git_commands = [
                ("git status", "Status do repositório"),
                ("git add .", "Adicionar mudanças"),
                ("git commit", "Fazer commit"),
            ]
            for cmd, desc in git_commands:
                print(f"  \033[92m{cmd:<12}\033[0m {desc}")
        
        # Container commands
        if context.has_containers:
            engine = context.container.engine_type
            print(f"\n🐳 \033[1m{engine.title()}\033[0m")
            container_commands = [
                (f"{engine} ps", "Listar containers"),
                (f"{engine} images", "Listar imagens"),
            ]
            for cmd, desc in container_commands:
                print(f"  \033[93m{cmd:<12}\033[0m {desc}")
    
    def show_status(self, context: DevelopmentContext) -> None:
        """Mostra status detalhado"""
        env_info = self.env_detector.detect()
        
        print("📊 \033[1mStatus do XKit\033[0m")
        print(f"   Ambiente: {env_info.icon} {env_info.display_name}")
        print(f"   Projeto: 📁 {context.project.name}")
        print(f"   Caminho: {context.project.path}")
        
        if context.is_git_project:
            status_icon = "✓" if context.git.is_clean else "±"
            print(f"   Git: 🌿 {context.git.current_branch} {status_icon}")
            if not context.git.is_clean:
                print(f"   Mudanças: {context.git.changes_count}")
        
        if context.project.technologies:
            tech_list = ", ".join(context.project.technologies[:5])
            print(f"   Tech: 🛠️  {tech_list}")
        
        if context.has_containers:
            print(f"   Container: 🐳 {context.container.engine_type}")
        
        # AI Status
        ai_status = "✓" if self.ai_service.is_available() else "✗"
        telegram_status = "✓" if self.telegram_service.is_available() else "✗"
        print(f"   Serviços: 🤖{ai_status} 📱{telegram_status}")
    
    def show_ai_suggestions(self, context: DevelopmentContext) -> None:
        """Mostra sugestões completas da AI"""
        if not self.ai_service.is_available():
            print("❌ Gemini AI não configurado")
            print("   Configure GEMINI_API_KEY para habilitar sugestões")
            return
        
        print("🤖 \033[1mAnalisando projeto...\033[0m")
        
        suggestions = self.ai_service.analyze_project_context(context)
        if suggestions:
            print()
            print("\033[94m" + suggestions + "\033[0m")
            
            # Envia resumo via Telegram
            if self.telegram_service.is_available():
                self.telegram_service.send_project_summary(context)
                print("\n📱 Resumo enviado via Telegram")
        else:
            print("❌ Não foi possível obter sugestões da AI")
    
    def ask_ai_solution(self, problem: str, context: DevelopmentContext) -> None:
        """Pergunta solução para a AI"""
        if not self.ai_service.is_available():
            print("❌ Gemini AI não configurado")
            return
        
        print(f"🤖 \033[1mBuscando solução para: {problem}\033[0m")
        
        solution = self.ai_service.suggest_solution(problem, context)
        if solution:
            print()
            print("\033[92m" + solution + "\033[0m")
        else:
            print("❌ Não foi possível obter solução da AI")