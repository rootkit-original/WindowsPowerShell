#!/usr/bin/env python3
"""
Telegram Bot Listener - Sistema de escuta para comandos Telegram
Implementa polling simples para receber comandos do Telegram
"""
import sys
import asyncio
import requests
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add XKit path
sys.path.insert(0, str(Path(__file__).parent.parent / "Scripts"))

from xkit.infrastructure.config import XKitConfigService
from xkit.mcp.client import XKitMCPClient


class TelegramBotListener:
    """Listener para comandos do Telegram usando polling"""
    
    def __init__(self):
        self.config = XKitConfigService()
        self.telegram_config = self.config.get_section("telegram")
        self.token = self.telegram_config.get("token") if self.telegram_config else None
        self.admin_id = self.telegram_config.get("admin_id") if self.telegram_config else None
        self.base_url = f"https://api.telegram.org/bot{self.token}" if self.token else None
        self.mcp_client = None
        self.last_update_id = 0
        self.running = False
    
    async def start_listening(self):
        """Inicia o sistema de polling do Telegram"""
        if not self.token or not self.admin_id:
            print("❌ Token ou Admin ID não configurados!")
            return
        
        self.mcp_client = XKitMCPClient()
        self.running = True
        
        print(f"🤖 Telegram Bot Listener iniciado!")
        print(f"📱 Monitorando mensagens para admin: {self.admin_id}")
        print("🔄 Pressione Ctrl+C para parar")
        
        while self.running:
            try:
                await self._poll_updates()
                await asyncio.sleep(2)  # Poll a cada 2 segundos
            except KeyboardInterrupt:
                print("\\n🛑 Parando bot listener...")
                self.running = False
                break
            except Exception as e:
                print(f"⚠️ Erro no polling: {e}")
                await asyncio.sleep(5)  # Wait longer on error
    
    async def _poll_updates(self):
        """Faz polling das atualizações do Telegram"""
        try:
            url = f"{self.base_url}/getUpdates"
            params = {
                "offset": self.last_update_id + 1,
                "timeout": 10,
                "limit": 100
            }
            
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("ok") and data.get("result"):
                    for update in data["result"]:
                        await self._process_update(update)
                        self.last_update_id = update["update_id"]
                        
        except requests.exceptions.Timeout:
            pass  # Normal timeout, continue polling
        except Exception as e:
            print(f"⚠️ Erro no polling: {e}")
    
    async def _process_update(self, update: Dict[str, Any]):
        """Processa uma atualização recebida do Telegram"""
        try:
            message = update.get("message")
            if not message:
                return
            
            # Verifica se é do admin
            user_id = str(message.get("from", {}).get("id", ""))
            if user_id != str(self.admin_id):
                return
            
            # Extrai informações da mensagem
            text = message.get("text", "")
            chat_id = str(message.get("chat", {}).get("id", ""))
            
            if text.startswith("/"):
                print(f"📲 Comando recebido: {text}")
                await self._handle_command(text, user_id, chat_id)
                
        except Exception as e:
            print(f"⚠️ Erro ao processar update: {e}")
    
    async def _handle_command(self, command_text: str, user_id: str, chat_id: str):
        """Processa comando via MCP Server"""
        try:
            # Parse command and args
            parts = command_text.strip().split()
            command = parts[0]
            args = parts[1:] if len(parts) > 1 else []
            
            # Send to MCP Server
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
                print(f"✅ Comando processado: {command}")
            else:
                print(f"❌ Erro no comando: {result.get('error')}")
                
        except Exception as e:
            print(f"⚠️ Erro ao processar comando: {e}")
    
    def stop(self):
        """Para o listener"""
        self.running = False


async def main():
    """Função principal"""
    listener = TelegramBotListener()
    
    try:
        await listener.start_listening()
    except KeyboardInterrupt:
        print("\\n👋 Bot listener parado pelo usuário")
    finally:
        listener.stop()


if __name__ == "__main__":
    asyncio.run(main())