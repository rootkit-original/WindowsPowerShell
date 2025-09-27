#!/usr/bin/env python3
"""
Diagnóstico Completo do Sistema Telegram
Valida todas as camadas: Direto, MCP, Bot Polling
"""
import sys
import asyncio
import time
from pathlib import Path
from datetime import datetime

# Add XKit path
XKIT_ROOT = Path(__file__).parent
sys.path.insert(0, str(XKIT_ROOT / "Scripts"))

try:
    from xkit.infrastructure.config import XKitConfigService
    from xkit.infrastructure.telegram_service import TelegramService
    from xkit.mcp.client import XKitMCPClient
except ImportError as e:
    print(f"❌ Erro de import: {e}")
    sys.exit(1)


class TelegramDiagnostics:
    """Diagnóstico completo do sistema Telegram"""
    
    def __init__(self):
        self.config = XKitConfigService()
        self.telegram_config = self.config.get_section("telegram")
        
        if not self.telegram_config:
            print("❌ Configuração Telegram não encontrada!")
            sys.exit(1)
            
        self.token = self.telegram_config.get("token")
        self.admin_id = self.telegram_config.get("admin_id")
        self.mcp_client = XKitMCPClient()
        
    def test_layer_1_config(self) -> bool:
        """Camada 1: Configuração"""
        print("🔍 [LAYER 1] Testando Configuração...")
        
        if not self.token:
            print("❌ Token não configurado")
            return False
            
        if not self.admin_id:
            print("❌ Admin ID não configurado")
            return False
            
        print("✅ Configuração OK")
        return True
    
    def test_layer_2_direct_service(self) -> bool:
        """Camada 2: Serviço Direto Telegram"""
        print("📡 [LAYER 2] Testando Serviço Direto...")
        
        try:
            service = TelegramService(self.token, self.admin_id)
            
            if not service.is_available():
                print("❌ Serviço não disponível")
                return False
            
            # Teste de envio direto
            timestamp = datetime.now().strftime("%H:%M:%S")
            message = f"🔹 [LAYER 2] Teste Direto - {timestamp}"
            
            success = service._send_message(message)
            
            if success:
                print("✅ Serviço Direto OK")
                return True
            else:
                print("❌ Falha no envio direto")
                return False
                
        except Exception as e:
            print(f"❌ Erro no serviço direto: {e}")
            return False
    
    async def test_layer_3_mcp_server(self) -> bool:
        """Camada 3: MCP Server"""
        print("🔌 [LAYER 3] Testando MCP Server...")
        
        try:
            # Verificar se server está disponível
            servers = await self.mcp_client.list_servers()
            
            if 'telegram-bot' not in servers:
                print("❌ MCP Server telegram-bot não encontrado")
                return False
            
            # Teste de envio via MCP
            timestamp = datetime.now().strftime("%H:%M:%S")
            message = f"🔸 [LAYER 3] Teste MCP - {timestamp}"
            
            result = await self.mcp_client.call_tool('telegram-bot', 'send-message', {
                'message': message,
                'format': 'text'
            })
            
            if result.get('success'):
                print("✅ MCP Server OK")
                return True
            else:
                print(f"❌ Falha no MCP: {result}")
                return False
                
        except Exception as e:
            print(f"❌ Erro no MCP: {e}")
            return False
    
    async def test_layer_4_bot_status(self) -> bool:
        """Camada 4: Status do Bot"""
        print("🤖 [LAYER 4] Testando Status do Bot...")
        
        try:
            result = await self.mcp_client.call_tool('telegram-bot', 'check-bot-status', {
                'detailed': True,
                'restart_if_offline': False
            })
            
            if result.get('success'):
                status = result.get('result', {})
                online = status.get('status') == 'online' or status.get('online', False)
                
                if online:
                    print("✅ Bot Status OK")
                    print(f"   📊 Status: {status.get('status', 'unknown')}")
                    return True
                else:
                    print("❌ Bot offline")
                    print(f"   📊 Status: {status}")
                    return False
            else:
                print(f"❌ Erro verificando status: {result}")
                return False
                
        except Exception as e:
            print(f"❌ Erro no status do bot: {e}")
            return False
    
    async def run_full_diagnostics(self):
        """Executa diagnóstico completo"""
        print("🔬 XKit Telegram - Diagnóstico Completo")
        print("=" * 50)
        
        results = {}
        
        # Layer 1: Config
        results['config'] = self.test_layer_1_config()
        
        # Layer 2: Direct Service  
        results['direct'] = self.test_layer_2_direct_service()
        
        # Layer 3: MCP Server
        results['mcp'] = await self.test_layer_3_mcp_server()
        
        # Layer 4: Bot Status
        results['bot'] = await self.test_layer_4_bot_status()
        
        # Resultado final
        print("\n📊 RESULTADOS DO DIAGNÓSTICO")
        print("=" * 30)
        
        all_ok = True
        for layer, status in results.items():
            emoji = "✅" if status else "❌"
            print(f"{emoji} {layer.upper()}: {'OK' if status else 'FALHA'}")
            if not status:
                all_ok = False
        
        print(f"\n🎯 RESULTADO GERAL: {'✅ SISTEMA OK' if all_ok else '❌ PROBLEMAS DETECTADOS'}")
        
        if not all_ok:
            print("\n🔧 AÇÕES SUGERIDAS:")
            if not results['config']:
                print("   • Verificar configuração em Scripts/xkit/config/config.json")
            if not results['direct']:
                print("   • Verificar token e conectividade de rede")
            if not results['mcp']:
                print("   • Reiniciar MCP server ou verificar inicialização")
            if not results['bot']:
                print("   • Reiniciar sistema de polling do bot")
        
        return all_ok


async def main():
    """Função principal"""
    diagnostics = TelegramDiagnostics()
    
    try:
        success = await diagnostics.run_full_diagnostics()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 Diagnóstico interrompido")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())