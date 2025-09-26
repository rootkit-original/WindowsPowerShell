#!/usr/bin/env python3
"""
Test prompt personalizado e podman-compose integration
"""

import subprocess
import os

def test_prompt_functionality():
    """Testa se o prompt vai funcionar corretamente"""
    print("🎯 Testando funcionalidades do prompt personalizado...")
    
    # Test git command
    try:
        result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], 
                               capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            branch = result.stdout.strip()
            print(f"✅ Git branch detectada: {branch}")
        else:
            print("ℹ️  Não é um repositório Git (normal)")
    except Exception as e:
        print(f"⚠️  Git não disponível: {e}")
    
    # Test environment variables
    user = os.getenv('USERNAME', 'unknown')
    computer = os.getenv('COMPUTERNAME', 'unknown')
    print(f"✅ Usuário: {user}")
    print(f"✅ Computador: {computer}")
    
    # Test podman-compose
    try:
        result = subprocess.run(['podman-compose', '--version'], 
                               capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Podman-compose: {version}")
        else:
            print("❌ Podman-compose não disponível")
    except Exception as e:
        print(f"❌ Podman-compose erro: {e}")
    
    print(f"\n🎨 Exemplo do prompt esperado:")
    print(f"{user}@{computer} [main] ~/Documents/WindowsPowerShell")
    print("$ ")

if __name__ == "__main__":
    test_prompt_functionality()