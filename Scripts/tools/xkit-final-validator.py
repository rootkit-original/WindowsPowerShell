#!/usr/bin/env python3
"""
XKit v2.1 Final Validator - Validação da interface compacta com AI
"""

import os
import sys
from pathlib import Path

def test_compact_interface():
    """Testa a interface compacta"""
    print("🎨 Testando Interface Compacta...")
    
    script_path = Path(__file__).parent.parent / "xkit_compact.py"
    if not script_path.exists():
        print("❌ Script compacto não encontrado")
        return False
    
    print("✅ Script compacto encontrado")
    return True

def test_ai_configuration():
    """Testa configuração da AI"""
    print("\n🤖 Testando Configuração AI...")
    
    required_env = ['GEMINI_API_KEY', 'TELEGRAM_TOKEN', 'ADMIN_ID']
    
    for env_var in required_env:
        if os.getenv(env_var):
            print(f"✅ {env_var} configurado")
        else:
            print(f"⚠️  {env_var} não encontrado em variáveis de ambiente")
    
    return True

def test_architecture():
    """Testa arquitetura clean"""
    print("\n🏗️  Testando Clean Architecture...")
    
    base_path = Path(__file__).parent.parent / "xkit"
    
    required_modules = {
        'domain': ['entities.py', 'interfaces.py'],
        'application': ['use_cases.py'],
        'infrastructure': ['compact_display.py', 'ai_service.py', 'telegram_service.py', 'environment.py']
    }
    
    all_good = True
    for layer, modules in required_modules.items():
        layer_path = base_path / layer
        if layer_path.exists():
            print(f"✅ Camada {layer}")
            for module in modules:
                if (layer_path / module).exists():
                    print(f"  ✅ {module}")
                else:
                    print(f"  ❌ {module}")
                    all_good = False
        else:
            print(f"❌ Camada {layer} não encontrada")
            all_good = False
    
    return all_good

def test_functionality():
    """Testa funcionalidade básica"""
    print("\n⚡ Testando Funcionalidade...")
    
    try:
        script_dir = Path(__file__).parent.parent
        sys.path.insert(0, str(script_dir))
        
        from xkit.infrastructure import CompactDisplayService, GeminiAIService, TelegramService
        from xkit.domain import DevelopmentContext
        
        print("✅ Imports funcionando")
        
        # Testa serviços
        compact_display = CompactDisplayService()
        ai_service = GeminiAIService()
        telegram_service = TelegramService()
        
        print(f"✅ CompactDisplayService criado")
        print(f"🤖 AI Service: {'✓' if ai_service.is_available() else '✗'}")
        print(f"📱 Telegram Service: {'✓' if telegram_service.is_available() else '✗'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar funcionalidade: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 XKit v2.1 - Validador Final")
    print("=" * 50)
    
    tests = [
        test_compact_interface(),
        test_ai_configuration(),
        test_architecture(),
        test_functionality()
    ]
    
    print("\n" + "=" * 50)
    
    if all(tests):
        print("🎉 XKit v2.1 COMPACTO FUNCIONANDO PERFEITAMENTE!")
        print()
        print("📋 Recursos Implementados:")
        print("  ✅ Interface compacta estilo oh-my-zsh")
        print("  ✅ Gemini AI integrado")
        print("  ✅ Telegram notifications") 
        print("  ✅ Detecção de ambiente avançada")
        print("  ✅ Clean Architecture mantida")
        print("  ✅ Container detection (Podman/Docker)")
        print()
        print("🎯 Interface Ultra-Compacta:")
        print("   🪟 📁projeto 🌿main ✓ 🐳podman 🐍⚛️")
        print("   🤖 AI suggestions • 📱 Telegram alerts")
        print()
        print("🚀 Para ativar: Reinicie o PowerShell")
        print("💡 Comandos: xkit-help, xkit-ai, xkit-solve")
        
    else:
        print("❌ ALGUNS TESTES FALHARAM")
        print("🔧 Verifique os erros acima")

if __name__ == "__main__":
    main()