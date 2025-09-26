#!/usr/bin/env python3
"""
🎯 XKit Gemini API Tester - Versão Corrigida
Testa com o formato correto de modelos (com prefixo models/)
"""

import requests
import json
from typing import Tuple, Optional, List


def test_model_with_correct_format(model_name: str, api_key: str) -> Tuple[bool, Optional[str], Optional[str], Optional[str]]:
    """
    Testa um modelo específico usando o formato correto com prefixo models/
    Retorna: (success, model_name, api_version, endpoint)
    """
    print(f"🧪 Testando {model_name}...")
    
    # Remove prefixo models/ se já existir e depois adiciona novamente
    clean_model = model_name.replace("models/", "")
    full_model_name = f"models/{clean_model}"
    
    # Testa diferentes versões da API
    for api_version in ["v1beta", "v1"]:
        endpoint = f"https://generativelanguage.googleapis.com/{api_version}/{full_model_name}:generateContent"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": "Responda em português: O que é inteligência artificial?"
                }]
            }],
            "generationConfig": {
                "temperature": 0.5,
                "maxOutputTokens": 100
            }
        }
        
        try:
            response = requests.post(
                f"{endpoint}?key={api_key}",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=20
            )
            
            print(f"  📡 {api_version}: {endpoint}")
            print(f"  🔍 Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and result['candidates']:
                    content = result['candidates'][0]['content']['parts'][0]['text']
                    print(f"  ✅ {api_version} FUNCIONOU!")
                    print(f"  🤖 Resposta: {content.strip()}")
                    return True, full_model_name, api_version, endpoint
                else:
                    print(f"  ⚠️  {api_version}: Resposta vazia")
            else:
                error_msg = ""
                try:
                    error_data = response.json()
                    if 'error' in error_data:
                        error_msg = error_data['error'].get('message', 'N/A')[:100]
                except:
                    error_msg = response.text[:100]
                
                print(f"  ❌ {api_version}: {response.status_code} - {error_msg}")
                
        except Exception as e:
            print(f"  ❌ {api_version}: Exception - {e}")
    
    return False, None, None, None


def test_priority_models() -> List[Tuple[str, str, str]]:
    """Testa modelos em ordem de prioridade"""
    api_key = "AIzaSyAad7j529fLDYA9IiTabQIOQ5jVv-cdLuo"
    
    # Modelos em ordem de prioridade (mais rápidos primeiro)
    priority_models = [
        "gemini-1.5-flash-latest",
        "gemini-1.5-flash",
        "gemini-1.5-flash-002",
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-1.5-pro-latest", 
        "gemini-1.5-pro",
        "gemini-1.5-pro-002",
        "gemini-2.5-pro",
        "gemini-pro"
    ]
    
    working_models = []
    
    print("🎯 Testando modelos prioritários com formato correto...")
    print("=" * 60)
    
    for model in priority_models:
        success, full_name, version, endpoint = test_model_with_correct_format(model, api_key)
        if success:
            working_models.append((full_name, version, endpoint))
            print(f"🎉 PRIMEIRO MODELO FUNCIONANDO: {full_name}")
            break  # Para no primeiro que funcionar
        print()
    
    return working_models


def test_all_from_api_list() -> List[Tuple[str, str, str]]:
    """Testa todos os modelos Flash e Pro da lista da API"""
    api_key = "AIzaSyAad7j529fLDYA9IiTabQIOQ5jVv-cdLuo"
    
    print("🔍 Listando e testando modelos da API...")
    
    # Lista modelos disponíveis
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'models' in data:
                all_models = [model['name'] for model in data['models']]
                
                # Filtra Flash e Pro
                flash_models = [m for m in all_models if 'flash' in m.lower()]
                pro_models = [m for m in all_models if 'pro' in m.lower() and 'flash' not in m.lower()]
                
                print(f"⚡ {len(flash_models)} modelos Flash encontrados")
                print(f"🎓 {len(pro_models)} modelos Pro encontrados")
                print()
                
                working_models = []
                
                # Testa Flash primeiro (mais rápido)
                print("🧪 Testando modelos Flash...")
                for model in flash_models[:5]:  # Testa os 5 primeiros
                    success, full_name, version, endpoint = test_model_with_correct_format(model, api_key)
                    if success:
                        working_models.append((full_name, version, endpoint))
                        print(f"✅ Flash funcionando: {full_name}")
                        break
                    print()
                
                # Se não achou Flash, testa Pro
                if not working_models:
                    print("🎯 Flash não funcionou, testando Pro...")
                    for model in pro_models[:5]:  # Testa os 5 primeiros
                        success, full_name, version, endpoint = test_model_with_correct_format(model, api_key)
                        if success:
                            working_models.append((full_name, version, endpoint))
                            print(f"✅ Pro funcionando: {full_name}")
                            break
                        print()
                
                return working_models
        else:
            print(f"❌ Erro ao listar modelos: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    return []


def main():
    """Função principal"""
    print("🚀 XKIT GEMINI API TESTER - FORMATO CORRETO")
    print("=" * 60)
    print("🎯 Testando com prefixo models/ baseado na API")
    print("=" * 60)
    
    # Teste 1: Modelos prioritários
    print("\n1️⃣  TESTE PRIORITÁRIO")
    print("-" * 40)
    
    working_models = test_priority_models()
    
    if working_models:
        model, version, endpoint = working_models[0]
        print(f"\n🎉 SUCESSO! Modelo funcionando:")
        print(f"✅ Modelo: {model}")
        print(f"🔧 API Version: v{version}")
        print(f"🔗 Endpoint: {endpoint}")
        
        print(f"\n📝 Configuração para ai_service.py:")
        print(f'MODEL_NAME = "{model}"')
        print(f'BASE_URL = "https://generativelanguage.googleapis.com/{version}"')
        
    else:
        print("\n❌ Teste prioritário falhou")
        
        # Teste 2: Todos da lista da API
        print("\n2️⃣  TESTE COMPLETO DA API")
        print("-" * 40)
        
        working_models = test_all_from_api_list()
        
        if working_models:
            model, version, endpoint = working_models[0]
            print(f"\n🎉 ENCONTROU modelo funcionando:")
            print(f"✅ Modelo: {model}")
            print(f"🔧 API Version: {version}")
            print(f"🔗 Endpoint: {endpoint}")
        else:
            print("\n❌ Nenhum modelo funcionou")
            print("💡 Possível problema de permissões ou billing")
    
    print(f"\n🏁 Teste concluído!")


if __name__ == "__main__":
    main()