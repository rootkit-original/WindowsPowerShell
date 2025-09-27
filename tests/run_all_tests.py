#!/usr/bin/env python3
"""
🧪 XKit Test Runner - Executor de Todos os Testes
Executa todos os testes do XKit v3.0 de forma organizada
"""
import sys
import asyncio
import subprocess
import logging
from pathlib import Path
from typing import List, Dict, Tuple
import json
import time

# Add XKit path
XKIT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(XKIT_ROOT / "Scripts"))

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class XKitTestRunner:
    """Executor de testes do XKit v3.0"""
    
    def __init__(self):
        self.tests_dir = Path(__file__).parent
        self.results: Dict[str, Dict] = {}
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.skipped_tests = 0
    
    async def run_all_tests(self):
        """Executa todos os testes disponíveis"""
        print("🚀 XKit v3.0 Test Runner - Executando Todos os Testes")
        print("=" * 70)
        
        # Lista de testes para executar
        test_files = [
            ("test_gemini_fixed.py", "🤖 Gemini AI Integration", self._run_gemini_test),
            ("test_telegram.py", "📱 Telegram Basic Test", self._run_telegram_test),
            ("test_telegram_mcp.py", "🔌 Telegram MCP Server", self._run_mcp_test)
        ]
        
        # Verificar configuração antes dos testes
        print("\\n🔍 Verificando Configuração...")
        config_status = await self._check_configuration()
        
        if not config_status["config_exists"]:
            print("⚠️ Arquivo de configuração não encontrado!")
            print("📝 Crie ~/.xkit/config.json com as credenciais necessárias")
            print("\\n📚 Consulte tests/README.md para instruções detalhadas")
            return
        
        # Executar testes
        print(f"\\n🧪 Executando {len(test_files)} suítes de testes...")
        print("-" * 50)
        
        for test_file, description, test_func in test_files:
            self.total_tests += 1
            print(f"\\n{description}")
            print("=" * 30)
            
            start_time = time.time()
            
            try:
                result = await test_func(test_file)
                execution_time = time.time() - start_time
                
                self.results[test_file] = {
                    "description": description,
                    "result": result,
                    "execution_time": execution_time,
                    "status": "passed" if result.get("success", False) else "failed"
                }
                
                if result.get("success", False):
                    self.passed_tests += 1
                    print(f"✅ {description} - PASSOU ({execution_time:.2f}s)")
                else:
                    self.failed_tests += 1
                    print(f"❌ {description} - FALHOU ({execution_time:.2f}s)")
                    if "error" in result:
                        print(f"   Erro: {result['error']}")
                        
            except Exception as e:
                execution_time = time.time() - start_time
                self.failed_tests += 1
                print(f"💥 {description} - ERRO CRÍTICO ({execution_time:.2f}s)")
                print(f"   Exceção: {str(e)}")
                
                self.results[test_file] = {
                    "description": description,
                    "result": {"success": False, "error": str(e)},
                    "execution_time": execution_time,
                    "status": "error"
                }
        
        # Mostrar relatório final
        await self._show_final_report()
    
    async def _check_configuration(self) -> Dict[str, any]:
        """Verifica configuração do XKit"""
        config_path = Path.home() / ".xkit" / "config.json"
        
        status = {
            "config_exists": config_path.exists(),
            "gemini_configured": False,
            "telegram_configured": False
        }
        
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # Verificar Gemini
                if "ai" in config and "gemini" in config["ai"]:
                    status["gemini_configured"] = bool(config["ai"]["gemini"].get("api_key"))
                
                # Verificar Telegram
                if "telegram" in config:
                    telegram = config["telegram"]
                    status["telegram_configured"] = (
                        telegram.get("enabled", False) and
                        bool(telegram.get("token")) and
                        bool(telegram.get("admin_id"))
                    )
                
                print(f"   📄 Configuração: {'✅' if status['config_exists'] else '❌'}")
                print(f"   🤖 Gemini API: {'✅' if status['gemini_configured'] else '❌'}")
                print(f"   📱 Telegram: {'✅' if status['telegram_configured'] else '❌'}")
                
            except Exception as e:
                print(f"   ⚠️ Erro ao ler configuração: {e}")
        else:
            print("   ❌ Arquivo de configuração não encontrado")
        
        return status
    
    async def _run_gemini_test(self, test_file: str) -> Dict[str, any]:
        """Executa teste do Gemini AI"""
        try:
            # Executa o script Python
            result = subprocess.run(
                [sys.executable, str(self.tests_dir / test_file)],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            success = result.returncode == 0
            output = result.stdout if success else result.stderr
            
            # Parse da saída para extrair informações
            lines = output.split('\\n')
            models_tested = len([line for line in lines if "Testando" in line])
            models_working = len([line for line in lines if "✅" in line and "funcionando" in line])
            
            return {
                "success": success,
                "output": output,
                "models_tested": models_tested,
                "models_working": models_working,
                "returncode": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Timeout - teste demorou mais que 60s"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _run_telegram_test(self, test_file: str) -> Dict[str, any]:
        """Executa teste básico do Telegram"""
        try:
            result = subprocess.run(
                [sys.executable, str(self.tests_dir / test_file)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            success = result.returncode == 0
            output = result.stdout if success else result.stderr
            
            # Verificar se mensagem foi enviada
            message_sent = "mensagem enviada" in output.lower() or "message sent" in output.lower()
            
            return {
                "success": success,
                "output": output,
                "message_sent": message_sent,
                "returncode": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Timeout - teste demorou mais que 30s"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _run_mcp_test(self, test_file: str) -> Dict[str, any]:
        """Executa teste do MCP Server"""
        try:
            # Para o teste MCP, usamos um processo não-interativo
            # Modificamos o arquivo temporariamente para pular a entrada do usuário
            
            # Lê o arquivo original
            original_file = self.tests_dir / test_file
            temp_file = self.tests_dir / f"temp_{test_file}"
            
            with open(original_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove a parte interativa
            modified_content = content.replace(
                'input("\\n🔄 Pressione ENTER para continuar com os testes (Ctrl+C para sair)...")',
                'print("\\n🔄 Executando testes automaticamente...")'
            )
            
            # Salva arquivo temporário
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(modified_content)
            
            try:
                result = subprocess.run(
                    [sys.executable, str(temp_file)],
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                
                success = result.returncode == 0
                output = result.stdout if success else result.stderr
                
                # Contar testes executados
                tests_run = len([line for line in output.split('\\n') if "Teste " in line and ":" in line])
                tests_passed = len([line for line in output.split('\\n') if "✅" in line])
                
                return {
                    "success": success,
                    "output": output,
                    "tests_run": tests_run,
                    "tests_passed": tests_passed,
                    "returncode": result.returncode
                }
                
            finally:
                # Remove arquivo temporário
                if temp_file.exists():
                    temp_file.unlink()
            
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Timeout - teste demorou mais que 120s"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _show_final_report(self):
        """Mostra relatório final dos testes"""
        print("\\n" + "=" * 70)
        print("📊 RELATÓRIO FINAL DOS TESTES")
        print("=" * 70)
        
        print(f"\\n📈 Estatísticas:")
        print(f"   Total de Testes: {self.total_tests}")
        print(f"   ✅ Passou: {self.passed_tests}")
        print(f"   ❌ Falhou: {self.failed_tests}")
        print(f"   ⏭️ Pulados: {self.skipped_tests}")
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        print(f"   🎯 Taxa de Sucesso: {success_rate:.1f}%")
        
        print(f"\\n📋 Detalhes por Teste:")
        for test_file, result in self.results.items():
            status_emoji = "✅" if result["status"] == "passed" else "❌" if result["status"] == "failed" else "💥"
            print(f"   {status_emoji} {result['description']}")
            print(f"      Tempo: {result['execution_time']:.2f}s")
            
            # Detalhes específicos por tipo de teste
            if "gemini" in test_file.lower() and "models_tested" in result["result"]:
                print(f"      Modelos testados: {result['result']['models_tested']}")
                print(f"      Modelos funcionando: {result['result']['models_working']}")
            
            elif "telegram" in test_file.lower() and "message_sent" in result["result"]:
                print(f"      Mensagem enviada: {'✅' if result['result']['message_sent'] else '❌'}")
            
            elif "mcp" in test_file.lower() and "tests_run" in result["result"]:
                print(f"      Testes MCP: {result['result']['tests_passed']}/{result['result']['tests_run']}")
        
        # Recomendações
        print(f"\\n💡 Recomendações:")
        if self.failed_tests > 0:
            print("   • Verifique a configuração em ~/.xkit/config.json")
            print("   • Confirme se as credenciais estão corretas")
            print("   • Execute testes individuais para debugging")
        
        if success_rate == 100:
            print("   🎉 Todos os testes passaram! XKit está funcionando perfeitamente!")
        elif success_rate >= 66:
            print("   👍 A maioria dos testes passou. Pequenos ajustes podem ser necessários.")
        else:
            print("   ⚠️ Muitos testes falharam. Verifique a configuração e documentação.")
        
        print("\\n📚 Para mais informações, consulte:")
        print("   • tests/README.md - Documentação completa dos testes")
        print("   • docs/api/ - Documentação das APIs")
        print("   • TROUBLESHOOTING.md - Solução de problemas")


async def main():
    """Função principal"""
    runner = XKitTestRunner()
    await runner.run_all_tests()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\\n❌ Testes interrompidos pelo usuário")
    except Exception as e:
        print(f"\\n💥 Erro crítico no test runner: {e}")
        logger.exception("Erro crítico")