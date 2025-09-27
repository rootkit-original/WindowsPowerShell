# 📊 XKit Project Analyzer Plugin

## 📋 Visão Geral

O **Project Analyzer Plugin** é um dos plugins centrais do XKit v3.0, responsável por analisar a qualidade e estrutura de projetos em diretórios `.xkit`. Ele fornece análises detalhadas com pontuação de qualidade, sugestões de melhoria e insights inteligentes.

## 🎯 Funcionalidades

### ✨ **Análise Completa de Projetos**
- 🔍 **Detecção Automática de Tipos**: Python, Node.js, Rust, Go, Java, C#, TypeScript
- 📊 **Pontuação de Qualidade**: Escala 0-10 baseada em múltiplos critérios
- 🤖 **Análise IA**: Integração com Gemini AI para insights avançados
- 📈 **Métricas Detalhadas**: Tamanho, arquivos, documentação, testes
- 🔧 **Sugestões Inteligentes**: Recomendações para melhorar o projeto

### 📁 **Detecção Inteligente**
- ✅ **Arquivos Essenciais**: README, LICENSE, CONTRIBUTING, CHANGELOG
- 📚 **Documentação**: Markdown, reStructuredText, AsciiDoc
- 🧪 **Testes**: Detecção automática de frameworks de teste
- ⚙️ **Configuração**: Package managers, build tools, CI/CD

### 🏗️ **Arquitetura Plugin**
- 🧩 **Plugin Base**: Herda de `XKitCorePlugin`
- 📡 **Event-Driven**: Publica eventos durante análise
- 🔌 **Serviços Integrados**: AI Service, Display Service
- 🔄 **Hot Reload**: Suporta recarregamento dinâmico

## 🚀 Comandos Disponíveis

### `analyze-project`
Executa análise completa de um projeto específico.

```powershell
# Analisar projeto atual
xkit analyze-project

# Analisar projeto específico
xkit analyze-project "C:\Users\Dev\MeuProjeto"
```

**Saída:**
- 📊 Pontuação geral (0-10)
- 📁 Tipo de projeto detectado
- 📈 Métricas detalhadas
- 🤖 Insights IA (se disponível)
- ❌ Issues encontrados
- 💡 Sugestões de melhoria

### `scan-xkit-projects`
Escaneia diretório em busca de projetos `.xkit` e analisa todos.

```powershell
# Escanear diretório atual
xkit scan-xkit-projects

# Escanear diretório específico
xkit scan-xkit-projects "C:\Users\Dev\Projetos"
```

**Saída:**
- 📂 Lista de projetos encontrados
- 📊 Resumo de pontuação para cada
- 🎯 Visão geral comparativa

### `project-score`
Retorna apenas a pontuação do projeto (útil para automação).

```powershell
# Score do projeto atual
xkit project-score

# Score de projeto específico  
xkit project-score "C:\Path\To\Project"
```

**Saída:**
- 📊 Pontuação numérica (0.0-10.0)

## 🏗️ Arquitetura Técnica

### 📦 **Estruturas de Dados**

#### `ProjectType` (Enum)
```python
class ProjectType(Enum):
    PYTHON = "python"
    NODE_JS = "nodejs" 
    RUST = "rust"
    GO = "go"
    JAVA = "java"
    C_SHARP = "csharp"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    UNKNOWN = "unknown"
```

#### `ProjectFile` (DataClass)
```python
@dataclass
class ProjectFile:
    name: str           # Nome do arquivo
    path: str           # Caminho completo
    size: int           # Tamanho em bytes
    is_essential: bool  # É arquivo essencial?
    category: str       # Categoria (docs, config, source, test)
```

#### `ProjectMetrics` (DataClass)
```python
@dataclass
class ProjectMetrics:
    total_files: int        # Total de arquivos
    total_size: int         # Tamanho total
    documentation_files: int # Arquivos de documentação
    config_files: int       # Arquivos de configuração
    source_files: int       # Arquivos de código fonte
    test_files: int         # Arquivos de teste
    has_git: bool          # Tem controle Git?
    has_readme: bool       # Tem README?
    has_license: bool      # Tem LICENSE?
    has_contributing: bool # Tem CONTRIBUTING?
    has_tests: bool        # Tem testes?
```

#### `ProjectAnalysisResult` (DataClass)
```python
@dataclass
class ProjectAnalysisResult:
    project_path: str           # Caminho do projeto
    project_type: ProjectType   # Tipo detectado
    metrics: ProjectMetrics     # Métricas calculadas
    score: float               # Pontuação (0-10)
    issues: List[str]          # Problemas encontrados
    suggestions: List[str]     # Sugestões de melhoria
    files: List[ProjectFile]   # Lista de arquivos
    ai_insights: Optional[str] # Insights IA (opcional)
```

### 🔧 **Algoritmo de Pontuação**

```python
# Sistema de pontuação ponderada
base_score = 0.0

# Arquivos Essenciais (0-3 pontos)
if has_readme: base_score += 1.0
if has_license: base_score += 0.5  
if has_contributing: base_score += 0.5
if has_changelog: base_score += 0.5
if has_gitignore: base_score += 0.5

# Código Fonte (0-3 pontos)  
source_ratio = source_files / total_files
base_score += min(3.0, source_ratio * 4.0)

# Testes (0-2 pontos)
if has_tests:
    test_ratio = test_files / source_files if source_files > 0 else 0
    base_score += min(2.0, test_ratio * 10.0)

# Documentação (0-1.5 pontos)
doc_ratio = documentation_files / total_files  
base_score += min(1.5, doc_ratio * 5.0)

# Estrutura (0-0.5 pontos)
if total_files >= 10: base_score += 0.5

# IA Bonus (0-1 ponto adicional)
if ai_available and project_follows_best_practices:
    base_score += ai_bonus_score

final_score = min(10.0, base_score)
```

### 🔍 **Detecção de Tipos de Projeto**

```python
project_patterns = {
    ProjectType.PYTHON: [
        "requirements.txt", "setup.py", "pyproject.toml", 
        "Pipfile", "poetry.lock", "*.py"
    ],
    ProjectType.NODE_JS: [
        "package.json", "package-lock.json", "yarn.lock", "*.js"
    ],
    ProjectType.RUST: [
        "Cargo.toml", "Cargo.lock", "src/main.rs"
    ],
    ProjectType.GO: [
        "go.mod", "go.sum", "main.go", "*.go"  
    ],
    ProjectType.JAVA: [
        "pom.xml", "build.gradle", "gradlew", "*.java"
    ],
    ProjectType.C_SHARP: [
        "*.csproj", "*.sln", "project.json", "*.cs"
    ],
    ProjectType.TYPESCRIPT: [
        "tsconfig.json", "package.json", "*.ts"
    ]
}

def _detect_project_type(self, files: List[ProjectFile]) -> ProjectType:
    """Detecta o tipo do projeto baseado nos arquivos presentes"""
    file_names = [f.name.lower() for f in files]
    
    # Conta matches para cada tipo
    type_scores = {}
    for project_type, patterns in self.project_patterns.items():
        score = 0
        for pattern in patterns:
            if any(fnmatch.fnmatch(name, pattern) for name in file_names):
                score += 1
        type_scores[project_type] = score
    
    # Retorna o tipo com maior score
    if type_scores:
        return max(type_scores, key=type_scores.get)
    return ProjectType.UNKNOWN
```

## 🤖 Integração IA

### **Gemini AI Service**
```python
async def _get_ai_insights(self, result: ProjectAnalysisResult) -> str:
    """Obtém insights de IA sobre o projeto"""
    
    prompt = f\"\"\"
    Analise este projeto {result.project_type.value}:
    
    📊 Métricas:
    - Arquivos: {result.metrics.total_files}
    - Tamanho: {result.metrics.total_size} bytes
    - Documentação: {result.metrics.documentation_files}
    - Testes: {result.metrics.test_files}
    - Score Atual: {result.score}/10
    
    🔍 Issues: {', '.join(result.issues)}
    
    Forneça insights específicos para melhorar este projeto.
    \"\"\"
    
    try:
        response = await self.ai_service.analyze(prompt)
        return response
    except Exception as e:
        self.log_warning(f"AI analysis failed: {e}")
        return None
```

### **Sugestões Inteligentes**
```python
def _generate_suggestions(self, result: ProjectAnalysisResult) -> List[str]:
    """Gera sugestões baseadas na análise"""
    suggestions = []
    
    # README ausente
    if not result.metrics.has_readme:
        suggestions.append("📖 Adicionar README.md com descrição do projeto")
    
    # LICENSE ausente  
    if not result.metrics.has_license:
        suggestions.append("⚖️ Adicionar arquivo LICENSE para definir termos de uso")
        
    # Testes insuficientes
    if result.metrics.test_files == 0:
        suggestions.append("🧪 Implementar testes unitários e de integração")
        
    # Documentação insuficiente
    doc_ratio = result.metrics.documentation_files / result.metrics.total_files
    if doc_ratio < 0.1:
        suggestions.append("📚 Expandir documentação do projeto")
        
    # Estrutura de diretórios
    if result.metrics.total_files < 5:
        suggestions.append("🗂️ Organizar código em estrutura de diretórios")
    
    return suggestions
```

## 📊 Sistema de Display

### **Exibição de Resultados**
```python
async def _display_analysis_result(self, result: ProjectAnalysisResult):
    """Exibe resultado completo da análise"""
    
    # Cabeçalho
    self.display.section(f"📊 Análise do Projeto: {os.path.basename(result.project_path)}")
    
    # Informações básicas
    self.display.info(f"📁 Tipo: {result.project_type.value.upper()}")
    self.display.info(f"📂 Caminho: {result.project_path}")
    
    # Pontuação com cor
    score_emoji = "🟢" if result.score >= 7 else "🟡" if result.score >= 4 else "🔴"
    self.display.print_colored(
        f"{score_emoji} Pontuação: {result.score:.1f}/10",
        "success" if result.score >= 7 else "warning" if result.score >= 4 else "error"
    )
    
    # Métricas
    self.display.section("📈 Métricas")
    print(f"  📄 Total de arquivos: {result.metrics.total_files:,}")
    print(f"  💾 Tamanho total: {self._format_size(result.metrics.total_size)}")
    print(f"  📚 Documentação: {result.metrics.documentation_files}")
    print(f"  🧪 Testes: {result.metrics.test_files}")
    print(f"  🔧 Configuração: {result.metrics.config_files}")
    print(f"  💻 Código fonte: {result.metrics.source_files}")
    
    # Issues
    if result.issues:
        self.display.section("❌ Problemas Encontrados")
        for issue in result.issues:
            print(f"  • {issue}")
    
    # Sugestões
    if result.suggestions:
        self.display.section("💡 Sugestões de Melhoria") 
        for suggestion in result.suggestions:
            print(f"  • {suggestion}")
    
    # Insights IA
    if result.ai_insights:
        self.display.section("🤖 Insights IA")
        print(f"  {result.ai_insights}")

def _format_size(self, size_bytes: int) -> str:
    """Formata tamanho em bytes para leitura humana"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"
```

## 🔧 Configuração e Instalação

### **Registro do Plugin**
```python
# No plugin manager
plugin_manager.register_plugin(XKitProjectAnalyzerPlugin())

# Verificação de dependências
required_services = ["ai_service", "display_service", "file_system"]
for service in required_services:
    if not plugin_manager.has_service(service):
        raise PluginDependencyError(f"Required service not available: {service}")
```

### **Configuração**
```json
{
  "project_analyzer": {
    "enabled": true,
    "ai_integration": true,
    "max_file_scan": 10000,
    "timeout": 30,
    "score_thresholds": {
      "excellent": 8.0,
      "good": 6.0,
      "needs_improvement": 4.0
    }
  }
}
```

## 🧪 Testes

### **Unit Tests**
```python
@pytest.mark.asyncio
async def test_project_type_detection():
    plugin = XKitProjectAnalyzerPlugin()
    
    # Test Python project detection
    files = [
        ProjectFile("requirements.txt", "/path/requirements.txt", 100, True, "config"),
        ProjectFile("main.py", "/path/main.py", 500, True, "source")
    ]
    
    project_type = plugin._detect_project_type(files)
    assert project_type == ProjectType.PYTHON

@pytest.mark.asyncio 
async def test_scoring_algorithm():
    plugin = XKitProjectAnalyzerPlugin()
    
    metrics = ProjectMetrics(
        total_files=10,
        total_size=5000,
        documentation_files=2,
        config_files=3,
        source_files=4,
        test_files=1,
        has_git=True,
        has_readme=True,
        has_license=True,
        has_contributing=False,
        has_tests=True
    )
    
    score = plugin._calculate_score(metrics)
    assert 6.0 <= score <= 8.0  # Expected range
```

### **Integration Tests**
```python
@pytest.mark.integration
async def test_full_project_analysis():
    # Criar projeto de teste
    test_project = create_test_project()
    
    plugin = XKitProjectAnalyzerPlugin()
    await plugin.initialize()
    
    # Executar análise
    result = await plugin.analyze_project(test_project.path)
    
    # Verificar resultado
    assert result.score > 0
    assert result.project_type != ProjectType.UNKNOWN
    assert len(result.files) > 0
    assert result.metrics.total_files > 0
```

## 🚀 Performance

### **Otimizações**
- ⚡ **Scan Assíncrono**: Usa `asyncio` para scan paralelo de arquivos
- 🎯 **Filtros Inteligentes**: Ignora diretórios desnecessários (node_modules, .git, __pycache__)
- 💾 **Cache Inteligente**: Cache de resultados para análises repetidas
- 🔄 **Lazy Loading**: Carrega dados conforme necessário

### **Configuração de Performance**
```python
# Configurações de performance
PERFORMANCE_CONFIG = {
    "max_concurrent_scans": 10,
    "max_file_size_mb": 100,
    "cache_duration_minutes": 30,
    "ignored_directories": [
        ".git", "node_modules", "__pycache__", 
        ".venv", "venv", "target", "build"
    ]
}
```

## 📚 Exemplos de Uso

### **Análise Simples**
```python
# Usar o plugin programaticamente
plugin = XKitProjectAnalyzerPlugin()
await plugin.initialize()

result = await plugin.analyze_project("/path/to/project")
print(f"Score: {result.score}/10")
print(f"Type: {result.project_type}")
```

### **Análise em Lote**
```python
# Analisar múltiplos projetos
projects = ["/project1", "/project2", "/project3"]
results = []

for project_path in projects:
    result = await plugin.analyze_project(project_path)
    results.append(result)

# Ordenar por score
results.sort(key=lambda x: x.score, reverse=True)
```

### **Integração com CI/CD**
```bash
#!/bin/bash
# Script de CI para verificar qualidade do projeto

score=$(xkit project-score)
if (( $(echo "$score >= 7.0" | bc -l) )); then
    echo "✅ Project quality check passed: $score/10"
    exit 0
else
    echo "❌ Project quality check failed: $score/10"
    echo "💡 Run 'xkit analyze-project' for suggestions"
    exit 1
fi
```

## 🔗 Links Relacionados

- 📖 [Plugin Development Guide](../development/plugin-development.md)
- 🏗️ [XKit Architecture](../architecture/README.md)
- 🤖 [AI Service Documentation](../api/core-api.md#ai-service)
- 📡 [Event System](../api/event-api.md)

---

**📊 Project Analyzer Plugin** é uma ferramenta essencial do XKit v3.0 para manter alta qualidade em projetos de desenvolvimento, fornecendo análises inteligentes e sugestões práticas para melhoria contínua.