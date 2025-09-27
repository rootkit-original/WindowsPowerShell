#!/usr/bin/env python3
"""
Teste rápido do MCP Server Telegram
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "Scripts"))

import asyncio

async def test_mcp_servers():
    try:
        from xkit.mcp.client import XKitMCPClient
        
        client = XKitMCPClient()
        servers = await client.list_servers()
        
        print('🔌 MCP Servers configurados:')
        for name, info in servers.items():
            enabled = info.get('enabled', False)
            status = '✅' if enabled else '❌'
            desc = info.get('description', 'N/A')
            print(f'   {status} {name}: {desc}')
        
        if 'telegram-bot' in servers:
            print('\n📱 Servidor Telegram-Bot encontrado!')
            telegram_info = servers['telegram-bot']
            print(f'   Módulo: {telegram_info.get("module", "N/A")}')
            print(f'   Classe: {telegram_info.get("class", "N/A")}')
            print(f'   Habilitado: {telegram_info.get("enabled", False)}')
            
            # Tentar listar ferramentas do servidor Telegram
            try:
                print('\n🛠️ Testando ferramentas do servidor Telegram...')
                tools = await client.call_tool("telegram-bot", "list_tools", {})
                if tools:
                    print(f'   ✅ {len(tools)} ferramentas disponíveis')
                else:
                    print('   ⚠️ Nenhuma ferramenta retornada')
            except Exception as e:
                print(f'   ❌ Erro ao acessar ferramentas: {e}')
        else:
            print('\n❌ Servidor Telegram-Bot não encontrado na configuração')
        
        return True
        
    except Exception as e:
        print(f'❌ Erro: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(test_mcp_servers())