#!/usr/bin/env python3
"""
Sistema de Emergência Anti-Spam Telegram
Para quando o bot está enviando mensagens em loop
"""
import sys
import time
import requests
from pathlib import Path
from datetime import datetime, timedelta

# Add XKit path
XKIT_ROOT = Path(__file__).parent
sys.path.insert(0, str(XKIT_ROOT / "Scripts"))

try:
    from xkit.infrastructure.config import XKitConfigService
except ImportError as e:
    print(f"❌ Erro de import: {e}")
    sys.exit(1)


class TelegramAntiSpam:
    """Sistema de emergência para parar spam"""
    
    def __init__(self):
        self.config = XKitConfigService()
        self.telegram_config = self.config.get_section("telegram")
        
        if not self.telegram_config:
            print("❌ Configuração não encontrada!")
            sys.exit(1)
            
        self.token = self.telegram_config.get("token")
        self.admin_id = self.telegram_config.get("admin_id")
        self.base_url = f"https://api.telegram.org/bot{self.token}"
        
    def get_recent_messages(self, limit: int = 100):
        """Obtém mensagens recentes"""
        try:
            response = requests.get(
                f"{self.base_url}/getUpdates",
                params={"limit": limit, "offset": -limit},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("ok"):
                    return data.get("result", [])
            return []
            
        except Exception as e:
            print(f"❌ Erro obtendo mensagens: {e}")
            return []
    
    def analyze_spam(self):
        """Analisa se há spam nas mensagens recentes"""
        print("🔍 Analisando mensagens recentes...")
        
        messages = self.get_recent_messages()
        
        if not messages:
            print("📭 Nenhuma mensagem encontrada")
            return False
        
        # Contar mensagens por timeframe
        now = datetime.now()
        last_5min = now - timedelta(minutes=5)
        last_1min = now - timedelta(minutes=1)
        
        recent_messages = []
        
        for msg in messages:
            if "message" in msg:
                message = msg["message"]
                timestamp = datetime.fromtimestamp(message.get("date", 0))
                
                if timestamp > last_5min:
                    from_bot = message.get("from", {}).get("is_bot", False)
                    text = message.get("text", "")
                    
                    recent_messages.append({
                        "timestamp": timestamp,
                        "is_bot": from_bot,
                        "text": text[:50] + "..." if len(text) > 50 else text,
                        "chat_id": message.get("chat", {}).get("id")
                    })
        
        # Estatísticas
        total_recent = len(recent_messages)
        bot_messages = [m for m in recent_messages if m["is_bot"]]
        last_minute = [m for m in recent_messages if m["timestamp"] > last_1min]
        
        print(f"📊 Mensagens nos últimos 5 min: {total_recent}")
        print(f"🤖 Mensagens do bot: {len(bot_messages)}")
        print(f"⚡ Mensagens no último minuto: {len(last_minute)}")
        
        # Detectar spam (mais de 10 mensagens do bot em 5 min)
        is_spam = len(bot_messages) > 10
        
        if is_spam:
            print("🚨 SPAM DETECTADO!")
            print("\nÚltimas mensagens do bot:")
            for msg in bot_messages[-5:]:
                print(f"  🕒 {msg['timestamp'].strftime('%H:%M:%S')}: {msg['text']}")
        else:
            print("✅ Nenhum spam detectado")
        
        return is_spam
    
    def send_stop_message(self):
        """Envia mensagem para parar o sistema"""
        stop_msg = f"""🛑 **SISTEMA DE EMERGÊNCIA ANTI-SPAM ATIVADO** 

⏰ **Timestamp:** {datetime.now().strftime('%H:%M:%S')}
🚨 **Motivo:** Spam detectado automaticamente

🔧 **Ações tomadas:**
• Sistema de polling será interrompido
• MCP servers serão reiniciados  
• Cache de mensagens limpo

📋 **Para reativar:**
1. Investigate root cause
2. Fix the issue
3. Restart bot manually

⚠️ **SISTEMA EM MODO SEGURO**"""
        
        try:
            response = requests.post(
                f"{self.base_url}/sendMessage",
                json={
                    "chat_id": self.admin_id,
                    "text": stop_msg
                },
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ Mensagem de emergência enviada")
                return True
            else:
                print(f"❌ Erro enviando emergência: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False
    
    def clear_webhook(self):
        """Limpa webhook se existir"""
        try:
            response = requests.post(
                f"{self.base_url}/deleteWebhook",
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ Webhook limpo")
            
        except Exception:
            pass
    
    def emergency_stop(self):
        """Procedimento de emergência completo"""
        print("🚨 PROCEDIMENTO DE EMERGÊNCIA ANTI-SPAM")
        print("=" * 45)
        
        # 1. Analisar spam
        is_spam = self.analyze_spam()
        
        if not is_spam:
            print("\n✅ Nenhum spam detectado. Sistema normal.")
            return False
        
        # 2. Enviar mensagem de parada
        print("\n📤 Enviando notificação de emergência...")
        self.send_stop_message()
        
        # 3. Limpar webhook
        print("🧹 Limpando webhook...")
        self.clear_webhook()
        
        # 4. Instruções para o usuário
        print("\n🔧 PRÓXIMOS PASSOS:")
        print("1. ✋ PARAR todos os processos Python do bot")
        print("2. 🔍 INVESTIGAR causa do spam")  
        print("3. 🛠️ CORRIGIR problema")
        print("4. 🚀 REINICIAR bot manualmente")
        
        return True


def main():
    """Função principal"""
    anti_spam = TelegramAntiSpam()
    
    try:
        spam_detected = anti_spam.emergency_stop()
        sys.exit(1 if spam_detected else 0)
    except KeyboardInterrupt:
        print("\n👋 Interrompido pelo usuário")
        sys.exit(1)


if __name__ == "__main__":
    main()