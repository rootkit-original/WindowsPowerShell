"""
XKit Telegram Plugin
Plugin integrado com MCP Server para comunicação completa com Telegram Bot
"""
import asyncio
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path

from .base import XKitCorePlugin
from ..infrastructure.telegram_service import TelegramService
from ..infrastructure.config import XKitConfigService
from ..core.ports.event_port import IEventService
from ..domain.entities import ProjectInfo, DevelopmentContext
from ..mcp.client import XKitMCPClient


class TelegramPlugin(XKitCorePlugin):
    """Plugin integrado com MCP Server para Telegram Bot"""
    
    def __init__(self):
        super().__init__(
            name="telegram",
            version="2.0.0", 
            description="🤖 Telegram Bot integrado com MCP Server para controle remoto completo"
        )
        self.telegram_service: Optional[TelegramService] = None
        self.config_service: Optional[XKitConfigService] = None
        self.event_service: Optional[IEventService] = None
        self.mcp_client: Optional[XKitMCPClient] = None
        
        # MCP Integration
        self._telegram_server_active = False
    
    async def _initialize_services(self) -> None:
        """Inicializa os serviços do plugin e MCP Server"""
        # Registra serviços
        self.config_service = XKitConfigService()
        self.register_service("config", self.config_service)
        
        # Inicializa cliente MCP
        await self._setup_mcp_client()
        
        # Configura Telegram se disponível
        await self._setup_telegram()
        
        # Registra handlers de eventos
        if self.event_service:
            await self._register_event_handlers()
    
    async def _setup_mcp_client(self) -> None:
        """Inicializa cliente MCP e servidor Telegram"""
        try:
            self.mcp_client = XKitMCPClient()
            
            # Tenta ativar o servidor telegram-bot
            available_servers = await self.mcp_client.list_servers()
            
            if "telegram-bot" in available_servers:
                # Testa conexão com servidor MCP Telegram
                result = await self.mcp_client.call_tool(
                    "telegram-bot", "get-bot-info", {}
                )
                
                if result.get("success"):
                    self._telegram_server_active = True
                    print("🚀 MCP Telegram Server ativado!")
                else:
                    print(f"⚠️ MCP Telegram Server com problemas: {result.get('error')}")
            else:
                print("⚠️ MCP Telegram Server não encontrado")
                
        except Exception as e:
            print(f"⚠️ Erro ao inicializar MCP Client: {e}")
    
    async def _setup_telegram(self) -> None:
        """Configura o serviço Telegram baseado na configuração"""
        telegram_config = self.config_service.get_section("telegram")
        
        if not telegram_config:
            # Cria configuração padrão
            default_config = {
                "enabled": False,
                "token": "",
                "admin_id": "",
                "notifications": {
                    "project_analysis": True,
                    "anomalies": True,
                    "startup": True,
                    "mcp_integration": True
                },
                "message_format": "markdown",
                "mcp_server_enabled": True,
                "webhook": {
                    "enabled": False,
                    "url": "",
                    "secret_token": ""
                }
            }
            self.config_service.set("telegram", default_config)
            self.config_service.save_config()
            
            # Mensagem de propaganda XKit v3.0 🎉
            print("🤖 Plugin Telegram v2.0 carregado!")
            print("� Agora com MCP Server integrado!")
            print("�📝 Configure em ~/.xkit/config.json:")
            print("   telegram.token = 'seu_bot_token'")
            print("   telegram.admin_id = 'seu_chat_id'")
            print("💡 Crie seu bot com @BotFather no Telegram!")
            print("🔌 Use comandos remotos: /analyze, /status, /git")
            return
        
        # Inicializa serviço se configurado
        if telegram_config.get("enabled", False):
            token = telegram_config.get("token")
            admin_id = telegram_config.get("admin_id")
            
            if token and admin_id:
                self.telegram_service = TelegramService(token, admin_id)
                self.register_service("telegram", self.telegram_service)
                
                if self.telegram_service.is_available():
                    print("🤖 Telegram Bot conectado!")
                    await self._send_startup_message()
                    
                    # Setup MCP Server webhook if enabled
                    if telegram_config.get("mcp_server_enabled") and self._telegram_server_active:
                        await self._setup_mcp_webhook()
                else:
                    print("⚠️ Telegram configurado mas não disponível")
            else:
                print("⚠️ Telegram habilitado mas token/admin_id não configurados")
    
    async def _setup_mcp_webhook(self) -> None:
        """Configura webhook através do MCP Server"""
        telegram_config = self.config_service.get_section("telegram")
        webhook_config = telegram_config.get("webhook", {})
        
        if webhook_config.get("enabled") and webhook_config.get("url"):
            try:
                result = await self.mcp_client.call_tool(
                    "telegram-bot", 
                    "setup-webhook",
                    {
                        "webhook_url": webhook_config["url"],
                        "secret_token": webhook_config.get("secret_token", "")
                    }
                )
                
                if result.get("success"):
                    print("🌐 Webhook Telegram configurado via MCP!")
                else:
                    print(f"⚠️ Erro no webhook: {result.get('error')}")
                    
            except Exception as e:
                print(f"⚠️ Erro ao configurar webhook: {e}")
    
    async def _register_event_handlers(self) -> None:
        """Registra handlers para eventos do sistema"""
        # Handler para análise de projeto completada
        self.register_event_handler("project_analyzed", self._on_project_analyzed)
        
        # Handler para anomalias detectadas  
        self.register_event_handler("anomalies_detected", self._on_anomalies_detected)
        
        # Handler para comandos MCP
        self.register_event_handler("mcp_command_received", self._on_mcp_command)
    
    
    async def _on_mcp_command(self, event) -> None:
        """Handler para comandos recebidos via MCP"""
        if not self._telegram_server_active:
            return
            
        command_data = event.data
        command = command_data.get("command")
        args = command_data.get("args", [])
        
        try:
            # Rota comando através do MCP Server
            result = await self.mcp_client.call_tool(
                "telegram-bot",
                "handle-telegram-command", 
                {
                    "command": command,
                    "args": args,
                    "user_id": command_data.get("user_id"),
                    "chat_id": command_data.get("chat_id")
                }
            )
            
            if result.get("success"):
                print(f"📱 Comando MCP processado: {command}")
            else:
                print(f"⚠️ Erro no comando MCP: {result.get('error')}")
                
        except Exception as e:
            print(f"⚠️ Erro ao processar comando MCP: {e}")

    async def _on_project_analyzed(self, event) -> None:
        """Handler melhorado com integração MCP"""
        if not self._should_send_notification("project_analysis"):
            return
            
        analysis: ProjectInfo = event.data.get("analysis")
        if analysis:
            # Método tradicional (fallback)
            if self.telegram_service:
                message = self._format_analysis_message(analysis)
                await asyncio.create_task(self._send_async_message(message))
            
            # Método MCP (preferred)
            if self._telegram_server_active:
                try:
                    result = await self.mcp_client.call_tool(
                        "telegram-bot",
                        "send-project-report",
                        {
                            "project_path": getattr(analysis, 'project_path', '.'),
                            "include_ai": True,
                            "include_suggestions": True
                        }
                    )
                    
                    if result.get("success"):
                        print("📱 Relatório enviado via MCP Server!")
                    
                except Exception as e:
                    print(f"⚠️ Erro MCP fallback para método tradicional: {e}")
    
    async def _on_anomalies_detected(self, event) -> None:
        """Handler para quando anomalias são detectadas"""
        if not self._should_send_notification("anomalies"):
            return
            
        anomalies = event.data.get("anomalies", {})
        project_name = event.data.get("project_name", "Unknown")
        
        if anomalies and self.telegram_service:
            success = self.telegram_service.send_anomaly_alert(anomalies, project_name)
            if success:
                print("📱 Alerta Telegram enviado")
    
    def _should_send_notification(self, notification_type: str) -> bool:
        """Verifica se deve enviar notificação do tipo especificado"""
        if not self.telegram_service or not self.telegram_service.is_available():
            return False
            
        telegram_config = self.config_service.get_section("telegram")
        notifications = telegram_config.get("notifications", {})
        
        return notifications.get(notification_type, True)
    
    def _format_analysis_message(self, analysis: ProjectInfo) -> str:
        """Formata mensagem de análise de projeto"""
        score = analysis.quality_score
        score_emoji = "🟢" if score >= 8 else "🟡" if score >= 6 else "🔴"
        
        message = f"📊 *Análise XKit Concluída*\n\n"
        message += f"📁 Projeto: `{analysis.project_name}`\n"
        message += f"{score_emoji} Qualidade: **{score:.1f}/10**\n\n"
        
        # Adiciona métricas principais
        if analysis.metrics:
            message += f"📈 *Métricas:*\n"
            message += f"• Arquivos: {analysis.metrics.total_files}\n"
            message += f"• Documentação: {'✅' if analysis.metrics.documentation_files > 0 else '❌'}\n"
            message += f"• Git: {'✅' if analysis.metrics.has_git else '❌'}\n"
        
        # Adiciona tecnologias detectadas
        if analysis.technologies:
            tech_line = " ".join([f"#{tech.lower()}" for tech in analysis.technologies[:3]])
            message += f"\n🛠️ {tech_line}\n"
        
        return message
    
    async def _send_async_message(self, message: str) -> bool:
        """Envia mensagem de forma assíncrona"""
        if self.telegram_service:
            # Executa em thread separada para não bloquear
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, self.telegram_service._send_message, message)
        return False
    
    async def _send_startup_message(self) -> None:
        """Envia mensagem de inicialização melhorada"""
        if self._should_send_notification("startup"):
            startup_msg = "🚀 *XKit v3.0 - Telegram Bot Ativo*\n\n"
            startup_msg += "✅ Bot conectado com Hybrid MCP Architecture\n"
            startup_msg += "🔌 MCP Server: " + ("✅ Ativo" if self._telegram_server_active else "❌ Indisponível") + "\n"
            startup_msg += "📊 Relatórios automáticos de análise ativados\n\n"
            startup_msg += "*Comandos disponíveis:*\n"
            startup_msg += "• /analyze - Analisar projeto\n"
            startup_msg += "• /status - Status do sistema\n"
            startup_msg += "• /git - Status Git\n"
            startup_msg += "• /help - Lista de comandos"
            
            await self._send_async_message(startup_msg)
    
    # MCP Integration Methods
    async def send_system_status(self) -> bool:
        """Envia status do sistema via MCP"""
        if not self._telegram_server_active:
            return False
            
        try:
            result = await self.mcp_client.call_tool(
                "telegram-bot",
                "send-system-status",
                {
                    "include_plugins": True,
                    "include_mcp": True
                }
            )
            return result.get("success", False)
        except Exception as e:
            print(f"⚠️ Erro ao enviar status via MCP: {e}")
            return False
    
    async def analyze_and_send_project(self, project_path: str = ".") -> bool:
        """Analisa projeto e envia via MCP"""
        if not self._telegram_server_active:
            return False
            
        try:
            result = await self.mcp_client.call_tool(
                "telegram-bot",
                "send-project-report",
                {
                    "project_path": project_path,
                    "include_ai": True,
                    "include_suggestions": True
                }
            )
            return result.get("success", False)
        except Exception as e:
            print(f"⚠️ Erro ao analisar via MCP: {e}")
            return False
    
    async def send_git_status(self, repo_path: str = ".") -> bool:
        """Envia status Git via MCP"""
        if not self._telegram_server_active:
            return False
            
        try:
            result = await self.mcp_client.call_tool(
                "telegram-bot",
                "send-git-status", 
                {
                    "repo_path": repo_path,
                    "detailed": True
                }
            )
            return result.get("success", False)
        except Exception as e:
            print(f"⚠️ Erro ao enviar Git status via MCP: {e}")
            return False
    
    def get_commands(self) -> Dict[str, Callable]:
        """Retorna comandos disponíveis do plugin"""
        return {
            "telegram-status": self.cmd_telegram_status,
            "telegram-test": self.cmd_telegram_test,
            "telegram-config": self.cmd_telegram_config
        }
    
    async def cmd_telegram_status(self, *args) -> None:
        """Comando para verificar status do Telegram"""
        if not self.telegram_service:
            print("🤖 Telegram não configurado")
            print("📝 Configure em ~/.xkit/config.json")
            return
        
        if self.telegram_service.is_available():
            print("🤖 Telegram Bot: ✅ Conectado")
            print(f"📱 Admin ID: {self.telegram_service.admin_id}")
        else:
            print("🤖 Telegram Bot: ❌ Não disponível")
            print("⚠️ Verifique token e admin_id")
    
    async def cmd_telegram_test(self, *args) -> None:
        """Comando para testar envio de mensagem"""
        if not self.telegram_service or not self.telegram_service.is_available():
            print("🤖 Telegram não disponível para teste")
            return
        
        test_message = "🧪 *Teste XKit Telegram Plugin*\n\n"
        test_message += "✅ Plugin funcionando corretamente!"
        
        success = await self._send_async_message(test_message)
        if success:
            print("📱 Mensagem de teste enviada!")
        else:
            print("❌ Falha ao enviar mensagem de teste")
    
    async def cmd_telegram_config(self, *args) -> None:
        """Comando para exibir configuração atual"""
        telegram_config = self.config_service.get_section("telegram")
        
        if not telegram_config:
            print("🤖 Telegram não configurado")
            return
        
        print("🤖 *Configuração Telegram:*")
        print(f"   Habilitado: {'✅' if telegram_config.get('enabled') else '❌'}")
        print(f"   Token: {'✅ Configurado' if telegram_config.get('token') else '❌ Não configurado'}")
        print(f"   Admin ID: {'✅ Configurado' if telegram_config.get('admin_id') else '❌ Não configurado'}")
        
        notifications = telegram_config.get("notifications", {})
        print("📢 *Notificações:*")
        for notif_type, enabled in notifications.items():
            status = "✅" if enabled else "❌"
            print(f"   {notif_type}: {status}")