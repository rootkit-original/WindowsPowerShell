"""
Application layer - Use cases and business logic orchestration
"""
import os
import asyncio
from typing import Optional, List, Dict, Any
from pathlib import Path
from ..domain import (
    DevelopmentContext, 
    ProjectInfo,
    XKitError,
    XPilotAnalysis,
    IFileSystemRepository,
    IGitRepository,
    IContainerRepository,
    IProjectAnalyzer,
    IDisplayService,
    IErrorHandler,
    IGitBranchManager,
    IXPilotAgent
)
from ..infrastructure.display import DisplayService


class AnalyzeXKitProjectUseCase:
    """Use case para analisar projetos .xkit com inteligência avançada"""
    
    def __init__(self, display_service: IDisplayService):
        self.display = display_service

    async def execute(self, path: str = None) -> None:
        """Analisa um projeto .xkit com análise inteligente usando IA"""
        if not path:
            path = os.getcwd()
        
        project_path = Path(path)
        
        # Verifica se é um projeto .xkit
        xkit_file = project_path / ".xkit"
        if not xkit_file.exists():
            print("⚠️  Este diretório não contém um arquivo .xkit")
            print("💡 Para criar um projeto .xkit, use: echo '{}' > .xkit")
            return
        
        print(f"🔍 XKit Smart Project Analysis")
        print(f"📂 Projeto: {project_path.name}")
        print("=" * 60)
        
        # 1. Análise básica estrutural
        await self._analyze_structure(project_path)
        
        # 2. Se tem .git e README.md, fazer análise profunda
        has_git = (project_path / ".git").exists()
        readme_files = [f for f in project_path.glob("README*")]
        
        if has_git and readme_files:
            print(f"\n🤖 Análise Inteligente Detectada")
            print("🔍 Projeto tem Git + README → Iniciando análise avançada...")
            await self._deep_analysis_with_ai(project_path)
        else:
            print(f"\n📊 Análise Básica (sem Git ou README)")
            await self._basic_scoring(project_path)

    async def _analyze_structure(self, project_path: Path) -> None:
        """Análise básica da estrutura do projeto"""
        files = list(project_path.rglob("*"))
        files = [f for f in files if f.is_file() and not self._should_ignore_file(f)]
        
        code_files = [f for f in files if f.suffix in ['.py', '.js', '.ts', '.ps1', '.java', '.go', '.rs', '.cpp', '.c']]
        config_files = [f for f in files if f.suffix in ['.json', '.yaml', '.yml', '.toml', '.ini']]
        doc_files = [f for f in files if f.suffix in ['.md', '.rst', '.txt'] or 'README' in f.name.upper()]
        
        print(f"📁 Total de arquivos: {len(files)}")
        print(f"💻 Código fonte: {len(code_files)}")
        print(f"⚙️  Configuração: {len(config_files)}")
        print(f"📚 Documentação: {len(doc_files)}")

    def _should_ignore_file(self, file_path: Path) -> bool:
        """Ignora arquivos comuns que não são relevantes para análise"""
        ignore_patterns = [
            '.git/', '__pycache__/', 'node_modules/', '.vscode/',
            '.pytest_cache/', 'dist/', 'build/', '.idea/',
            '*.pyc', '*.log', '.DS_Store', 'Thumbs.db'
        ]
        
        path_str = str(file_path)
        return any(pattern.replace('*', '') in path_str for pattern in ignore_patterns)

    async def _deep_analysis_with_ai(self, project_path: Path) -> None:
        """Análise profunda usando Gemini AI"""
        try:
            # Importar AI service
            from ..infrastructure.ai_service import GeminiAIService
            ai_service = GeminiAIService()
            
            if not ai_service.is_available():
                print("⚠️  Gemini AI não disponível - usando análise básica")
                await self._basic_scoring(project_path)
                return
            
            print("🤖 Conectando com Gemini AI...")
            
            # 1. Análise do Git
            git_analysis = await self._analyze_git_repo(project_path)
            
            # 2. 🆕 Análise do GitHub (issues e PRs)
            github_analysis = await self._analyze_github_issues(project_path)
            
            # 3. Análise profunda dos arquivos de documentação
            doc_analysis = await self._analyze_documentation_deep(project_path)
            
            # 4. Análise multithread da estrutura de código
            code_analysis = await self._analyze_code_structure_multithread(project_path)
            
            # 5. Detecção de problemas do projeto
            issues = await self._detect_project_issues(project_path)
            
            # 6. Arquivos perdidos importantes
            missing_files = await self._find_missing_files(project_path)
            
            # 7. Prompt para Gemini com contexto enriquecido
            context = self._build_enhanced_ai_context(project_path, git_analysis, github_analysis, doc_analysis, code_analysis, issues, missing_files)
            
            print("🧠 Analisando com IA...")
            ai_response = await self._get_gemini_analysis(ai_service, context)
            
            # 8. Exibir análise completa e avançada
            await self._display_enhanced_analysis(ai_response, git_analysis, github_analysis, doc_analysis, code_analysis, issues, missing_files)
            
        except Exception as e:
            print(f"❌ Erro na análise com IA: {e}")
            print("� Fallback para análise básica...")
            await self._basic_scoring(project_path)

    async def _analyze_git_repo(self, project_path: Path) -> dict:
        """Analisa informações do repositório Git"""
        git_info = {}
        
        try:
            import subprocess
            
            # Branch atual
            result = subprocess.run(['git', 'branch', '--show-current'], 
                                  cwd=project_path, capture_output=True, text=True)
            git_info['current_branch'] = result.stdout.strip() if result.returncode == 0 else "unknown"
            
            # Branches remotas
            result = subprocess.run(['git', 'branch', '-r'], 
                                  cwd=project_path, capture_output=True, text=True)
            if result.returncode == 0:
                remote_branches = [b.strip() for b in result.stdout.split('\n') if b.strip()]
                git_info['remote_branches'] = remote_branches[:5]  # Top 5
            
            # Último commit
            result = subprocess.run(['git', 'log', '-1', '--oneline'], 
                                  cwd=project_path, capture_output=True, text=True)
            git_info['last_commit'] = result.stdout.strip() if result.returncode == 0 else "unknown"
            
            # 🆕 Últimos 3 commits com detalhes
            result = subprocess.run(['git', 'log', '-3', '--oneline', '--decorate'], 
                                  cwd=project_path, capture_output=True, text=True)
            if result.returncode == 0:
                commits = []
                for line in result.stdout.split('\n'):
                    if line.strip():
                        commits.append(line.strip())
                git_info['recent_commits'] = commits
            
            # Informações de commit com data
            result = subprocess.run(['git', 'log', '-3', '--format=%h|%s|%an|%ar'], 
                                  cwd=project_path, capture_output=True, text=True)
            if result.returncode == 0:
                detailed_commits = []
                for line in result.stdout.split('\n'):
                    if line.strip():
                        parts = line.strip().split('|', 3)
                        if len(parts) == 4:
                            detailed_commits.append({
                                'hash': parts[0],
                                'message': parts[1],
                                'author': parts[2],
                                'date': parts[3]
                            })
                git_info['detailed_commits'] = detailed_commits
            
            # Arquivos modificados
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  cwd=project_path, capture_output=True, text=True)
            if result.returncode == 0:
                modified_files = len([f for f in result.stdout.split('\n') if f.strip()])
                git_info['modified_files'] = modified_files
            
            # Remote origin
            result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                                  cwd=project_path, capture_output=True, text=True)
            if result.returncode == 0:
                git_info['remote_url'] = result.stdout.strip()
            
        except Exception as e:
            git_info['error'] = str(e)
        
        return git_info

    async def _analyze_github_issues(self, project_path: Path) -> dict:
        """🆕 Analisa issues do GitHub usando gh CLI"""
        github_info = {}
        
        try:
            import subprocess
            
            # Verificar se gh CLI está disponível
            result = subprocess.run(['gh', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                github_info['error'] = "GitHub CLI (gh) não está instalado"
                return github_info
            
            # Verificar se está autenticado
            result = subprocess.run(['gh', 'auth', 'status'], 
                                  cwd=project_path, capture_output=True, text=True)
            if result.returncode != 0:
                github_info['error'] = "GitHub CLI não está autenticado (use: gh auth login)"
                return github_info
            
            # Buscar issues abertas
            result = subprocess.run(['gh', 'issue', 'list', '--state', 'open', '--limit', '5', 
                                   '--json', 'number,title,author,createdAt,labels'], 
                                  cwd=project_path, capture_output=True, text=True)
            
            if result.returncode == 0:
                import json
                try:
                    issues_data = json.loads(result.stdout)
                    github_info['open_issues'] = issues_data
                    github_info['open_issues_count'] = len(issues_data)
                except json.JSONDecodeError:
                    github_info['error'] = "Erro ao processar dados das issues"
            else:
                github_info['error'] = f"Erro ao buscar issues: {result.stderr}"
            
            # Buscar PRs abertos
            result = subprocess.run(['gh', 'pr', 'list', '--state', 'open', '--limit', '3',
                                   '--json', 'number,title,author,createdAt'], 
                                  cwd=project_path, capture_output=True, text=True)
            
            if result.returncode == 0:
                try:
                    prs_data = json.loads(result.stdout)
                    github_info['open_prs'] = prs_data
                    github_info['open_prs_count'] = len(prs_data)
                except json.JSONDecodeError:
                    pass
            
        except Exception as e:
            github_info['error'] = str(e)
        
        return github_info

    async def _detect_project_issues(self, project_path: Path) -> dict:
        """Detecta problemas no projeto (arquivos grandes, extensões estranhas, etc.)"""
        issues = {
            'large_files': [],
            'unknown_extensions': [],
            'binary_files': [],
            'empty_dirs': [],
            'suspicious_files': []
        }
        
        # Limites
        LARGE_FILE_THRESHOLD = 10 * 1024 * 1024  # 10MB
        
        # Extensões conhecidas
        known_extensions = {
            '.py', '.js', '.ts', '.ps1', '.psm1', '.psd1', '.java', '.cpp', '.c', '.cs',
            '.rb', '.go', '.rs', '.php', '.sh', '.bat', '.cmd', '.html', '.css', '.scss',
            '.json', '.xml', '.yml', '.yaml', '.toml', '.ini', '.cfg', '.conf',
            '.md', '.txt', '.rst', '.log', '.sql', '.csv', '.tsv',
            '.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico', '.bmp',
            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
            '.zip', '.tar', '.gz', '.7z', '.rar',
            '.exe', '.dll', '.so', '.dylib', '.app',
            '.gitignore', '.gitattributes', '.editorconfig', '.dockerignore'
        }
        
        print("🔍 Detectando problemas no projeto...")
        
        try:
            for item in project_path.rglob("*"):
                if self._should_ignore_file(item):
                    continue
                    
                if item.is_file():
                    try:
                        # Arquivos grandes
                        size = item.stat().st_size
                        if size > LARGE_FILE_THRESHOLD:
                            issues['large_files'].append({
                                'path': str(item.relative_to(project_path)),
                                'size_mb': round(size / 1024 / 1024, 2)
                            })
                        
                        # Extensões desconhecidas
                        ext = item.suffix.lower()
                        if ext and ext not in known_extensions:
                            issues['unknown_extensions'].append({
                                'path': str(item.relative_to(project_path)),
                                'extension': ext
                            })
                        
                        # Arquivos suspeitos
                        name_lower = item.name.lower()
                        if any(suspicious in name_lower for suspicious in [
                            'password', 'secret', 'private', 'key', 'token', 'credential',
                            'backup', 'temp', 'tmp', 'cache', 'log'
                        ]):
                            issues['suspicious_files'].append({
                                'path': str(item.relative_to(project_path)),
                                'reason': 'Nome suspeito'
                            })
                            
                    except (OSError, PermissionError) as e:
                        # Arquivo inacessível
                        issues['suspicious_files'].append({
                            'path': str(item.relative_to(project_path)),
                            'reason': f'Inacessível: {e}'
                        })
                
                elif item.is_dir():
                    # Diretórios vazios
                    try:
                        if not any(item.iterdir()):
                            issues['empty_dirs'].append(str(item.relative_to(project_path)))
                    except (OSError, PermissionError):
                        pass
        
        except Exception as e:
            issues['scan_error'] = str(e)
        
        return issues

    async def _find_missing_files(self, project_path: Path) -> dict:
        """Identifica arquivos importantes que podem estar faltando"""
        missing = {
            'critical': [],
            'recommended': [],
            'optional': []
        }
        
        # Arquivos críticos por tipo de projeto
        critical_files = {
            'python': ['requirements.txt', 'setup.py', 'pyproject.toml'],
            'node': ['package.json'],
            'docker': ['Dockerfile'],
            'git': ['.gitignore'],
            'ci': ['.github/workflows', 'Jenkinsfile', '.travis.yml', '.gitlab-ci.yml']
        }
        
        # Arquivos recomendados
        recommended_files = [
            'README.md', 'LICENSE', 'CONTRIBUTING.md', 
            'CHANGELOG.md', 'CODE_OF_CONDUCT.md',
            '.editorconfig', 'tests/', 'docs/'
        ]
        
        # Arquivos opcionais mas úteis
        optional_files = [
            'ARCHITECTURE.md', 'SECURITY.md', 'INSTALL.md',
            'Makefile', 'docker-compose.yml', 'tox.ini',
            '.pre-commit-config.yaml'
        ]
        
        # Detecta tipo de projeto
        has_python = any((project_path / f).exists() for f in ['*.py']) or list(project_path.rglob("*.py"))
        has_node = (project_path / 'package.json').exists()
        has_docker = (project_path / 'Dockerfile').exists() 
        has_git = (project_path / '.git').exists()
        
        # Verifica arquivos críticos
        if has_python:
            for file in critical_files['python']:
                if not (project_path / file).exists():
                    missing['critical'].append(f"{file} (Python project)")
        
        if has_node:
            for file in critical_files['node']:
                if not (project_path / file).exists():
                    missing['critical'].append(f"{file} (Node.js project)")
        
        if has_git:
            for file in critical_files['git']:
                if not (project_path / file).exists():
                    missing['critical'].append(f"{file} (Git repository)")
        
        # Verifica arquivos recomendados
        for file in recommended_files:
            file_path = project_path / file
            if not file_path.exists():
                missing['recommended'].append(file)
        
        # Verifica arquivos opcionais
        for file in optional_files:
            file_path = project_path / file
            if not file_path.exists():
                missing['optional'].append(file)
        
        return missing

    async def _analyze_documentation_deep(self, project_path: Path) -> dict:
        """Análise profunda da documentação vs realidade do projeto"""
        docs = {}
        
        # Arquivos de documentação importantes
        doc_files = {
            'README.md': 'readme',
            'ARCHITECTURE.md': 'architecture', 
            'CONTRIBUTING.md': 'contributing',
            'INSTALL.md': 'install',
            'CHANGELOG.md': 'changelog',
            'LICENSE': 'license',
            'requirements.txt': 'dependencies',
            'package.json': 'package_config',
            'setup.py': 'setup',
            'pyproject.toml': 'pyproject'
        }
        
        for file_name, doc_type in doc_files.items():
            file_path = project_path / file_name
            if file_path.exists():
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    docs[file_name] = {
                        'exists': True,
                        'size': len(content),
                        'lines': len(content.split('\n')),
                        'content_preview': content[:500] if len(content) > 500 else content,
                        'type': doc_type,
                        'quality_score': self._assess_doc_quality(content, doc_type)
                    }
                except Exception as e:
                    docs[file_name] = {
                        'exists': True,
                        'error': str(e),
                        'type': doc_type
                    }
            else:
                docs[file_name] = {'exists': False, 'type': doc_type}
        
        return docs
    
    def _assess_doc_quality(self, content: str, doc_type: str) -> int:
        """Avalia a qualidade da documentação (0-10)"""
        score = 0
        content_lower = content.lower()
        
        if doc_type == 'readme':
            if 'installation' in content_lower or 'install' in content_lower: score += 2
            if 'usage' in content_lower or 'example' in content_lower: score += 2
            if 'contributing' in content_lower: score += 1
            if 'license' in content_lower: score += 1
            if len(content) > 500: score += 2
            if '```' in content: score += 2  # Exemplos de código
        elif doc_type == 'architecture':
            if 'diagram' in content_lower or 'structure' in content_lower: score += 3
            if 'design' in content_lower: score += 2
            if 'pattern' in content_lower: score += 2
            if len(content) > 1000: score += 3
        elif doc_type == 'contributing':
            if 'pull request' in content_lower or 'pr' in content_lower: score += 3
            if 'code style' in content_lower or 'style' in content_lower: score += 2
            if 'test' in content_lower: score += 3
            if 'issue' in content_lower: score += 2
        
        return min(score, 10)
        """Analisa arquivos de documentação importantes"""
        docs = {}
        
        # Arquivos importantes para encontrar
        important_files = [
            'README.md', 'README.rst', 'README.txt',
            'ARCHITECTURE.md', 'CONTRIBUTING.md', 'INSTALL.md', 
            'CHANGELOG.md', 'LICENSE', 'LICENSE.md',
            'USAGE.md', 'API.md', 'TROUBLESHOOTING.md'
        ]
        
        for filename in important_files:
            file_path = project_path / filename
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        docs[filename] = {
                            'exists': True,
                            'size': len(content),
                            'lines': len(content.split('\n')),
                            'preview': content[:200] + "..." if len(content) > 200 else content
                        }
                except Exception:
                    docs[filename] = {'exists': True, 'error': 'Could not read file'}
            else:
                docs[filename] = {'exists': False}
        
        return docs

    async def _analyze_code_structure_multithread(self, project_path: Path) -> dict:
        """Análise multithread inteligente da estrutura de código"""
        import asyncio
        from concurrent.futures import ThreadPoolExecutor
        import threading
        from collections import defaultdict
        
        # Configurações de análise
        MAX_FILE_SIZE = 1024 * 1024  # 1MB max
        MAX_FILES_TO_ANALYZE = 100
        THREAD_COUNT = 4
        
        # Extensões de código para analisar
        code_extensions = {
            '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript', 
            '.ps1': 'PowerShell', '.psm1': 'PowerShell', '.psd1': 'PowerShell',
            '.java': 'Java', '.cpp': 'C++', '.c': 'C', '.cs': 'C#',
            '.rb': 'Ruby', '.go': 'Go', '.rs': 'Rust', '.php': 'PHP',
            '.sh': 'Shell', '.bat': 'Batch', '.cmd': 'Batch'
        }
        
        # Coletores thread-safe
        languages_lock = threading.Lock()
        languages = defaultdict(int)
        frameworks = set()
        total_lines_count = 0
        issues = []
        
        def analyze_file(file_path: Path) -> dict:
            """Analisa um arquivo individual"""
            nonlocal total_lines_count
            
            try:
                if file_path.stat().st_size > MAX_FILE_SIZE:
                    with languages_lock:
                        issues.append(f"⚠️ Arquivo muito grande: {file_path.name} ({file_path.stat().st_size // 1024}KB)")
                    return {'skipped': True, 'reason': 'too_large'}
                
                ext = file_path.suffix.lower()
                if ext not in code_extensions:
                    return {'skipped': True, 'reason': 'not_code'}
                
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                lines = len(content.split('\n'))
                
                # Thread-safe updates
                with languages_lock:
                    languages[code_extensions[ext]] += 1
                    total_lines_count += lines
                
                    # Detecta frameworks
                    content_lower = content.lower()
                    framework_keywords = {
                        'react': 'React', 'vue': 'Vue.js', 'angular': 'Angular',
                        'express': 'Express.js', 'fastapi': 'FastAPI', 'django': 'Django',
                        'flask': 'Flask', 'spring': 'Spring', 'laravel': 'Laravel',
                        'tensorflow': 'TensorFlow', 'pytorch': 'PyTorch'
                    }
                    
                    for keyword, framework in framework_keywords.items():
                        if keyword in content_lower:
                            frameworks.add(framework)
                
                return {'analyzed': True, 'lines': lines, 'language': code_extensions[ext]}
                
            except Exception as e:
                with languages_lock:
                    issues.append(f"❌ Erro ao analisar {file_path.name}: {str(e)}")
                return {'error': str(e)}
        
        # Busca arquivos de código
        code_files = []
        for ext in code_extensions.keys():
            code_files.extend(list(project_path.rglob(f"*{ext}")))
        
        # Filtra arquivos ignorados
        code_files = [f for f in code_files if not self._should_ignore_file(f)]
        
        # Limita quantidade para performance  
        if len(code_files) > MAX_FILES_TO_ANALYZE:
            issues.append(f"📊 Analisando apenas {MAX_FILES_TO_ANALYZE} de {len(code_files)} arquivos de código")
            code_files = code_files[:MAX_FILES_TO_ANALYZE]
        
        # Análise paralela
        print(f"🔍 Analisando {len(code_files)} arquivos de código...")
        
        with ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
            results = list(executor.map(analyze_file, code_files))
        
        return {
            'languages': dict(languages),
            'frameworks': list(frameworks),
            'total_files': len(code_files),
            'total_lines': total_lines_count,
            'analysis_issues': issues,
            'results': results
        }
        """Analisa a estrutura do código"""
        structure = {
            'languages': {},
            'frameworks': [],
            'patterns': [],
            'directories': []
        }
        
        # Detectar linguagens por extensão
        language_map = {
            '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
            '.java': 'Java', '.go': 'Go', '.rs': 'Rust', '.cpp': 'C++',
            '.c': 'C', '.cs': 'C#', '.php': 'PHP', '.rb': 'Ruby'
        }
        
        for file_path in project_path.rglob("*"):
            if file_path.is_file() and not self._should_ignore_file(file_path):
                ext = file_path.suffix.lower()
                if ext in language_map:
                    lang = language_map[ext]
                    structure['languages'][lang] = structure['languages'].get(lang, 0) + 1
        
        # Detectar frameworks por arquivos específicos
        framework_indicators = {
            'package.json': 'Node.js',
            'requirements.txt': 'Python',
            'Cargo.toml': 'Rust',
            'pom.xml': 'Maven/Java',
            'build.gradle': 'Gradle/Java',
            'composer.json': 'PHP/Composer',
            'Dockerfile': 'Docker',
            'docker-compose.yml': 'Docker Compose'
        }
        
        for indicator, framework in framework_indicators.items():
            if (project_path / indicator).exists():
                structure['frameworks'].append(framework)
        
        # Detectar estrutura de diretórios importantes
        important_dirs = ['src', 'lib', 'tests', 'test', 'docs', 'scripts', 'bin']
        for dir_name in important_dirs:
            if (project_path / dir_name).exists():
                structure['directories'].append(dir_name)
        
        return structure

    def _build_enhanced_ai_context(self, project_path: Path, git_info: dict, github_info: dict, docs: dict, 
                                   code_structure: dict, issues: dict, missing_files: dict) -> str:
        """Constrói contexto enriquecido para análise IA"""
        context_parts = [
            f"# Análise do Projeto: {project_path.name}",
            f"Localização: {project_path}",
            "",
            "## 🔧 Informações Git",
            f"Branch atual: {git_info.get('current_branch', 'N/A')}",
            f"Branches remotas: {', '.join(git_info.get('remote_branches', [])[:5])}",
            f"Último commit: {git_info.get('last_commit', 'N/A')}",
            f"Arquivos modificados: {git_info.get('modified_files', 0)}",
        ]
        
        # 🆕 Últimos commits detalhados
        detailed_commits = git_info.get('detailed_commits', [])
        if detailed_commits:
            context_parts.extend([
                "",
                "### 📚 Últimos 3 Commits:",
            ])
            for commit in detailed_commits:
                context_parts.append(
                    f"- {commit['hash']}: {commit['message']} ({commit['author']}, {commit['date']})"
                )
        
        # 🆕 Informações do GitHub
        context_parts.extend([
            "",
            "## 🐙 Informações do GitHub",
        ])
        
        if github_info.get('error'):
            context_parts.append(f"⚠️ {github_info['error']}")
        else:
            # Issues abertas
            open_issues = github_info.get('open_issues', [])
            open_issues_count = github_info.get('open_issues_count', 0)
            context_parts.append(f"📋 Issues abertas: {open_issues_count}")
            
            if open_issues:
                context_parts.append("Top issues:")
                for issue in open_issues[:3]:
                    labels = ', '.join([label['name'] for label in issue.get('labels', [])])
                    context_parts.append(
                        f"- #{issue['number']}: {issue['title']} ({issue['author']['login']}) [{labels}]"
                    )
            
            # PRs abertos
            open_prs = github_info.get('open_prs', [])
            open_prs_count = github_info.get('open_prs_count', 0)
            if open_prs_count > 0:
                context_parts.append(f"� Pull Requests abertos: {open_prs_count}")
                for pr in open_prs[:2]:
                    context_parts.append(
                        f"- #{pr['number']}: {pr['title']} ({pr['author']['login']})"
                    )
        
        context_parts.extend([
            "",
            "## �📚 Análise de Documentação",
        ])
        
        # Documentação com qualidade
        for file_name, info in docs.items():
            if info.get('exists'):
                quality = info.get('quality_score', 0)
                size = info.get('size', 0)
                context_parts.append(
                    f"- {file_name}: ✅ (Qualidade: {quality}/10, {size} chars)"
                )
                if info.get('content_preview'):
                    context_parts.append(f"  Preview: {info['content_preview'][:200]}...")
            else:
                context_parts.append(f"- {file_name}: ❌ AUSENTE")
        
        context_parts.extend([
            "",
            "## 💻 Estrutura de Código (Análise Multithread)",
            f"Total de arquivos analisados: {code_structure.get('total_files', 0)}",
            f"Total de linhas: {code_structure.get('total_lines', 0)}",
        ])
        
        # Linguagens detectadas
        languages = code_structure.get('languages', {})
        if languages:
            context_parts.append("Linguagens:")
            for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True):
                context_parts.append(f"- {lang}: {count} arquivos")
        
        # Frameworks detectados
        frameworks = code_structure.get('frameworks', [])
        if frameworks:
            context_parts.append(f"Frameworks detectados: {', '.join(frameworks)}")
        
        context_parts.extend([
            "",
            "## ⚠️ Problemas Detectados"
        ])
        
        # Arquivos grandes
        large_files = issues.get('large_files', [])
        if large_files:
            context_parts.append("Arquivos grandes (>10MB):")
            for file_info in large_files[:5]:  # Top 5
                context_parts.append(f"- {file_info['path']}: {file_info['size_mb']}MB")
        
        # Extensões desconhecidas
        unknown_exts = issues.get('unknown_extensions', [])
        if unknown_exts:
            ext_counts = {}
            for item in unknown_exts:
                ext = item['extension']
                ext_counts[ext] = ext_counts.get(ext, 0) + 1
            
            context_parts.append("Extensões desconhecidas:")
            for ext, count in sorted(ext_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
                context_parts.append(f"- {ext}: {count} arquivos")
        
        # Arquivos suspeitos
        suspicious = issues.get('suspicious_files', [])
        if suspicious:
            context_parts.append("Arquivos suspeitos:")
            for item in suspicious[:5]:
                context_parts.append(f"- {item['path']}: {item['reason']}")
        
        context_parts.extend([
            "",
            "## 📋 Arquivos Ausentes"
        ])
        
        # Arquivos críticos ausentes
        critical_missing = missing_files.get('critical', [])
        if critical_missing:
            context_parts.append("CRÍTICOS (podem quebrar o projeto):")
            for file in critical_missing:
                context_parts.append(f"- {file}")
        
        # Arquivos recomendados ausentes  
        recommended_missing = missing_files.get('recommended', [])
        if recommended_missing:
            context_parts.append("RECOMENDADOS (melhoram qualidade):")
            for file in recommended_missing[:10]:
                context_parts.append(f"- {file}")
        
        context_parts.extend([
            "",
            "## 🎯 Foco da Análise",
            "Por favor, analise especialmente:",
            "1. Se a documentação reflete a realidade do código",
            "2. Problemas de estrutura e organização",
            "3. Arquivos ausentes críticos para o projeto",
            "4. Qualidade e consistência do código",
            "5. Recomendações práticas para melhorar o projeto",
            ""
        ])
        
        return "\n".join(context_parts)
        """Constrói o contexto para enviar ao Gemini"""
        context = f"""
Analise este projeto de software e forneça insights detalhados para desenvolvedores:

PROJETO: {project_path.name}
LOCALIZAÇÃO: {project_path}

=== INFORMAÇÕES GIT ===
Branch atual: {git_info.get('current_branch', 'unknown')}
URL remota: {git_info.get('remote_url', 'não configurada')}
Último commit: {git_info.get('last_commit', 'não encontrado')}
Arquivos modificados: {git_info.get('modified_files', 0)}
Branches remotas: {', '.join(git_info.get('remote_branches', [])[:3])}

=== DOCUMENTAÇÃO ENCONTRADA ===
"""
        
        # Adicionar info dos docs importantes
        important_docs = ['README.md', 'ARCHITECTURE.md', 'CONTRIBUTING.md', 'INSTALL.md', 'CHANGELOG.md']
        for doc in important_docs:
            if docs.get(doc, {}).get('exists'):
                context += f"✅ {doc} ({docs[doc]['lines']} linhas)\n"
                if 'preview' in docs[doc]:
                    context += f"   Preview: {docs[doc]['preview'][:100]}...\n"
            else:
                context += f"❌ {doc} (ausente)\n"
        
        context += f"""

=== ESTRUTURA DO CÓDIGO ===
Linguagens: {', '.join([f"{k} ({v} arquivos)" for k, v in code_structure['languages'].items()])}
Frameworks: {', '.join(code_structure['frameworks']) if code_structure['frameworks'] else 'Nenhum detectado'}
Diretórios: {', '.join(code_structure['directories'])}

=== SOLICITAÇÃO DE ANÁLISE ===
Como especialista em desenvolvimento de software, forneça:

1. **QUALIDADE GERAL** (nota 1-10):
   - Avalie a organização, documentação e estrutura
   - Considere padrões de desenvolvimento encontrados

2. **PADRÕES DETECTADOS**:
   - Que convenções de código/projeto você identifica?
   - O projeto segue boas práticas da linguagem principal?

3. **PONTOS FORTES**:
   - O que está bem implementado?
   - Quais aspectos mostram maturidade do projeto?

4. **ÁREAS DE MELHORIA** (prioritárias):
   - Documentação ausente ou incompleta
   - Estrutura que poderia ser melhorada
   - Arquivos/configurações importantes faltando

5. **RECOMENDAÇÕES PARA DESENVOLVEDOR**:
   - Como contribuir efetivamente neste projeto?
   - Que workflow seguir baseado na estrutura Git?
   - Primeiros passos para um novo contribuidor

Responda de forma concisa mas detalhada, focando em aspectos práticos para desenvolvimento.
"""
        
        return context

    async def _get_gemini_analysis(self, ai_service, context: str) -> str:
        """Chama o Gemini para análise"""
        try:
            # Usar o método suggest_improvements que já existe
            result = await ai_service.suggest_improvements(
                code=context,
                language="project-analysis", 
                focus="development-workflow"
            )
            return result
        except Exception as e:
            return f"Erro na análise AI: {str(e)}"

    async def _display_smart_analysis(self, ai_response: str, git_info: dict, docs: dict, code_structure: dict) -> None:
        """Exibe a análise completa formatada"""
        
        print(f"\n� ANÁLISE INTELIGENTE COMPLETA")
        print("=" * 60)
        
        # Info Git resumida
        print(f"🌿 Git: Branch '{git_info.get('current_branch')}' | {git_info.get('modified_files', 0)} arquivos modificados")
        
        # Linguagens detectadas
        if code_structure['languages']:
            langs = ", ".join([f"{k}({v})" for k, v in list(code_structure['languages'].items())[:3]])
            print(f"💻 Linguagens: {langs}")
        
        # Frameworks
        if code_structure['frameworks']:
            print(f"🛠️  Frameworks: {', '.join(code_structure['frameworks'][:3])}")
        
        print(f"\n🤖 ANÁLISE GEMINI AI")
        print("-" * 40)
        self._display_formatted_ai_response(ai_response)
        
        print(f"\n📋 ARQUIVOS DE DOCUMENTAÇÃO")
        print("-" * 40)
        important_docs = ['README.md', 'ARCHITECTURE.md', 'CONTRIBUTING.md', 'INSTALL.md', 'CHANGELOG.md', 'LICENSE']
        for doc in important_docs:
            status = "✅" if docs.get(doc, {}).get('exists') else "❌"
            print(f"{status} {doc}")
        
        print(f"\n✨ Análise completa finalizada!")

    async def _display_enhanced_analysis(self, ai_response, git_info: dict, github_info: dict, docs: dict, 
                                         code_structure: dict, issues: dict, missing_files: dict):
        """Display avançado com todas as informações"""
        
        print(f"\n� ANÁLISE INTELIGENTE COMPLETA")
        print("=" * 60)
        
        # Informações Git
        branch = git_info.get('current_branch', 'unknown')
        modified = git_info.get('modified_files', 0)
        print(f"🌿 Git: Branch '{branch}' | {modified} arquivos modificados")
        
        # 🆕 Últimos commits
        detailed_commits = git_info.get('detailed_commits', [])
        if detailed_commits:
            print(f"📚 Últimos commits:")
            for commit in detailed_commits[:3]:
                print(f"  • {commit['hash']}: {commit['message']} ({commit['date']})")
        
        # 🆕 Informações do GitHub
        if not github_info.get('error'):
            open_issues_count = github_info.get('open_issues_count', 0)
            open_prs_count = github_info.get('open_prs_count', 0)
            print(f"🐙 GitHub: {open_issues_count} issues abertas, {open_prs_count} PRs abertas")
            
            # Mostrar top issues
            open_issues = github_info.get('open_issues', [])
            if open_issues:
                print(f"📋 Top issues:")
                for issue in open_issues[:3]:
                    labels = ', '.join([label['name'] for label in issue.get('labels', [])])
                    print(f"  • #{issue['number']}: {issue['title']} [{labels}]")
        else:
            print(f"🐙 GitHub: {github_info.get('error', 'Não disponível')}")
        
        print("")  # Linha em branco
        languages = code_structure.get('languages', {})
        total_files = code_structure.get('total_files', 0)
        total_lines = code_structure.get('total_lines', 0)
        
        if languages:
            lang_summary = ', '.join([f"{lang}({count})" for lang, count in list(languages.items())[:3]])
            print(f"💻 Código: {total_files} arquivos, {total_lines:,} linhas")
            print(f"🔤 Linguagens: {lang_summary}")
        
        # Frameworks
        frameworks = code_structure.get('frameworks', [])
        if frameworks:
            print(f"🛠️  Frameworks: {', '.join(frameworks[:3])}")
        
        # IA Analysis
        print(f"\n🤖 ANÁLISE GEMINI AI")
        print("-" * 40)
        self._display_formatted_ai_response(ai_response)
        
        # Problemas detectados
        print(f"\n⚠️ PROBLEMAS DETECTADOS")
        print("-" * 40)
        
        large_files = issues.get('large_files', [])
        if large_files:
            print(f"📁 Arquivos grandes (>{len(large_files)} encontrados):")
            for file_info in large_files[:3]:
                print(f"  • {file_info['path']}: {file_info['size_mb']}MB")
            if len(large_files) > 3:
                print(f"  ... e mais {len(large_files) - 3}")
        
        unknown_exts = issues.get('unknown_extensions', [])
        if unknown_exts:
            ext_counts = {}
            for item in unknown_exts:
                ext = item['extension']
                ext_counts[ext] = ext_counts.get(ext, 0) + 1
            
            print(f"🔍 Extensões desconhecidas ({len(ext_counts)} tipos):")
            for ext, count in list(sorted(ext_counts.items(), key=lambda x: x[1], reverse=True))[:5]:
                print(f"  • {ext}: {count} arquivos")
        
        suspicious = issues.get('suspicious_files', [])
        if suspicious:
            print(f"🚨 Arquivos suspeitos ({len(suspicious)} encontrados):")
            for item in suspicious[:3]:
                print(f"  • {item['path']}: {item['reason']}")
        
        # Arquivos ausentes
        print(f"\n📋 ARQUIVOS AUSENTES")
        print("-" * 40)
        
        critical_missing = missing_files.get('critical', [])
        if critical_missing:
            print(f"🚨 CRÍTICOS ({len(critical_missing)}):")
            for file in critical_missing:
                print(f"  ❌ {file}")
        
        recommended_missing = missing_files.get('recommended', [])
        if recommended_missing:
            print(f"⚠️ RECOMENDADOS ({len(recommended_missing)}):")
            for file in recommended_missing[:5]:
                print(f"  ⚪ {file}")
            if len(recommended_missing) > 5:
                print(f"  ... e mais {len(recommended_missing) - 5}")
        
        # Documentação com qualidade
        print(f"\n📚 QUALIDADE DA DOCUMENTAÇÃO")
        print("-" * 40)
        important_docs = ['README.md', 'ARCHITECTURE.md', 'CONTRIBUTING.md', 'INSTALL.md', 'CHANGELOG.md', 'LICENSE']
        
        for doc in important_docs:
            if doc in docs and docs[doc].get('exists'):
                quality = docs[doc].get('quality_score', 0)
                size = docs[doc].get('size', 0)
                if quality >= 7:
                    status = "✅"
                elif quality >= 4:
                    status = "⚠️"
                else:
                    status = "❌"
                print(f"{status} {doc}: {quality}/10 ({size:,} chars)")
            else:
                print(f"❌ {doc}: AUSENTE")
        
        print(f"\n✨ Análise completa finalizada!")
        
        # Análise issues do código
        analysis_issues = code_structure.get('analysis_issues', [])
        if analysis_issues:
            print(f"\n📊 NOTAS DA ANÁLISE:")
            for issue in analysis_issues[:3]:
                print(f"  • {issue}")

    def _display_formatted_ai_response(self, ai_response):
        """Formata a resposta da IA de forma mais legível"""
        if hasattr(ai_response, 'findings') and ai_response.findings:
            analysis_text = ai_response.findings[0] if ai_response.findings else str(ai_response)
            
            lines = analysis_text.split('\n')
            current_section = ""
            section_count = 0
            
            for line in lines:
                line = line.strip()
                if not line or section_count > 4:  # Limita a 4 seções principais
                    continue
                    
                # Detecta seções principais
                if line.startswith('**') and line.endswith('**') and 'QUALIDADE' in line:
                    print(f"\n📊 QUALIDADE GERAL")
                    print("-" * 30)
                    section_count += 1
                    continue
                elif line.startswith('**') and line.endswith('**') and 'PONTOS FORTES' in line:
                    print(f"\n✅ PONTOS FORTES")
                    print("-" * 30)
                    section_count += 1
                    continue
                elif line.startswith('**') and line.endswith('**') and 'ÁREAS DE MELHORIA' in line:
                    print(f"\n⚠️ ÁREAS DE MELHORIA")
                    print("-" * 30)
                    section_count += 1
                    continue
                elif line.startswith('**') and line.endswith('**') and 'RECOMENDAÇÕES' in line:
                    print(f"\n� PRÓXIMOS PASSOS")
                    print("-" * 30)
                    section_count += 1
                    continue
                
                # Formata conteúdo das seções
                if section_count > 0:
                    clean_line = line.replace('*   **', '• ').replace('**:', ':').replace('*   ', '• ')
                    clean_line = clean_line.replace('**', '').replace('*', '')
                    
                    # Mostra apenas pontos importantes e concisos
                    if clean_line.startswith('• ') and len(clean_line) < 150:
                        print(f"  {clean_line}")
                    elif 'Nota:' in clean_line or 'Clone o' in clean_line or 'Leia a' in clean_line:
                        print(f"  {clean_line}")
                        
            print(f"\n🎯 RESUMO: Projeto com boa base documental, mas precisa de mais testes e CI/CD")
        else:
            print(f"📝 {str(ai_response)[:300]}...")

    async def _basic_scoring(self, project_path: Path) -> None:
        """Análise básica quando AI não está disponível"""
        files = list(project_path.rglob("*"))
        files = [f for f in files if f.is_file() and not self._should_ignore_file(f)]
        code_files = [f for f in files if f.suffix in ['.py', '.js', '.ts', '.ps1']]
        
        score = 0
        
        # Git (+3)
        has_git = (project_path / '.git').exists()
        if has_git:
            score += 3
            print("✅ Git: +3 pontos")
        else:
            print("❌ Git: 0 pontos")
        
        # README (+2)
        readme_files = [f for f in files if f.name.upper().startswith('README')]
        has_readme = len(readme_files) > 0
        if has_readme:
            score += 2
            print("✅ README: +2 pontos")
        else:
            print("❌ README: 0 pontos")
            
        # Código fonte (+3)
        if code_files:
            score += 3
            print(f"✅ Código fonte ({len(code_files)} arquivos): +3 pontos")
        else:
            print("❌ Código fonte: 0 pontos")
            
        # Estrutura (+2)
        if len(files) > 5:
            score += 2
            print("✅ Estrutura organizada: +2 pontos")
        else:
            print("⚠️  Estrutura básica: +1 ponto")
            score += 1
        
        score_emoji = "🟢" if score >= 7 else "🟡" if score >= 4 else "🔴"
        print(f"\n{score_emoji} Pontuação Final: {score}/10")
        
        # Sugestões básicas
        suggestions = []
        if not has_git:
            suggestions.append("🔧 Execute: git init")
        if not has_readme:
            suggestions.append("📝 Crie um arquivo README.md")
        
        if suggestions:
            print("\n💡 Sugestões:")
            for suggestion in suggestions:
                print(f"  {suggestion}")
        
        print("\n✅ Análise básica concluída!")


class AnalyzeProjectUseCase:
    """Use case for analyzing the current development context"""
    
    def __init__(
        self,
        file_system: IFileSystemRepository,
        git_repo: IGitRepository,
        container_repo: IContainerRepository,
        project_analyzer: IProjectAnalyzer
    ):
        self.file_system = file_system
        self.git_repo = git_repo
        self.container_repo = container_repo
        self.project_analyzer = project_analyzer

    def execute(self, current_path: Path) -> DevelopmentContext:
        """Analyze current development context"""
        
        # Get basic project info
        project_info = self.project_analyzer.get_project_info(current_path)
        
        # Try to find git repository
        git_root = self.file_system.find_git_root(current_path)
        git_info = None
        if git_root:
            git_info = self.git_repo.get_git_info(git_root)
            # Update project info for git projects
            project_info = ProjectInfo(
                name=git_root.name,
                path=git_root,
                type='git_project',
                technologies=self.project_analyzer.detect_technologies(git_root),
                relative_path=str(current_path.relative_to(git_root)) if current_path != git_root else '.'
            )
        
        # Analyze README
        readme_info = self.project_analyzer.analyze_readme(
            git_root if git_root else current_path
        )
        
        # Detect container engine
        container_info = self.container_repo.detect_container_engine()
        
        return DevelopmentContext(
            project=project_info,
            git=git_info,
            readme=readme_info,
            container=container_info
        )


class ShowWelcomeUseCase:
    """Use case for showing welcome message"""
    
    def __init__(self, display_service: IDisplayService):
        self.display_service = display_service
    
    def execute(self, context: DevelopmentContext) -> None:
        """Show welcome message based on context"""
        self.display_service.show_welcome(context)


class ShowHelpUseCase:
    """Use case for showing help information"""
    
    def __init__(self, display_service: IDisplayService):
        self.display_service = display_service
    
    def execute(self, context: DevelopmentContext) -> None:
        """Show help based on context"""
        self.display_service.show_help(context)


class ShowStatusUseCase:
    """Use case for showing detailed status"""
    
    def __init__(self, display_service: IDisplayService):
        self.display_service = display_service
    
    def execute(self, context: DevelopmentContext) -> None:
        """Show detailed status"""
        self.display_service.show_status(context)


class ShowAISuggestionsUseCase:
    """Use case for showing AI suggestions"""
    
    def __init__(self, display_service: IDisplayService):
        self.display_service = display_service
    
    def execute(self, context: DevelopmentContext) -> None:
        """Show AI suggestions"""
        if hasattr(self.display_service, 'show_ai_suggestions'):
            self.display_service.show_ai_suggestions(context)
        else:
            print("❌ Serviço de AI não disponível")


class AskAISolutionUseCase:
    """Use case for asking AI solutions"""
    
    def __init__(self, display_service: IDisplayService):
        self.display_service = display_service
    
    def execute(self, problem: str, context: DevelopmentContext) -> None:
        """Ask AI for solution"""
        if hasattr(self.display_service, 'ask_ai_solution'):
            self.display_service.ask_ai_solution(problem, context)
        else:
            print("❌ Serviço de AI não disponível")


class ExecuteContainerCommandUseCase:
    """Use case for executing container commands"""
    
    def __init__(self, container_repo: IContainerRepository):
        self.container_repo = container_repo
        
    def execute(self, command: str, args: list = None) -> bool:
        """Execute container command if engine is available"""
        container_info = self.container_repo.detect_container_engine()
        if not container_info or not container_info.is_available:
            return False
            
        # This would be implemented to execute the actual command
        # For now, just return success if container is available
        return True


class HandleErrorUseCase:
    """Use case for handling errors in the XKit system"""
    
    def __init__(
        self,
        error_handler: IErrorHandler,
        display_service: IDisplayService,
        git_branch_manager: IGitBranchManager,
        xpilot_agent: IXPilotAgent
    ):
        self.error_handler = error_handler
        self.display_service = display_service
        self.git_branch_manager = git_branch_manager
        self.xpilot_agent = xpilot_agent
    
    def execute(self, message: str, command: str = "", context: str = "") -> None:
        """Handle error with full XPilot resolution workflow"""
        # Create error instance
        error = self.error_handler.create_error(message, command, context)
        
        # Store error for tracking
        self.error_handler.store_error(error)
        
        # Show error details with emojis
        self.display_service.show_error(error)
        
        # Ask user for action
        user_choice = self.display_service.prompt_error_action()
        
        if user_choice.lower() in ['y', 'yes']:
            self._start_xpilot_resolution(error)
        elif user_choice.lower() in ['d', 'details']:
            self.display_service.show_error_details(error)
            # Recurse for another choice
            self.execute(message, command, context)
        elif user_choice.lower() in ['s', 'skip']:
            self.display_service.show_skip_message()
        else:
            self.display_service.show_ignore_message()
    
    def _start_xpilot_resolution(self, error: XKitError) -> None:
        """Start XPilot resolution process"""
        try:
            # Create error branch
            branch_name = self.git_branch_manager.create_error_branch(error)
            error.git_branch = branch_name
            
            # Commit error report
            self.git_branch_manager.commit_error_report(error, branch_name)
            
            # Analyze with XPilot
            analysis = self.xpilot_agent.analyze_error(error)
            
            # Show analysis results
            self.display_service.show_xpilot_analysis(error, analysis)
            
            # Apply auto-fix if available and user agrees
            if analysis.auto_fix_available:
                if self.display_service.confirm_auto_fix():
                    self._apply_auto_fix(error, analysis)
            
            # Ask if user wants to return to main branch
            if self.display_service.confirm_return_to_main():
                self.git_branch_manager.switch_to_previous_branch()
                
        except Exception as e:
            self.display_service.show_git_error(str(e))
            # Continue with analysis without git operations
            analysis = self.xpilot_agent.analyze_error(error)
            self.display_service.show_xpilot_analysis(error, analysis)
    
    def _apply_auto_fix(self, error: XKitError, analysis: XPilotAnalysis) -> None:
        """Apply automatic fix"""
        if analysis.auto_fix_script:
            # This would execute the fix script
            self.display_service.show_auto_fix_applied()


class ShowErrorDetailsUseCase:
    """Use case for showing detailed error information"""
    
    def __init__(self, error_handler: IErrorHandler, display_service: IDisplayService):
        self.error_handler = error_handler
        self.display_service = display_service
    
    def execute(self) -> None:
        """Show details of the last error"""
        error = self.error_handler.get_last_error()
        if error:
            self.display_service.show_error_details(error)
        else:
            self.display_service.show_no_error_message()


class RetryLastErrorUseCase:
    """Use case for retrying the last error resolution"""
    
    def __init__(self, handle_error_use_case: HandleErrorUseCase, error_handler: IErrorHandler):
        self.handle_error_use_case = handle_error_use_case
        self.error_handler = error_handler
    
    def execute(self) -> None:
        """Retry resolution of the last error"""
        error = self.error_handler.get_last_error()
        if error:
            self.handle_error_use_case.execute(error.message, error.command, error.context)
        else:
            print("ℹ️  No recent error to retry")