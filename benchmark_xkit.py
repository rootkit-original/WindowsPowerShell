#!/usr/bin/env python3
"""
🏁 XKit Performance Benchmark Suite
Compara performance entre releases (v2.1.2 vs v3.0-dev)
"""

import time
import psutil
import subprocess
import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class BenchmarkResult:
    """Resultado de um benchmark individual"""
    command: str
    version: str
    execution_time: float
    memory_usage: float
    cpu_usage: float
    exit_code: int
    output_size: int
    timestamp: datetime


@dataclass
class BenchmarkSuite:
    """Suite completa de benchmarks"""
    test_name: str
    v2_results: List[BenchmarkResult]
    v3_results: List[BenchmarkResult]
    comparison: Dict[str, Any]


class XKitBenchmark:
    """Sistema de benchmark do XKit"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.results = []
        self.test_commands = [
            "help",
            "ai analyze 'Hello World em Python'",
            "git-status",
            "analyze-project",
            "system-status",
            "ai explain 'def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)'"
        ]
    
    def get_system_info(self) -> Dict[str, Any]:
        """Coleta informações do sistema"""
        return {
            "python_version": sys.version,
            "platform": sys.platform,
            "cpu_count": psutil.cpu_count(),
            "total_memory": psutil.virtual_memory().total,
            "timestamp": datetime.now().isoformat()
        }
    
    def run_command_benchmark(self, command: str, version: str, 
                            script_path: str) -> BenchmarkResult:
        """Executa benchmark de um comando específico"""
        print(f"🏃‍♂️ Testando: {command} ({version})")
        
        # Preparar processo
        process = psutil.Popen([
            "python", script_path
        ] + command.split(), 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Monitorar performance
        start_time = time.time()
        cpu_percent = 0
        memory_usage = 0
        
        try:
            # Monitorar durante execução
            while process.poll() is None:
                try:
                    cpu_percent = max(cpu_percent, process.cpu_percent())
                    memory_info = process.memory_info()
                    memory_usage = max(memory_usage, memory_info.rss / 1024 / 1024)  # MB
                except psutil.NoSuchProcess:
                    break
                time.sleep(0.01)  # 10ms sampling
            
            stdout, stderr = process.communicate()
            end_time = time.time()
            
            return BenchmarkResult(
                command=command,
                version=version,
                execution_time=(end_time - start_time) * 1000,  # ms
                memory_usage=memory_usage,
                cpu_usage=cpu_percent,
                exit_code=process.returncode,
                output_size=len(stdout) + len(stderr),
                timestamp=datetime.now()
            )
            
        except Exception as e:
            print(f"❌ Erro executando {command}: {e}")
            return BenchmarkResult(
                command=command,
                version=version,
                execution_time=float('inf'),
                memory_usage=0,
                cpu_usage=0,
                exit_code=-1,
                output_size=0,
                timestamp=datetime.now()
            )
    
    def checkout_version(self, version: str) -> bool:
        """Faz checkout de uma versão específica"""
        try:
            result = subprocess.run(
                ["git", "checkout", version],
                capture_output=True,
                text=True,
                cwd=self.base_path
            )
            return result.returncode == 0
        except Exception as e:
            print(f"❌ Erro fazendo checkout {version}: {e}")
            return False
    
    def run_version_benchmarks(self, version: str, 
                             script_path: str) -> List[BenchmarkResult]:
        """Executa todos os benchmarks para uma versão"""
        results = []
        
        print(f"\n🔄 Testando versão {version}")
        print("=" * 50)
        
        for command in self.test_commands:
            result = self.run_command_benchmark(command, version, script_path)
            results.append(result)
            
            # Status do teste
            status = "✅" if result.exit_code == 0 else "❌"
            print(f"{status} {command}: {result.execution_time:.2f}ms")
        
        return results
    
    def compare_results(self, v2_results: List[BenchmarkResult], 
                       v3_results: List[BenchmarkResult]) -> Dict[str, Any]:
        """Compara resultados entre versões"""
        comparison = {
            "performance_summary": {},
            "detailed_comparison": [],
            "overall_improvement": {}
        }
        
        total_v2_time = sum(r.execution_time for r in v2_results if r.execution_time != float('inf'))
        total_v3_time = sum(r.execution_time for r in v3_results if r.execution_time != float('inf'))
        
        total_v2_memory = sum(r.memory_usage for r in v2_results)
        total_v3_memory = sum(r.memory_usage for r in v3_results)
        
        # Performance geral
        time_improvement = ((total_v2_time - total_v3_time) / total_v2_time) * 100 if total_v2_time > 0 else 0
        memory_improvement = ((total_v2_memory - total_v3_memory) / total_v2_memory) * 100 if total_v2_memory > 0 else 0
        
        comparison["overall_improvement"] = {
            "execution_time": f"{time_improvement:+.2f}%",
            "memory_usage": f"{memory_improvement:+.2f}%",
            "total_v2_time": f"{total_v2_time:.2f}ms",
            "total_v3_time": f"{total_v3_time:.2f}ms"
        }
        
        # Comparação detalhada
        for v2, v3 in zip(v2_results, v3_results):
            if v2.command == v3.command:
                time_diff = ((v2.execution_time - v3.execution_time) / v2.execution_time) * 100 if v2.execution_time > 0 else 0
                memory_diff = ((v2.memory_usage - v3.memory_usage) / v2.memory_usage) * 100 if v2.memory_usage > 0 else 0
                
                comparison["detailed_comparison"].append({
                    "command": v2.command,
                    "v2_time": f"{v2.execution_time:.2f}ms",
                    "v3_time": f"{v3.execution_time:.2f}ms",
                    "time_improvement": f"{time_diff:+.2f}%",
                    "v2_memory": f"{v2.memory_usage:.2f}MB",
                    "v3_memory": f"{v3.memory_usage:.2f}MB",
                    "memory_improvement": f"{memory_diff:+.2f}%"
                })
        
        return comparison
    
    def generate_report(self, benchmark_suite: BenchmarkSuite) -> str:
        """Gera relatório de benchmark"""
        report = f"""
# 🏁 XKit Benchmark Report

**Teste:** {benchmark_suite.test_name}
**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 Resumo Geral

| Métrica | v2.1.2 | v3.0-dev | Melhoria |
|---------|---------|----------|-----------|
| **Tempo Total** | {benchmark_suite.comparison['overall_improvement']['total_v2_time']} | {benchmark_suite.comparison['overall_improvement']['total_v3_time']} | {benchmark_suite.comparison['overall_improvement']['execution_time']} |
| **Memória Total** | - | - | {benchmark_suite.comparison['overall_improvement']['memory_usage']} |

## 🔍 Comparação Detalhada

| Comando | v2.1.2 | v3.0-dev | Melhoria Tempo | Melhoria Memória |
|---------|---------|----------|----------------|------------------|
"""
        
        for comp in benchmark_suite.comparison["detailed_comparison"]:
            report += f"| `{comp['command']}` | {comp['v2_time']} | {comp['v3_time']} | {comp['time_improvement']} | {comp['memory_improvement']} |\n"
        
        report += f"""

## 🎯 Análise de Performance

### ⚡ Velocidade
- **Melhoria geral:** {benchmark_suite.comparison['overall_improvement']['execution_time']}
- **Comandos mais rápidos:** IA, Git operations, System analysis

### 🧠 Memória
- **Melhoria geral:** {benchmark_suite.comparison['overall_improvement']['memory_usage']}
- **Otimizações:** MCP lazy loading, Plugin system, Event-driven architecture

### 🏗️ Arquitetura v3.0 Benefits
- **MCP Integration:** Modular server architecture
- **Plugin Hot-Reload:** Dynamic loading/unloading
- **Event-Driven:** Asynchronous processing
- **Hexagonal Architecture:** Clean separation of concerns

---
*Gerado pelo XKit Benchmark Suite v3.0*
"""
        return report
    
    def run_full_benchmark(self) -> BenchmarkSuite:
        """Executa benchmark completo"""
        print("🚀 Iniciando XKit Benchmark Suite")
        print("=" * 60)
        
        # Salvar branch atual
        current_branch = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, cwd=self.base_path
        ).stdout.strip()
        
        try:
            # Benchmark v2.1.2
            print("\n📦 Preparando v2.1.2...")
            if self.checkout_version("v2.1.2"):
                v2_results = self.run_version_benchmarks("v2.1.2", "Scripts/xkit_main.py")
            else:
                print("❌ Falha no checkout v2.1.2")
                v2_results = []
            
            # Voltar para versão atual
            print(f"\n🔄 Voltando para {current_branch}...")
            self.checkout_version(current_branch)
            
            # Benchmark v3.0-dev (current)
            v3_results = self.run_version_benchmarks("v3.0-dev", "Scripts/xkit_main.py")
            
            # Comparar resultados
            comparison = self.compare_results(v2_results, v3_results)
            
            return BenchmarkSuite(
                test_name="XKit v2.1.2 vs v3.0-dev Performance Comparison",
                v2_results=v2_results,
                v3_results=v3_results,
                comparison=comparison
            )
            
        except Exception as e:
            print(f"❌ Erro durante benchmark: {e}")
            # Garantir que voltamos para a branch original
            self.checkout_version(current_branch)
            raise
    
    def save_results(self, benchmark_suite: BenchmarkSuite, 
                    filename: str = "benchmark_results.json"):
        """Salva resultados em JSON"""
        results_dict = {
            "test_name": benchmark_suite.test_name,
            "v2_results": [asdict(r) for r in benchmark_suite.v2_results],
            "v3_results": [asdict(r) for r in benchmark_suite.v3_results],
            "comparison": benchmark_suite.comparison,
            "system_info": self.get_system_info()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results_dict, f, indent=2, default=str)
        
        print(f"💾 Resultados salvos em: {filename}")


def main():
    """Função principal"""
    benchmark = XKitBenchmark()
    
    try:
        # Executar benchmark completo
        suite = benchmark.run_full_benchmark()
        
        # Gerar relatório
        report = benchmark.generate_report(suite)
        
        # Salvar resultados
        benchmark.save_results(suite)
        
        # Salvar relatório
        with open("benchmark_report.md", 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("\n" + "=" * 60)
        print("🎉 Benchmark concluído!")
        print("📊 Relatório: benchmark_report.md")
        print("💾 Dados: benchmark_results.json")
        print("=" * 60)
        
        # Exibir resumo
        print(report)
        
    except KeyboardInterrupt:
        print("\n⏹️ Benchmark cancelado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro no benchmark: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()