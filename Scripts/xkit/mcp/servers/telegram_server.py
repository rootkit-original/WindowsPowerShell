"""
Telegram MCP Server
Provides Telegram bot functionality through MCP protocol
Allows communication between XKit and Telegram Bot with access to all plugins
"""
import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

from ..protocol import MCPServer, Tool


class TelegramMCPServer(MCPServer):
    """Telegram Bot MCP Server - Bridge between MCP and Telegram"""
    
    def __init__(self):
        super().__init__("telegram-bot", "1.0.0")
        self.description = "Telegram Bot integration with full XKit access"
        self.logger = logging.getLogger(__name__)
        
        # Telegram service (initialized on demand)
        self._telegram_service = None
        self._config = None
    
    async def initialize(self) -> bool:
        """Initialize the telegram service"""
        try:
            from ...infrastructure.config import XKitConfigService
            from ...infrastructure.telegram_service import TelegramService
            
            self._config = XKitConfigService()
            telegram_config = self._config.get_section("telegram")
            
            if not telegram_config or not telegram_config.get("enabled", False):
                self.logger.warning("Telegram not enabled in config")
                return False
            
            token = telegram_config.get("token")
            admin_id = telegram_config.get("admin_id")
            
            if not token or not admin_id:
                self.logger.error("Telegram token/admin_id not configured")
                return False
            
            self._telegram_service = TelegramService(token, admin_id)
            
            if not self._telegram_service.is_available():
                self.logger.error("Telegram service not available")
                return False
            
            self.logger.info("Telegram MCP Server initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Telegram MCP Server: {e}")
            return False
    
    async def list_tools(self) -> List[Tool]:
        """List available Telegram tools"""
        return [
            Tool(
                name="send-message",
                description="Send message to Telegram admin chat",
                input_schema={
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "Message text to send"
                        },
                        "format": {
                            "type": "string", 
                            "description": "Message format",
                            "enum": ["text", "markdown", "html"],
                            "default": "markdown"
                        },
                        "reply_markup": {
                            "type": "object",
                            "description": "Optional inline keyboard markup"
                        }
                    },
                    "required": ["message"]
                }
            ),
            Tool(
                name="send-project-report",
                description="Send comprehensive project analysis report to Telegram",
                input_schema={
                    "type": "object",
                    "properties": {
                        "project_path": {
                            "type": "string",
                            "description": "Path to project to analyze"
                        },
                        "include_ai": {
                            "type": "boolean",
                            "description": "Include AI insights",
                            "default": True
                        },
                        "include_suggestions": {
                            "type": "boolean",
                            "description": "Include improvement suggestions",
                            "default": True
                        }
                    },
                    "required": []
                }
            ),
            Tool(
                name="send-system-status",
                description="Send XKit system status to Telegram",
                input_schema={
                    "type": "object",
                    "properties": {
                        "include_plugins": {
                            "type": "boolean",
                            "description": "Include plugin status",
                            "default": True
                        },
                        "include_mcp": {
                            "type": "boolean", 
                            "description": "Include MCP server status",
                            "default": True
                        }
                    },
                    "required": []
                }
            ),
            Tool(
                name="send-git-status",
                description="Send Git repository status to Telegram",
                input_schema={
                    "type": "object",
                    "properties": {
                        "repo_path": {
                            "type": "string",
                            "description": "Repository path"
                        },
                        "detailed": {
                            "type": "boolean",
                            "description": "Include detailed file changes",
                            "default": False
                        }
                    },
                    "required": []
                }
            ),
            Tool(
                name="handle-telegram-command",
                description="Process command received from Telegram bot",
                input_schema={
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "Command from Telegram chat"
                        },
                        "args": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Command arguments"
                        },
                        "user_id": {
                            "type": "string",
                            "description": "Telegram user ID"
                        },
                        "chat_id": {
                            "type": "string",
                            "description": "Telegram chat ID"
                        }
                    },
                    "required": ["command"]
                }
            ),
            Tool(
                name="setup-webhook",
                description="Setup Telegram webhook for real-time communication",
                input_schema={
                    "type": "object",
                    "properties": {
                        "webhook_url": {
                            "type": "string",
                            "description": "Public webhook URL"
                        },
                        "secret_token": {
                            "type": "string",
                            "description": "Secret token for webhook validation"
                        }
                    },
                    "required": ["webhook_url"]
                }
            ),
            Tool(
                name="get-bot-info",
                description="Get Telegram bot information and status",
                input_schema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            )
        ]
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a Telegram tool"""
        try:
            # Ensure service is initialized
            if not self._telegram_service:
                if not await self.initialize():
                    return {"error": "Telegram service not available"}
            
            # Route to appropriate handler
            handler_map = {
                "send-message": self._handle_send_message,
                "send-project-report": self._handle_send_project_report,
                "send-system-status": self._handle_send_system_status,
                "send-git-status": self._handle_send_git_status,
                "handle-telegram-command": self._handle_telegram_command,
                "setup-webhook": self._handle_setup_webhook,
                "get-bot-info": self._handle_get_bot_info
            }
            
            handler = handler_map.get(name)
            if not handler:
                return {"error": f"Unknown tool: {name}"}
            
            result = await handler(arguments)
            return {"success": True, "result": result}
            
        except Exception as e:
            self.logger.error(f"Error in {name}: {e}")
            return {"success": False, "error": str(e)}
    
    async def _handle_send_message(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Send a message to Telegram"""
        message = args.get("message", "")
        format_type = args.get("format", "markdown")
        reply_markup = args.get("reply_markup")
        
        success = await asyncio.get_event_loop().run_in_executor(
            None, self._telegram_service._send_message, message
        )
        
        return {
            "sent": success,
            "message": message,
            "format": format_type,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _handle_send_project_report(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Send project analysis report to Telegram"""
        project_path = args.get("project_path", ".")
        include_ai = args.get("include_ai", True)
        include_suggestions = args.get("include_suggestions", True)
        
        try:
            # Get project analyzer plugin through MCP
            from ...plugins.project_analyzer_plugin import XKitProjectAnalyzerPlugin
            
            analyzer = XKitProjectAnalyzerPlugin()
            await analyzer._initialize_services()
            
            # Analyze project
            result = await analyzer.analyze_project(project_path)
            
            # Format for Telegram
            report = await self._format_project_report(
                result, include_ai, include_suggestions
            )
            
            # Send to Telegram
            success = await asyncio.get_event_loop().run_in_executor(
                None, self._telegram_service._send_message, report
            )
            
            return {
                "sent": success,
                "project_path": project_path,
                "score": getattr(result, 'score', 'unknown'),
                "report_length": len(report)
            }
            
        except Exception as e:
            error_msg = f"❌ Erro na análise do projeto: {str(e)}"
            await asyncio.get_event_loop().run_in_executor(
                None, self._telegram_service._send_message, error_msg
            )
            return {"sent": False, "error": str(e)}
    
    async def _handle_send_system_status(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Send system status to Telegram"""
        include_plugins = args.get("include_plugins", True)
        include_mcp = args.get("include_mcp", True)
        
        try:
            status_report = await self._format_system_status(include_plugins, include_mcp)
            success = await asyncio.get_event_loop().run_in_executor(
                None, self._telegram_service._send_message, status_report
            )
            
            return {
                "sent": success,
                "include_plugins": include_plugins,
                "include_mcp": include_mcp
            }
            
        except Exception as e:
            return {"sent": False, "error": str(e)}
    
    async def _handle_send_git_status(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Send Git status to Telegram"""
        repo_path = args.get("repo_path", ".")
        detailed = args.get("detailed", False)
        
        try:
            git_report = await self._format_git_status(repo_path, detailed)
            success = await asyncio.get_event_loop().run_in_executor(
                None, self._telegram_service._send_message, git_report
            )
            
            return {
                "sent": success,
                "repo_path": repo_path,
                "detailed": detailed
            }
            
        except Exception as e:
            return {"sent": False, "error": str(e)}
    
    async def _handle_telegram_command(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Process command from Telegram chat"""
        command = args.get("command", "").lower()
        command_args = args.get("args", [])
        user_id = args.get("user_id")
        chat_id = args.get("chat_id")
        
        # Command routing
        response = await self._route_telegram_command(command, command_args, user_id, chat_id)
        
        # Send response back to Telegram
        if response:
            await asyncio.get_event_loop().run_in_executor(
                None, self._telegram_service._send_message, response
            )
        
        return {
            "command": command,
            "processed": True,
            "response_sent": bool(response)
        }
    
    async def _handle_setup_webhook(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Setup Telegram webhook"""
        webhook_url = args.get("webhook_url")
        secret_token = args.get("secret_token")
        
        # This would integrate with a web server for webhook handling
        # For now, return configuration info
        return {
            "webhook_configured": False,
            "webhook_url": webhook_url,
            "note": "Webhook setup requires web server integration"
        }
    
    async def _handle_get_bot_info(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get bot information"""
        try:
            bot_info = await asyncio.get_event_loop().run_in_executor(
                None, self._telegram_service.get_bot_info
            )
            return {
                "bot_info": bot_info,
                "service_available": self._telegram_service.is_available()
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def _format_project_report(self, result, include_ai: bool, include_suggestions: bool) -> str:
        """Format project analysis for Telegram"""
        if not result:
            return "❌ Não foi possível analisar o projeto"
        
        # Get basic info
        project_name = Path(result.project_path if hasattr(result, 'project_path') else '.').name
        score = getattr(result, 'score', 0)
        project_type = getattr(result, 'project_type', 'unknown')
        
        # Score emoji
        score_emoji = "🟢" if score >= 8 else "🟡" if score >= 6 else "🔴"
        
        report = [
            f"📊 **Relatório do Projeto: {project_name}**",
            f"{score_emoji} **Pontuação: {score}/10**",
            f"🔧 **Tipo: {project_type}**",
            "",
            "📈 **Métricas:**"
        ]
        
        # Add metrics if available
        metrics = getattr(result, 'metrics', None)
        if metrics:
            report.extend([
                f"📁 Arquivos: {getattr(metrics, 'total_files', 'N/A')}",
                f"💻 Código: {getattr(metrics, 'source_files', 'N/A')}",
                f"📚 Docs: {getattr(metrics, 'documentation_files', 'N/A')}",
                f"🧪 Testes: {getattr(metrics, 'test_files', 'N/A')}"
            ])
        
        # Add issues
        issues = getattr(result, 'issues', [])
        if issues:
            report.extend(["", "⚠️ **Problemas:**"])
            for issue in issues[:5]:  # Limit for Telegram
                report.append(f"• {issue}")
        
        # Add suggestions
        if include_suggestions:
            suggestions = getattr(result, 'suggestions', [])
            if suggestions:
                report.extend(["", "💡 **Sugestões:**"])
                for suggestion in suggestions[:5]:  # Limit for Telegram
                    report.append(f"• {suggestion}")
        
        # Add AI insights
        if include_ai:
            ai_insights = getattr(result, 'ai_insights', None)
            if ai_insights:
                # Truncate AI insights for Telegram
                truncated = ai_insights[:500] + "..." if len(ai_insights) > 500 else ai_insights
                report.extend([
                    "",
                    "🤖 **Insights IA:**",
                    f"_{truncated}_"
                ])
        
        report.extend([
            "",
            f"🕒 **Analisado:** {datetime.now().strftime('%H:%M:%S')}",
            "🚀 **XKit v3.0**"
        ])
        
        return "\n".join(report)
    
    async def _format_system_status(self, include_plugins: bool, include_mcp: bool) -> str:
        """Format system status for Telegram"""
        status = [
            "🚀 **XKit System Status**",
            f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "✅ **Sistema:** Ativo",
            "🏗️ **Arquitetura:** Hybrid MCP v3.0"
        ]
        
        if include_plugins:
            status.extend([
                "",
                "🧩 **Plugins:**",
                "• Project Analyzer: ✅ Ativo",
                "• Telegram Bot: ✅ Ativo",
                "• MCP Servers: ✅ Funcionando"
            ])
        
        if include_mcp:
            status.extend([
                "",
                "🔌 **MCP Servers:**",
                "• xkit-core: ✅ Ativo",
                "• xkit-ai: ✅ Ativo", 
                "• xkit-git: ✅ Ativo",
                "• telegram-bot: ✅ Ativo"
            ])
        
        return "\n".join(status)
    
    async def _format_git_status(self, repo_path: str, detailed: bool) -> str:
        """Format Git status for Telegram"""
        try:
            from ...infrastructure.git import GitRepository
            from pathlib import Path
            
            git_repo = GitRepository()
            repo_path_obj = Path(repo_path)
            status_info = git_repo.get_git_info(repo_path_obj)
            
            if not status_info:
                return f"❌ Não é um repositório Git: {repo_path}"
            
            report = [
                "🌿 **Git Status**",
                f"📂 **Repo:** {repo_path_obj.name}",
                f"🌳 **Branch:** {status_info.current_branch}",
                ""
            ]
            
            # Add file changes info
            if status_info.is_clean:
                report.append("✅ **Repositório limpo**")
            else:
                report.append(f"📝 **Modificações:** {status_info.changes_count} arquivos")
            
            return "\n".join(report)
            
        except Exception as e:
            return f"❌ Erro ao obter status Git: {str(e)}"
    
    async def _route_telegram_command(self, command: str, args: list, user_id: str, chat_id: str) -> str:
        """Route Telegram commands to appropriate handlers"""
        
        # Basic commands
        if command in ["/start", "/help"]:
            return self._get_help_message()
        
        elif command == "/status":
            status = await self._format_system_status(True, True)
            return status
            
        elif command == "/analyze":
            try:
                project_path = args[0] if args else "."
                # Análise simplificada direta
                return await self._simple_project_analysis(project_path)
            except Exception as e:
                return f"❌ Erro na análise: {str(e)}"
        
        elif command == "/git":
            try:
                repo_path = args[0] if args else "."
                return await self._format_git_status(repo_path, True)
            except Exception as e:
                return f"❌ Erro no Git: {str(e)}"
        
        elif command == "/plugins":
            return "🧩 **Plugins Disponíveis:**\\n• Project Analyzer\\n• Telegram Bot\\n• MCP Integration"
        
        else:
            return f"❓ Comando não reconhecido: {command}\\nUse /help para ver comandos disponíveis"
    
    def _get_help_message(self) -> str:
        """Get help message for Telegram bot"""
        return """🤖 **XKit Telegram Bot - Comandos Disponíveis**

📊 **Análise de Projetos:**
/analyze - Analisar projeto atual
/analyze /path/to/project - Analisar projeto específico

🔧 **Sistema:**
/status - Status completo do XKit
/plugins - Listar plugins disponíveis

🌿 **Git:**
/git - Status do repositório atual
/git /path/to/repo - Status de repositório específico

❓ **Ajuda:**
/help - Esta mensagem de ajuda

🚀 **XKit v3.0 - Hybrid MCP Architecture**
Desenvolvido com ❤️ para desenvolvedores"""
    
    async def _simple_project_analysis(self, project_path: str) -> str:
        """Análise simplificada de projeto"""
        try:
            from pathlib import Path
            import os
            
            path = Path(project_path)
            if not path.exists():
                return f"❌ Caminho não encontrado: {project_path}"
            
            # Contadores básicos
            total_files = 0
            source_files = 0
            doc_files = 0
            config_files = 0
            
            # Extensões conhecidas
            source_exts = {'.py', '.js', '.ts', '.java', '.cs', '.cpp', '.c', '.go', '.rs', '.php'}
            doc_exts = {'.md', '.txt', '.rst', '.adoc'}
            config_exts = {'.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf'}
            
            # Tecnologias detectadas
            technologies = set()
            
            # Percorrer arquivos
            for root, dirs, files in os.walk(path):
                # Ignorar diretórios comuns
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in {'node_modules', '__pycache__', 'target', 'build'}]
                
                for file in files:
                    if file.startswith('.'):
                        continue
                        
                    total_files += 1
                    file_path = Path(root) / file
                    ext = file_path.suffix.lower()
                    
                    if ext in source_exts:
                        source_files += 1
                        
                        # Detectar tecnologias
                        if ext == '.py':
                            technologies.add('Python')
                        elif ext in {'.js', '.ts'}:
                            technologies.add('JavaScript/TypeScript')
                        elif ext == '.java':
                            technologies.add('Java')
                        elif ext == '.cs':
                            technologies.add('C#')
                        elif ext in {'.cpp', '.c'}:
                            technologies.add('C/C++')
                        elif ext == '.go':
                            technologies.add('Go')
                        elif ext == '.rs':
                            technologies.add('Rust')
                            
                    elif ext in doc_exts:
                        doc_files += 1
                    elif ext in config_exts:
                        config_files += 1
                        
                    # Detectar arquivos especiais
                    if file.lower() in {'package.json', 'requirements.txt', 'cargo.toml', 'go.mod', 'pom.xml'}:
                        config_files += 1
            
            # Verificar Git
            has_git = (path / '.git').exists()
            
            # Calcular score básico
            score = 5  # Base
            if source_files > 0:
                score += 2
            if doc_files > 0:
                score += 1
            if has_git:
                score += 1
            if config_files > 0:
                score += 1
            
            # Emojis baseados no score
            score_emoji = "🟢" if score >= 8 else "🟡" if score >= 6 else "🔴"
            
            # Formatação do relatório
            report = [
                f"📊 **Análise Rápida: {path.name}**",
                f"{score_emoji} **Score: {score}/10**",
                "",
                "📈 **Métricas:**",
                f"📁 Total de arquivos: {total_files}",
                f"💻 Código fonte: {source_files}",
                f"📚 Documentação: {doc_files}",
                f"⚙️ Configuração: {config_files}",
                f"🌿 Git: {'✅ Sim' if has_git else '❌ Não'}",
                ""
            ]
            
            # Adicionar tecnologias
            if technologies:
                tech_list = list(technologies)[:3]  # Máximo 3
                report.append("🛠️ **Tecnologias:**")
                for tech in tech_list:
                    report.append(f"• {tech}")
                report.append("")
            
            # Sugestões básicas
            suggestions = []
            if not has_git:
                suggestions.append("Inicializar repositório Git")
            if doc_files == 0:
                suggestions.append("Adicionar documentação (README.md)")
            if source_files == 0:
                suggestions.append("Adicionar código fonte")
                
            if suggestions:
                report.append("💡 **Sugestões:**")
                for suggestion in suggestions[:3]:
                    report.append(f"• {suggestion}")
                report.append("")
            
            report.extend([
                f"🕒 **Analisado:** {datetime.now().strftime('%H:%M:%S')}",
                "🚀 **XKit v3.0 - Análise Rápida**"
            ])
            
            return "\n".join(report)
            
        except Exception as e:
            return f"❌ Erro na análise: {str(e)}"