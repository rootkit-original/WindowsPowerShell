#!/usr/bin/env python3
"""
Script de teste para o MCP Server do Telegram
Testa todas as funcionalidades do servidor MCP integrado com Telegram Bot
"""
import sys
import asyncio
import logging
from pathlib import Path
from typing import Dict, Any

# Add XKit path
sys.path.insert(0, str(Path(__file__).parent.parent / "Scripts"))

from xkit.mcp.client import XKitMCPClient
from xkit.infrastructure.config import XKitConfigService

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TelegramMCPTester:
    """Tester para o MCP Server do Telegram"""
    
    def __init__(self):
        self.mcp_client = XKitMCPClient()
        self.config = XKitConfigService()
        self.server_name = "telegram-bot"
    
    async def run_all_tests(self):
        """Executa todos os testes do MCP Server"""
        print("🚀 Iniciando testes do MCP Telegram Server...")
        print("=" * 60)
        
        try:
            # Test 1: Verificar se servidor está disponível
            await self.test_server_availability()
            
            # Test 2: Listar ferramentas disponíveis
            await self.test_list_tools()
            
            # Test 3: Testar informações do bot
            await self.test_bot_info()
            
            # Test 4: Testar envio de mensagem
            await self.test_send_message()
            
            # Test 5: Testar relatório de projeto
            await self.test_project_report()
            
            # Test 6: Testar status do sistema
            await self.test_system_status()
            
            # Test 7: Testar status Git
            await self.test_git_status()
            
            # Test 8: Testar comando do Telegram
            await self.test_telegram_command()
            
            print("\\n" + "=" * 60)
            print("✅ Todos os testes concluídos!")
            
        except Exception as e:
            print(f"\\n❌ Erro durante os testes: {e}")
            logger.exception("Erro nos testes")
    
    async def test_server_availability(self):
        """Testa se o servidor MCP está disponível"""
        print("\\n📡 Teste 1: Disponibilidade do Servidor")
        print("-" * 40)
        
        try:
            servers = await self.mcp_client.list_servers()
            
            if self.server_name in servers:
                print(f"✅ Servidor '{self.server_name}' encontrado")
                server_info = servers[self.server_name]
                print(f"   Tipo: {server_info.get('type', 'unknown')}")
                print(f"   Ativo: {server_info.get('enabled', False)}")
            else:
                print(f"❌ Servidor '{self.server_name}' não encontrado")
                print(f"   Servidores disponíveis: {list(servers.keys())}")
                
        except Exception as e:
            print(f"❌ Erro ao verificar disponibilidade: {e}")
    
    async def test_list_tools(self):
        """Testa listagem de ferramentas"""
        print("\\n🛠️ Teste 2: Listagem de Ferramentas")
        print("-" * 40)
        
        try:
            result = await self.mcp_client.call_tool(
                self.server_name, "list_tools", {}
            )
            
            if result.get("success"):
                tools = result.get("result", [])
                print(f"✅ {len(tools)} ferramentas encontradas:")
                
                for tool in tools:
                    if isinstance(tool, dict):
                        name = tool.get("name", "Unknown")
                        description = tool.get("description", "No description")
                        print(f"   • {name}: {description}")
                    else:
                        print(f"   • {tool}")
            else:
                print(f"❌ Erro ao listar ferramentas: {result.get('error')}")
                
        except Exception as e:
            print(f"❌ Erro na listagem: {e}")
    
    async def test_bot_info(self):
        """Testa informações do bot"""
        print("\\n🤖 Teste 3: Informações do Bot")
        print("-" * 40)
        
        try:
            result = await self.mcp_client.call_tool(
                self.server_name, "get-bot-info", {}
            )
            
            if result.get("success"):
                bot_info = result.get("result", {})
                print("✅ Bot info obtida:")
                print(f"   Disponível: {bot_info.get('service_available', False)}")
                
                if "bot_info" in bot_info:
                    info = bot_info["bot_info"]
                    print(f"   Nome: {info.get('first_name', 'N/A')}")
                    print(f"   Username: @{info.get('username', 'N/A')}")
            else:
                print(f"❌ Erro ao obter bot info: {result.get('error')}")
                
        except Exception as e:
            print(f"❌ Erro no teste de bot info: {e}")
    
    async def test_send_message(self):
        """Testa envio de mensagem"""
        print("\\n📱 Teste 4: Envio de Mensagem")
        print("-" * 40)
        
        # Verificar se Telegram está configurado
        telegram_config = self.config.get_section("telegram")
        if not telegram_config or not telegram_config.get("enabled"):
            print("⚠️ Telegram não configurado - pulando teste")
            return
        
        try:
            test_message = """🧪 **Teste MCP Telegram Server**

✅ Mensagem enviada via MCP Server
🚀 XKit v3.0 - Hybrid MCP Architecture
🕒 Teste executado automaticamente

*Este é um teste de integração*"""
            
            result = await self.mcp_client.call_tool(
                self.server_name, "send-message", {
                    "message": test_message,
                    "format": "markdown"
                }
            )
            
            if result.get("success"):
                print("✅ Mensagem enviada com sucesso!")
                print(f"   Timestamp: {result.get('result', {}).get('timestamp', 'N/A')}")
            else:
                print(f"❌ Erro ao enviar mensagem: {result.get('error')}")
                
        except Exception as e:
            print(f"❌ Erro no teste de mensagem: {e}")
    
    async def test_project_report(self):
        """Testa relatório de projeto"""
        print("\\n📊 Teste 5: Relatório de Projeto")
        print("-" * 40)
        
        try:
            result = await self.mcp_client.call_tool(
                self.server_name, "send-project-report", {
                    "project_path": ".",
                    "include_ai": True,
                    "include_suggestions": True
                }
            )
            
            if result.get("success"):
                report_info = result.get("result", {})
                print("✅ Relatório enviado!")
                print(f"   Projeto: {report_info.get('project_path', 'N/A')}")
                print(f"   Score: {report_info.get('score', 'N/A')}")
                print(f"   Tamanho: {report_info.get('report_length', 'N/A')} chars")
            else:
                print(f"❌ Erro no relatório: {result.get('error')}")
                
        except Exception as e:
            print(f"❌ Erro no teste de relatório: {e}")
    
    async def test_system_status(self):
        """Testa status do sistema"""
        print("\\n🔧 Teste 6: Status do Sistema")
        print("-" * 40)
        
        try:
            result = await self.mcp_client.call_tool(
                self.server_name, "send-system-status", {
                    "include_plugins": True,
                    "include_mcp": True
                }
            )
            
            if result.get("success"):
                print("✅ Status do sistema enviado!")
                status_info = result.get("result", {})
                print(f"   Plugins incluídos: {status_info.get('include_plugins', False)}")
                print(f"   MCP incluído: {status_info.get('include_mcp', False)}")
            else:
                print(f"❌ Erro no status: {result.get('error')}")
                
        except Exception as e:
            print(f"❌ Erro no teste de status: {e}")
    
    async def test_git_status(self):
        """Testa status Git"""
        print("\\n🌿 Teste 7: Status Git")
        print("-" * 40)
        
        try:
            result = await self.mcp_client.call_tool(
                self.server_name, "send-git-status", {
                    "repo_path": ".",
                    "detailed": True
                }
            )
            
            if result.get("success"):
                print("✅ Status Git enviado!")
                git_info = result.get("result", {})
                print(f"   Repositório: {git_info.get('repo_path', 'N/A')}")
                print(f"   Detalhado: {git_info.get('detailed', False)}")
            else:
                print(f"❌ Erro no Git status: {result.get('error')}")
                
        except Exception as e:
            print(f"❌ Erro no teste Git: {e}")
    
    async def test_telegram_command(self):
        """Testa processamento de comando"""
        print("\\n📲 Teste 8: Comando do Telegram")
        print("-" * 40)
        
        try:
            result = await self.mcp_client.call_tool(
                self.server_name, "handle-telegram-command", {
                    "command": "/status",
                    "args": [],
                    "user_id": "test_user",
                    "chat_id": "test_chat"
                }
            )
            
            if result.get("success"):
                print("✅ Comando processado!")
                cmd_info = result.get("result", {})
                print(f"   Comando: {cmd_info.get('command', 'N/A')}")
                print(f"   Processado: {cmd_info.get('processed', False)}")
                print(f"   Resposta enviada: {cmd_info.get('response_sent', False)}")
            else:
                print(f"❌ Erro no comando: {result.get('error')}")
                
        except Exception as e:
            print(f"❌ Erro no teste de comando: {e}")
    
    def print_configuration_help(self):
        """Exibe ajuda de configuração"""
        print("\\n" + "=" * 60)
        print("📝 Configuração necessária para testes completos:")
        print("=" * 60)
        print("\\n1. Configure o Telegram em ~/.xkit/config.json:")
        print('{')
        print('  "telegram": {')
        print('    "enabled": true,')
        print('    "token": "SEU_BOT_TOKEN",')
        print('    "admin_id": "SEU_CHAT_ID"')
        print('  }')
        print('}')
        print("\\n2. Obtenha o token do bot em @BotFather")
        print("3. Obtenha seu chat_id enviando /start para @userinfobot")
        print("\\n💡 Alguns testes podem falhar sem configuração completa")


async def main():
    """Função principal"""
    tester = TelegramMCPTester()
    
    # Exibe ajuda de configuração
    tester.print_configuration_help()
    
    # Aguarda confirmação do usuário
    try:
        input("\\n🔄 Pressione ENTER para continuar com os testes (Ctrl+C para sair)...")
    except KeyboardInterrupt:
        print("\\n❌ Testes cancelados pelo usuário")
        return
    
    # Executa testes
    await tester.run_all_tests()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\\n❌ Testes interrompidos")
    except Exception as e:
        print(f"\\n❌ Erro crítico: {e}")