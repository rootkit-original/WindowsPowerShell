#!/usr/bin/env python3
"""
Script para testar configuração do Telegram no XKit
"""
import json
import sys
from pathlib import Path

def test_telegram_config():
    """Testa a configuração do Telegram"""
    config_file = Path.home() / '.xkit' / 'config.json'
    
    if not config_file.exists():
        print("❌ Arquivo de configuração não encontrado!")
        print(f"   Esperado em: {config_file}")
        return False
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        telegram_config = config.get('telegram', {})
        
        # Verificações
        enabled = telegram_config.get('enabled', False)
        token = telegram_config.get('token', '')
        admin_id = telegram_config.get('admin_id', '')
        
        print("🔍 Verificando configuração do Telegram...")
        print(f"   Habilitado: {'✅' if enabled else '❌'} {enabled}")
        print(f"   Token: {'✅' if token and len(token) > 20 else '❌'} {len(token) if token else 0} caracteres")
        print(f"   Admin ID: {'✅' if admin_id else '❌'} {admin_id}")
        
        if not enabled:
            print("\n💡 Para habilitar:")
            print("   1. Configure telegram.enabled = true")
            print("   2. Adicione seu bot token")
            print("   3. Adicione seu chat ID")
            return False
        
        if not token or len(token) < 20:
            print("\n❌ Token inválido!")
            print("   1. Converse com @BotFather no Telegram")
            print("   2. Use /newbot para criar um bot")
            print("   3. Copie o token fornecido")
            return False
            
        if not admin_id:
            print("\n❌ Admin ID não configurado!")
            print("   1. Envie mensagem para seu bot")
            print("   2. Acesse: https://api.telegram.org/bot<TOKEN>/getUpdates")
            print("   3. Copie o 'id' do campo 'from'")
            return False
        
        print("\n✅ Configuração parece correta!")
        
        # Teste de conexão
        print("\n🔗 Testando conexão...")
        try:
            import requests
            url = f"https://api.telegram.org/bot{token}/getMe"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                bot_info = response.json()
                if bot_info.get('ok'):
                    bot_name = bot_info['result']['first_name']
                    bot_username = bot_info['result']['username']
                    print(f"✅ Bot conectado: {bot_name} (@{bot_username})")
                    
                    # Teste de mensagem
                    print("\n📤 Enviando mensagem de teste...")
                    message = "🤖 XKit Telegram Test\\n✅ Configuração funcionando!"
                    
                    send_url = f"https://api.telegram.org/bot{token}/sendMessage"
                    data = {
                        'chat_id': admin_id,
                        'text': message,
                        'parse_mode': 'Markdown'
                    }
                    
                    send_response = requests.post(send_url, json=data, timeout=5)
                    
                    if send_response.status_code == 200 and send_response.json().get('ok'):
                        print("✅ Mensagem de teste enviada com sucesso!")
                        print("📱 Verifique seu Telegram!")
                        return True
                    else:
                        print(f"❌ Erro ao enviar mensagem: {send_response.text}")
                        return False
                else:
                    print("❌ Token inválido - bot não autenticado")
                    return False
            else:
                print(f"❌ Erro de conexão: HTTP {response.status_code}")
                return False
                
        except ImportError:
            print("⚠️  requests não disponível - instale com: pip install requests")
            return False
        except Exception as e:
            print(f"❌ Erro de conexão: {e}")
            return False
            
    except json.JSONDecodeError as e:
        print(f"❌ Erro ao ler configuração: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    success = test_telegram_config()
    sys.exit(0 if success else 1)