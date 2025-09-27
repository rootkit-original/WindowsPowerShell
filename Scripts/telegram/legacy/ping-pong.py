#!/usr/bin/env python3
"""
Teste de Ping-Pong com Telegram
Validação rápida da conectividade
"""
import sys
import time
import requests
from pathlib import Path
from datetime import datetime

# Add XKit path
XKIT_ROOT = Path(__file__).parent
sys.path.insert(0, str(XKIT_ROOT / "Scripts"))

try:
    from xkit.infrastructure.config import XKitConfigService
except ImportError as e:
    print(f"❌ Erro de import: {e}")
    sys.exit(1)


class TelegramPingPong:
    """Teste simples de ping-pong com Telegram"""
    
    def __init__(self):
        self.config = XKitConfigService()
        self.telegram_config = self.config.get_section("telegram")
        
        if not self.telegram_config:
            print("❌ Configuração Telegram não encontrada!")
            print("📋 Configure em Scripts/xkit/config/config.json:")
            print("""
{
  "telegram": {
    "enabled": true,
    "token": "SEU_BOT_TOKEN_AQUI",
    "admin_id": "SEU_USER_ID_AQUI"
  }
}
            """)
            sys.exit(1)
            
        self.token = self.telegram_config.get("token")
        self.admin_id = self.telegram_config.get("admin_id")
        self.base_url = f"https://api.telegram.org/bot{self.token}"
        
    def ping(self) -> bool:
        """Envia ping para o Telegram"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        ping_message = f"""🏓 PING - {timestamp}

🧪 Teste de Conectividade XKit

🤖 Bot: @xkit_bot
👤 Admin ID: {self.admin_id}
🌐 Status: Testando conexão...

📱 Se você recebeu esta mensagem:
✅ Token configurado corretamente
✅ Bot funcionando  
✅ Permissões OK
✅ Rede funcionando

🎯 Responda com: PONG"""
        
        try:
            response = requests.post(
                f"{self.base_url}/sendMessage",
                json={
                    "chat_id": self.admin_id,
                    "text": ping_message
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("ok"):
                    print(f"✅ PING enviado com sucesso! ({timestamp})")
                    print(f"📱 Mensagem ID: {data['result']['message_id']}")
                    return True
                else:
                    print(f"❌ Erro na API: {data}")
                    return False
            else:
                print(f"❌ Erro HTTP: {response.status_code}")
                print(f"Resposta: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Erro no ping: {e}")
            return False
    
    def check_pong(self) -> bool:
        """Verifica se recebeu PONG"""
        try:
            response = requests.get(
                f"{self.base_url}/getUpdates",
                params={
                    "offset": -1,  # Última mensagem
                    "limit": 1
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("ok") and data.get("result"):
                    updates = data["result"]
                    if updates:
                        message = updates[0].get("message", {})
                        text = message.get("text", "").upper()
                        user_id = str(message.get("from", {}).get("id", ""))
                        
                        if "PONG" in text and user_id == str(self.admin_id):
                            timestamp = datetime.now().strftime("%H:%M:%S")
                            print(f"✅ PONG recebido! ({timestamp})")
                            return True
            
            return False
            
        except Exception as e:
            print(f"❌ Erro verificando PONG: {e}")
            return False
    
    def validate_config(self):
        """Valida configuração do Telegram"""
        print("🔍 Validando configuração...")
        
        if not self.token:
            print("❌ Token não configurado!")
            return False
            
        if not self.admin_id:
            print("❌ Admin ID não configurado!")
            return False
            
        # Testar conectividade com bot
        try:
            response = requests.get(f"{self.base_url}/getMe", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("ok"):
                    bot_info = data["result"]
                    print(f"✅ Bot conectado: {bot_info['username']} (@{bot_info['username']})")
                    print(f"✅ Admin ID: {self.admin_id}")
                    return True
                else:
                    print(f"❌ Erro na API do bot: {data}")
                    return False
            else:
                print(f"❌ Erro HTTP: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erro de conectividade: {e}")
            return False
    
    def run_test(self, wait_pong: bool = True):
        """Executa teste completo"""
        print("🏓 XKit Telegram Ping-Pong Test")
        print("=" * 40)
        
        # Validar configuração
        if not self.validate_config():
            print("\n❌ Configuração inválida!")
            return False
        
        print("\n📤 Enviando PING...")
        
        # Enviar ping
        if not self.ping():
            print("❌ Falha no PING!")
            return False
        
        if wait_pong:
            print("\n⏳ Aguardando PONG... (responda 'PONG' no Telegram)")
            print("⏰ Timeout em 30 segundos...")
            
            # Aguardar PONG por 30 segundos
            start_time = time.time()
            while time.time() - start_time < 30:
                if self.check_pong():
                    print("✅ Teste PING-PONG completado com sucesso!")
                    return True
                time.sleep(2)
            
            print("⏰ Timeout - PONG não recebido")
            print("💡 Dica: Verifique se você respondeu 'PONG' no chat")
            return False
        else:
            print("✅ PING enviado! Verifique seu Telegram")
            return True


def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Teste Ping-Pong Telegram")
    parser.add_argument("--no-wait", action="store_true", help="Não aguardar PONG")
    parser.add_argument("--continuous", action="store_true", help="Teste contínuo")
    
    args = parser.parse_args()
    
    pinger = TelegramPingPong()
    
    if args.continuous:
        print("🔄 Modo contínuo ativado (Ctrl+C para parar)")
        try:
            while True:
                pinger.run_test(wait_pong=not args.no_wait)
                if not args.no_wait:
                    print("\n⏳ Próximo ping em 60 segundos...")
                    time.sleep(60)
                else:
                    time.sleep(10)
        except KeyboardInterrupt:
            print("\n👋 Teste interrompido")
    else:
        success = pinger.run_test(wait_pong=not args.no_wait)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()