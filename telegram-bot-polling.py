#!/usr/bin/env python3
"""
XKit Telegram Bot Polling - Sistema de escuta automática para comandos
Implementa polling para processar comandos enviados no Telegram
"""
import sys
import asyncio
import requests
import json
import time
from pathlib import Path
from datetime import datetime

# Add XKit path
XKIT_ROOT = Path(__file__).parent
sys.path.insert(0, str(XKIT_ROOT / "Scripts"))

try:
    from xkit.infrastructure.config import XKitConfigService
    from xkit.mcp.client import XKitMCPClient
except ImportError as e:
    print(f"❌ Erro de import: {e}")
    print("🔧 Executando do diretório correto...")
    sys.exit(1)


class TelegramBotPoller:
    """Sistema de polling para comandos Telegram"""
    
    def __init__(self):
        self.config = XKitConfigService()
        self.telegram_config = self.config.get_section("telegram")
        
        if not self.telegram_config:
            print("❌ Configuração Telegram não encontrada!")
            sys.exit(1)
            
        self.token = self.telegram_config.get("token")
        self.admin_id = self.telegram_config.get("admin_id")
        self.base_url = f"https://api.telegram.org/bot{self.token}"
        
        self.mcp_client = XKitMCPClient()
        self.last_update_id = 0
        self.running = False
        
    def is_configured(self) -> bool:
        """Verifica se está configurado"""
        return bool(self.token and self.admin_id)
    
    async def start_polling(self):
        """Inicia o polling automático"""
        if not self.is_configured():
            print("❌ Token ou Admin ID não configurados!")
            return
            
        print("🤖 XKit Telegram Bot Polling iniciado!")
        print(f"📱 Monitorando comandos para: {self.admin_id}")
        print("🔄 Pressione Ctrl+C para parar")
        print("-" * 50)
        
        self.running = True
        
        # Teste de conectividade
        await self._test_connection()
        
        # Limpar mensagens antigas para evitar loop
        await self._clear_old_messages()
        
        # Loop principal de polling
        while self.running:
            try:
                await self._poll_updates()
                await asyncio.sleep(2)  # Poll a cada 2 segundos (menos spam)
            except KeyboardInterrupt:
                print("\\n🛑 Parando bot polling...")
                break
            except Exception as e:
                print(f"⚠️ Erro no polling: {e}")
                await asyncio.sleep(5)  # Wait longer on error
                
        print("👋 Bot polling parado")
    
    async def _test_connection(self):
        """Testa conexão com Telegram"""
        try:
            response = requests.get(f"{self.base_url}/getMe", timeout=5)
            if response.status_code == 200:
                data = response.json()
                bot_info = data.get("result", {})
                bot_name = bot_info.get("first_name", "Unknown")
                bot_username = bot_info.get("username", "unknown")
                print(f"✅ Bot conectado: {bot_name} (@{bot_username})")
            else:
                print("⚠️ Problema na conexão com Telegram")
        except Exception as e:
            print(f"⚠️ Erro ao testar conexão: {e}")
    
    async def _clear_old_messages(self):
        """Limpa mensagens antigas para evitar reprocessamento"""
        try:
            print("🔄 Limpando mensagens antigas...")
            
            # Pega todas as mensagens pendentes
            response = requests.get(
                f"{self.base_url}/getUpdates", 
                params={"limit": 100, "timeout": 1},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                updates = data.get("result", [])
                
                if updates:
                    # Pega o último update_id
                    last_id = max(update["update_id"] for update in updates)
                    self.last_update_id = last_id
                    
                    # Confirma limpeza fazendo uma chamada com offset
                    requests.get(
                        f"{self.base_url}/getUpdates",
                        params={"offset": last_id + 1, "timeout": 1},
                        timeout=5
                    )
                    
                    print(f"✅ {len(updates)} mensagens antigas limpas. Último ID: {last_id}")
                else:
                    print("✅ Nenhuma mensagem antiga encontrada")
                    
        except Exception as e:
            print(f"⚠️ Erro ao limpar mensagens: {e}")
    
    async def _poll_updates(self):
        """Faz polling das mensagens"""
        try:
            url = f"{self.base_url}/getUpdates"
            params = {
                "offset": self.last_update_id + 1,
                "limit": 10,
                "timeout": 10
            }
            
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("ok") and data.get("result"):
                    updates = data["result"]
                    
                    # Processa todas as mensagens
                    for update in updates:
                        await self._process_update(update)
                        # IMPORTANTE: Atualiza o ID IMEDIATAMENTE após processar
                        self.last_update_id = update["update_id"]
                        
                    if updates:
                        print(f"🔄 Processadas {len(updates)} mensagens. Last ID: {self.last_update_id}")
                        
        except requests.exceptions.Timeout:
            pass  # Timeout normal
        except requests.exceptions.RequestException:
            pass  # Erro de rede temporário
        except Exception as e:
            print(f"⚠️ Erro inesperado no polling: {e}")
    
    async def _process_update(self, update: dict):
        """Processa mensagem recebida"""
        try:
            message = update.get("message")
            if not message:
                return
                
            # Verifica se é do admin autorizado
            user_id = str(message.get("from", {}).get("id", ""))
            if user_id != str(self.admin_id):
                print(f"🚫 Mensagem de usuário não autorizado: {user_id}")
                return
            
            # Extrai dados da mensagem
            text = message.get("text", "")
            chat_id = str(message.get("chat", {}).get("id", ""))
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            # Só processa comandos (iniciados com /)
            if text.startswith("/"):
                print(f"📲 [{timestamp}] Comando: {text}")
                await self._handle_command(text, user_id, chat_id)
            else:
                print(f"💬 [{timestamp}] Mensagem ignorada: {text[:30]}...")
                
        except Exception as e:
            print(f"⚠️ Erro ao processar mensagem: {e}")
    
    async def _handle_command(self, command_text: str, user_id: str, chat_id: str):
        """Processa comando via MCP"""
        try:
            # Parse do comando
            parts = command_text.strip().split()
            command = parts[0].lower()
            args = parts[1:] if len(parts) > 1 else []
            
            print(f"🔄 Processando: {command}")
            
            # Envia para MCP Server processar
            result = await self.mcp_client.call_tool(
                "telegram-bot",
                "handle-telegram-command",
                {
                    "command": command,
                    "args": args,
                    "user_id": user_id, 
                    "chat_id": chat_id
                }
            )
            
            if result.get("success"):
                print(f"✅ Comando executado: {command}")
            else:
                error = result.get("error", "Unknown error")
                print(f"❌ Erro no comando: {error}")
                
                # Envia mensagem de erro
                await self._send_error_message(f"❌ Erro: {error}")
                
        except Exception as e:
            print(f"⚠️ Erro crítico no comando: {e}")
            await self._send_error_message(f"💥 Erro crítico: {str(e)}")
    
    async def _send_error_message(self, error_text: str):
        """Envia mensagem de erro via MCP"""
        try:
            await self.mcp_client.call_tool(
                "telegram-bot",
                "send-message",
                {
                    "message": error_text,
                    "format": "markdown"
                }
            )
        except Exception as e:
            print(f"⚠️ Não foi possível enviar mensagem de erro: {e}")
    
    def stop(self):
        """Para o polling"""
        self.running = False


async def main():
    """Função principal"""
    print("🚀 XKit Telegram Bot - Sistema de Polling Automático")
    print("=" * 60)
    
    try:
        poller = TelegramBotPoller()
        await poller.start_polling()
    except KeyboardInterrupt:
        print("\\n👋 Sistema parado pelo usuário")
    except Exception as e:
        print(f"💥 Erro crítico: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\\n🛑 Interrompido")
    except Exception as e:
        print(f"💥 Erro na inicialização: {e}")