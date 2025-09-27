"""
XKit Project Analyzer Plugin
Analisa estrutura de projetos em diretórios .xkit e gera relatórios com pontuação
"""
import os
import json
import asyncio
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from .base import XKitCorePlugin
from ..infrastructure.ai_service import GeminiAIService
from ..infrastructure.display import DisplayService


class ProjectType(Enum):
    """Tipos de projetos detectados"""
    PYTHON = "python"
    NODE_JS = "nodejs"
    RUST = "rust"
    GO = "go"
    JAVA = "java"
    C_SHARP = "csharp"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    UNKNOWN = "unknown"


@dataclass
class ProjectFile:
    """Representa um arquivo do projeto"""
    name: str
    path: str
    size: int
    is_essential: bool = False
    category: str = "other"


@dataclass
class ProjectMetrics:
    """Métricas calculadas do projeto"""
    total_files: int
    total_size: int
    documentation_files: int
    config_files: int
    source_files: int
    test_files: int
    has_git: bool
    has_readme: bool
    has_license: bool
    has_contributing: bool
    has_tests: bool


@dataclass
class ProjectAnalysisResult:
    """Resultado da análise do projeto"""
    project_path: str
    project_type: ProjectType
    metrics: ProjectMetrics
    score: float  # 0-10
    issues: List[str]
    suggestions: List[str]
    files: List[ProjectFile]
    ai_insights: Optional[str] = None


class XKitProjectAnalyzerPlugin(XKitCorePlugin):
    """Plugin para análise de projetos .xkit"""
    
    def __init__(self):
        super().__init__(
            name="project_analyzer",
            version="1.0.0",
            description="🔍 Analisa projetos em diretórios .xkit e gera relatórios de qualidade"
        )
        self.ai_service = GeminiAIService()
        self.display = DisplayService()
        
        # Patterns para detecção de tipos de projeto
        self.project_patterns = {
            ProjectType.PYTHON: ["requirements.txt", "setup.py", "pyproject.toml", "Pipfile", "poetry.lock"],
            ProjectType.NODE_JS: ["package.json", "package-lock.json", "yarn.lock"],
            ProjectType.RUST: ["Cargo.toml", "Cargo.lock"],
            ProjectType.GO: ["go.mod", "go.sum"],
            ProjectType.JAVA: ["pom.xml", "build.gradle", "gradlew"],
            ProjectType.C_SHARP: ["*.csproj", "*.sln", "project.json"],
            ProjectType.JAVASCRIPT: ["package.json", "webpack.config.js"],
            ProjectType.TYPESCRIPT: ["tsconfig.json", "package.json"]
        }
        
        # Arquivos essenciais para qualquer projeto
        self.essential_files = [
            "README.md", "README.rst", "README.txt",
            "LICENSE", "LICENSE.md", "LICENSE.txt",
            "CONTRIBUTING.md", "CHANGELOG.md", "CHANGES.md",
            ".gitignore", ".gitattributes"
        ]
        
        # Padrões de documentação
        self.documentation_patterns = [
            "*.md", "*.rst", "*.txt", "docs/", "documentation/",
            "*.adoc", "*.wiki"
        ]
        
        # Padrões de testes
        self.test_patterns = [
            "test_*.py", "*_test.py", "tests/", "test/",
            "*.test.js", "*.spec.js", "__tests__/",
            "*Test.java", "*Tests.cs", "test*.go"
        ]
    
    def get_commands(self) -> Dict[str, callable]:
        """Retorna os comandos do plugin"""
        return {
            "analyze-project": self.analyze_project_command,
            "scan-xkit-projects": self.scan_xkit_projects_command,
            "project-score": self.project_score_command
        }
    
    async def _initialize_services(self) -> None:
        """Inicializa os serviços do plugin"""
        self.register_service("project_analyzer", self)
    
    async def analyze_project_command(self, *args) -> None:
        """Comando para analisar um projeto específico"""
        try:
            project_path = args[0] if args else os.getcwd()
            
            # Verifica se é um diretório .xkit
            if not await self._is_xkit_directory(project_path):
                self.display.info("ℹ️  Este não é um diretório .xkit válido")
                return
            
            self.display.info(f"🔍 Analisando projeto em: {project_path}")
            
            # Executa a análise
            result = await self.analyze_project(project_path)
            
            # Exibe o relatório
            await self._display_analysis_result(result)
            
        except Exception as e:
            self.display.error(f"❌ Erro na análise: {str(e)}")
    
    async def scan_xkit_projects_command(self, *args) -> None:
        """Comando para escanear todos os projetos .xkit no diretório atual"""
        try:
            base_path = args[0] if args else os.getcwd()
            
            self.display.info(f"🔍 Procurando projetos .xkit em: {base_path}")
            
            # Encontra todos os diretórios .xkit
            xkit_projects = await self._find_xkit_projects(base_path)
            
            if not xkit_projects:
                self.display.warning("⚠️  Nenhum projeto .xkit encontrado")
                return
            
            self.display.success(f"📁 Encontrados {len(xkit_projects)} projetos .xkit")
            
            # Analisa cada projeto
            for project_path in xkit_projects:
                self.display.section(f"📂 {os.path.basename(project_path)}")
                result = await self.analyze_project(project_path)
                await self._display_summary_result(result)
            
        except Exception as e:
            self.display.error(f"❌ Erro no escaneamento: {str(e)}")
    
    async def project_score_command(self, *args) -> None:
        """Comando para mostrar apenas a pontuação do projeto"""
        try:
            project_path = args[0] if args else os.getcwd()
            
            if not await self._is_xkit_directory(project_path):
                self.display.info("ℹ️  Este não é um diretório .xkit válido")
                return
            
            result = await self.analyze_project(project_path)
            
            # Exibe apenas o score
            score_color = "success" if result.score >= 7.0 else "warning" if result.score >= 4.0 else "error"
            self.display.print_colored(
                f"📊 Pontuação do Projeto: {result.score:.1f}/10", 
                score_color
            )
            
        except Exception as e:
            self.display.error(f"❌ Erro no cálculo da pontuação: {str(e)}")
    
    async def analyze_project(self, project_path: str) -> ProjectAnalysisResult:
        """Analisa um projeto e retorna o resultado completo"""
        project_path = Path(project_path).resolve()
        
        # Coleta informações básicas
        files = await self._scan_project_files(project_path)
        project_type = self._detect_project_type(files)
        metrics = self._calculate_metrics(files, project_path)
        
        # Identifica problemas e sugestões
        issues = self._identify_issues(metrics, files)
        suggestions = self._generate_suggestions(issues, project_type, metrics)
        
        # Calcula pontuação
        score = self._calculate_score(metrics, len(issues))
        
        # Análise com IA (opcional)
        ai_insights = None
        if self.ai_service.is_available():
            try:
                ai_insights = await self._get_ai_insights(project_path, project_type, metrics, issues)
            except Exception:
                pass  # AI analysis is optional
        
        return ProjectAnalysisResult(
            project_path=str(project_path),
            project_type=project_type,
            metrics=metrics,
            score=score,
            issues=issues,
            suggestions=suggestions,
            files=files,
            ai_insights=ai_insights
        )
    
    async def _is_xkit_directory(self, path: str) -> bool:
        """Verifica se o diretório contém um marcador .xkit"""
        xkit_file = Path(path) / ".xkit"
        return xkit_file.exists() and (xkit_file.is_file() or xkit_file.is_dir())
    
    async def _find_xkit_projects(self, base_path: str) -> List[str]:
        """Encontra todos os diretórios .xkit recursivamente"""
        xkit_projects = []
        
        try:
            for root, dirs, files in os.walk(base_path):
                if ".xkit" in files or ".xkit" in dirs:
                    xkit_projects.append(root)
                    # Não procura subdiretórios de projetos .xkit
                    dirs.clear()
        except PermissionError:
            pass
        
        return xkit_projects
    
    async def _scan_project_files(self, project_path: Path) -> List[ProjectFile]:
        """Escaneia todos os arquivos do projeto"""
        files = []
        
        try:
            for item in project_path.rglob("*"):
                if item.is_file() and not self._should_ignore_file(item):
                    relative_path = item.relative_to(project_path)
                    
                    file_obj = ProjectFile(
                        name=item.name,
                        path=str(relative_path),
                        size=item.stat().st_size,
                        is_essential=self._is_essential_file(item.name),
                        category=self._categorize_file(item)
                    )
                    files.append(file_obj)
        except PermissionError:
            pass
        
        return files
    
    def _should_ignore_file(self, path: Path) -> bool:
        """Verifica se o arquivo deve ser ignorado"""
        ignore_patterns = [
            ".git/", "__pycache__/", "node_modules/", "target/",
            "build/", "dist/", ".vscode/", ".idea/",
            "*.pyc", "*.log", ".DS_Store", "Thumbs.db"
        ]
        
        path_str = str(path)
        return any(pattern in path_str for pattern in ignore_patterns)
    
    def _is_essential_file(self, filename: str) -> bool:
        """Verifica se é um arquivo essencial"""
        return any(essential in filename.upper() for essential in 
                  [f.upper() for f in self.essential_files])
    
    def _categorize_file(self, file_path: Path) -> str:
        """Categoriza o arquivo"""
        extension = file_path.suffix.lower()
        name = file_path.name.lower()
        
        if any(pattern in name for pattern in ["test", "spec"]):
            return "test"
        elif extension in [".md", ".rst", ".txt", ".adoc"]:
            return "documentation"
        elif extension in [".py", ".js", ".ts", ".rs", ".go", ".java", ".cs"]:
            return "source"
        elif extension in [".json", ".toml", ".yaml", ".yml", ".xml", ".ini"]:
            return "config"
        else:
            return "other"
    
    def _detect_project_type(self, files: List[ProjectFile]) -> ProjectType:
        """Detecta o tipo do projeto baseado nos arquivos"""
        file_names = {f.name.lower() for f in files}
        
        for project_type, patterns in self.project_patterns.items():
            if any(pattern.lower() in file_names for pattern in patterns):
                return project_type
        
        # Detecção por extensão de arquivo
        extensions = {Path(f.path).suffix.lower() for f in files if f.category == "source"}
        
        if ".py" in extensions:
            return ProjectType.PYTHON
        elif ".js" in extensions or ".jsx" in extensions:
            return ProjectType.JAVASCRIPT
        elif ".ts" in extensions or ".tsx" in extensions:
            return ProjectType.TYPESCRIPT
        elif ".rs" in extensions:
            return ProjectType.RUST
        elif ".go" in extensions:
            return ProjectType.GO
        elif ".java" in extensions:
            return ProjectType.JAVA
        elif ".cs" in extensions:
            return ProjectType.C_SHARP
        
        return ProjectType.UNKNOWN
    
    def _calculate_metrics(self, files: List[ProjectFile], project_path: Path) -> ProjectMetrics:
        """Calcula métricas do projeto"""
        return ProjectMetrics(
            total_files=len(files),
            total_size=sum(f.size for f in files),
            documentation_files=len([f for f in files if f.category == "documentation"]),
            config_files=len([f for f in files if f.category == "config"]),
            source_files=len([f for f in files if f.category == "source"]),
            test_files=len([f for f in files if f.category == "test"]),
            has_git=(project_path / ".git").exists(),
            has_readme=any(f.name.upper().startswith("README") for f in files),
            has_license=any(f.name.upper().startswith("LICENSE") for f in files),
            has_contributing=any(f.name.upper().startswith("CONTRIB") for f in files),
            has_tests=len([f for f in files if f.category == "test"]) > 0
        )
    
    def _identify_issues(self, metrics: ProjectMetrics, files: List[ProjectFile]) -> List[str]:
        """Identifica problemas no projeto"""
        issues = []
        
        if not metrics.has_git:
            issues.append("❌ Projeto não está sob controle de versão Git")
        
        if not metrics.has_readme:
            issues.append("❌ Arquivo README ausente")
        
        if not metrics.has_license:
            issues.append("⚠️  Arquivo LICENSE ausente")
        
        if not metrics.has_contributing:
            issues.append("ℹ️  Arquivo CONTRIBUTING.md ausente")
        
        if metrics.documentation_files == 0:
            issues.append("⚠️  Projeto sem documentação")
        
        if metrics.test_files == 0:
            issues.append("❌ Projeto sem testes")
        
        if metrics.source_files == 0:
            issues.append("❌ Nenhum arquivo de código fonte encontrado")
        
        # Problemas de estrutura
        if metrics.total_files < 3:
            issues.append("⚠️  Projeto com poucos arquivos")
        
        return issues
    
    def _generate_suggestions(self, issues: List[str], project_type: ProjectType, metrics: ProjectMetrics) -> List[str]:
        """Gera sugestões baseadas nos problemas encontrados"""
        suggestions = []
        
        if not metrics.has_git:
            suggestions.append("🔧 Execute: git init")
        
        if not metrics.has_readme:
            suggestions.append("📝 Crie um arquivo README.md explicando o projeto")
        
        if not metrics.has_license:
            suggestions.append("⚖️  Adicione uma licença (MIT, GPL, Apache, etc.)")
        
        if not metrics.has_contributing:
            suggestions.append("🤝 Crie um CONTRIBUTING.md com guidelines")
        
        if metrics.test_files == 0:
            if project_type == ProjectType.PYTHON:
                suggestions.append("🧪 Adicione testes com pytest ou unittest")
            elif project_type == ProjectType.NODE_JS:
                suggestions.append("🧪 Adicione testes com Jest ou Mocha")
            else:
                suggestions.append("🧪 Adicione testes unitários")
        
        if metrics.documentation_files == 0:
            suggestions.append("📚 Adicione documentação técnica")
        
        return suggestions
    
    def _calculate_score(self, metrics: ProjectMetrics, issues_count: int) -> float:
        """Calcula pontuação do projeto (0-10)"""
        score = 10.0
        
        # Penalizações
        if not metrics.has_git:
            score -= 2.0
        if not metrics.has_readme:
            score -= 1.5
        if not metrics.has_tests:
            score -= 2.0
        if not metrics.has_license:
            score -= 0.5
        if metrics.documentation_files == 0:
            score -= 1.0
        
        # Bonificações
        if metrics.has_contributing:
            score += 0.5
        if metrics.test_files > 0:
            score += 0.5
        
        return max(0.0, min(10.0, score))
    
    async def _get_ai_insights(self, project_path: Path, project_type: ProjectType, 
                             metrics: ProjectMetrics, issues: List[str]) -> str:
        """Obtém insights da IA sobre o projeto"""
        try:
            prompt = f"""
Analise este projeto de software e forneça insights em português:

Tipo: {project_type.value}
Arquivos: {metrics.total_files}
Código fonte: {metrics.source_files}
Testes: {metrics.test_files}
Documentação: {metrics.documentation_files}
Git: {'Sim' if metrics.has_git else 'Não'}
README: {'Sim' if metrics.has_readme else 'Não'}
Licença: {'Sim' if metrics.has_license else 'Não'}

Problemas identificados:
{chr(10).join(issues)}

Forneça 2-3 insights específicos sobre:
1. Qualidade geral do projeto
2. Áreas prioritárias de melhoria
3. Boas práticas recomendadas

Responda em no máximo 300 caracteres, de forma direta e prática.
"""
            
            # Mock da resposta da IA (substituir por chamada real quando integrado)
            return await self._mock_ai_response(prompt)
            
        except Exception:
            return None
    
    async def _mock_ai_response(self, prompt: str) -> str:
        """Mock temporário da resposta da IA"""
        # Simulação baseada no conteúdo do prompt
        if "Git: Não" in prompt:
            return "🤖 Prioridade: implementar controle de versão Git. Projeto parece estar em fase inicial, foque em estrutura básica e documentação."
        elif "Testes: 0" in prompt:
            return "🤖 Projeto funcional mas precisa de testes. Implemente CI/CD, melhore documentação e adicione cobertura de testes."
        else:
            return "🤖 Projeto bem estruturado! Considere automação de deploy, documentação avançada e métricas de qualidade."
    
    async def _display_analysis_result(self, result: ProjectAnalysisResult) -> None:
        """Exibe resultado completo da análise"""
        self.display.section(f"📊 Análise do Projeto: {os.path.basename(result.project_path)}")
        
        # Informações básicas
        self.display.info(f"📂 Caminho: {result.project_path}")
        self.display.info(f"🏷️  Tipo: {result.project_type.value.upper()}")
        
        # Pontuação
        score_color = "success" if result.score >= 7.0 else "warning" if result.score >= 4.0 else "error"
        self.display.print_colored(f"⭐ Pontuação: {result.score:.1f}/10", score_color)
        
        # Métricas
        metrics = result.metrics
        self.display.subsection("📈 Métricas")
        self.display.info(f"📄 Total de arquivos: {metrics.total_files}")
        self.display.info(f"💻 Arquivos de código: {metrics.source_files}")
        self.display.info(f"🧪 Arquivos de teste: {metrics.test_files}")
        self.display.info(f"📚 Documentação: {metrics.documentation_files}")
        self.display.info(f"⚙️  Configuração: {metrics.config_files}")
        
        # Status dos arquivos essenciais
        self.display.subsection("✅ Arquivos Essenciais")
        self._display_status("Git", metrics.has_git)
        self._display_status("README", metrics.has_readme)
        self._display_status("LICENSE", metrics.has_license)
        self._display_status("CONTRIBUTING", metrics.has_contributing)
        self._display_status("Testes", metrics.has_tests)
        
        # Problemas encontrados
        if result.issues:
            self.display.subsection("⚠️  Problemas Encontrados")
            for issue in result.issues:
                self.display.warning(f"  {issue}")
        
        # Sugestões
        if result.suggestions:
            self.display.subsection("💡 Sugestões de Melhoria")
            for suggestion in result.suggestions:
                self.display.info(f"  {suggestion}")
        
        # Insights da IA
        if result.ai_insights:
            self.display.subsection("🤖 Insights da IA")
            self.display.success(result.ai_insights)
    
    async def _display_summary_result(self, result: ProjectAnalysisResult) -> None:
        """Exibe resultado resumido da análise"""
        score_emoji = "🟢" if result.score >= 7.0 else "🟡" if result.score >= 4.0 else "🔴"
        project_name = os.path.basename(result.project_path)
        
        self.display.info(f"{score_emoji} {project_name}: {result.score:.1f}/10 ({result.project_type.value})")
        
        if result.issues:
            issues_count = len(result.issues)
            self.display.warning(f"   ⚠️  {issues_count} problema{'s' if issues_count > 1 else ''} encontrado{'s' if issues_count > 1 else ''}")
    
    def _display_status(self, item: str, status: bool) -> None:
        """Exibe status de um item"""
        icon = "✅" if status else "❌"
        color = "success" if status else "error"
        self.display.print_colored(f"  {icon} {item}", color)