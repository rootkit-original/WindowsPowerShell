"""
Project Analyzer MCP Server
Provides project analysis functionality through MCP protocol
"""
import asyncio
import os
import json
from typing import Dict, Any, List, Optional
from pathlib import Path
import sys

from ..protocol import MCPServer, Tool


class XKitProjectAnalyzerServer(MCPServer):
    """Project analysis functionality MCP server"""
    
    def __init__(self):
        super().__init__("xkit-project-analyzer", "1.0.0")
        self.xkit_root = Path(__file__).parent.parent.parent.parent
    
    async def list_tools(self) -> List[Tool]:
        """List available project analysis tools"""
        return [
            Tool(
                name="analyze-project",
                description="Perform comprehensive project analysis with Git and GitHub integration",
                input_schema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Path to analyze (default: current directory)"
                        },
                        "include_git": {
                            "type": "boolean",
                            "description": "Include Git information in analysis",
                            "default": True
                        },
                        "include_github": {
                            "type": "boolean", 
                            "description": "Include GitHub issues and PRs",
                            "default": True
                        },
                        "detailed": {
                            "type": "boolean",
                            "description": "Include detailed analysis",
                            "default": False
                        }
                    },
                    "required": []
                }
            ),
            Tool(
                name="quick-analyze",
                description="Quick project analysis without AI",
                input_schema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Path to analyze (default: current directory)"
                        }
                    },
                    "required": []
                }
            ),
            Tool(
                name="analyze-git-status",
                description="Analyze Git repository status and recent commits",
                input_schema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Repository path (default: current directory)"
                        },
                        "commit_count": {
                            "type": "integer",
                            "description": "Number of recent commits to include",
                            "default": 3
                        }
                    },
                    "required": []
                }
            ),
            Tool(
                name="analyze-github-issues",
                description="Analyze GitHub issues and pull requests",
                input_schema={
                    "type": "object", 
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Repository path (default: current directory)"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of issues to fetch",
                            "default": 5
                        }
                    },
                    "required": []
                }
            )
        ]
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute project analysis tool"""
        try:
            if name == "analyze-project":
                return await self._analyze_project_full(arguments)
            elif name == "quick-analyze":
                return await self._quick_analyze(arguments)
            elif name == "analyze-git-status":
                return await self._analyze_git_status(arguments)
            elif name == "analyze-github-issues":
                return await self._analyze_github_issues(arguments)
            else:
                return {
                    "success": False,
                    "error": f"Unknown tool: {name}",
                    "available_tools": [tool.name for tool in await self.list_tools()]
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Tool execution failed: {str(e)}",
                "tool": name,
                "arguments": arguments
            }
    
    async def _analyze_project_full(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Full project analysis with all features"""
        try:
            from xkit.application.use_cases import AnalyzeXKitProjectUseCase
            from xkit.infrastructure.display import DisplayService
            
            path = args.get("path", os.getcwd())
            include_git = args.get("include_git", True)
            include_github = args.get("include_github", True)
            detailed = args.get("detailed", False)
            
            # Create a display service that captures output
            class CaptureDisplayService:
                def __init__(self):
                    self.output = []
                
                def info(self, message):
                    self.output.append(f"ℹ️ {message}")
                
                def success(self, message):
                    self.output.append(f"✅ {message}")
                
                def error(self, message):
                    self.output.append(f"❌ {message}")
                
                def warning(self, message):
                    self.output.append(f"⚠️ {message}")
            
            display_service = CaptureDisplayService()
            use_case = AnalyzeXKitProjectUseCase(display_service)
            
            # Execute analysis
            await use_case.execute(path)
            
            # Get basic project metrics
            project_path = Path(path)
            files = list(project_path.rglob("*"))
            files = [f for f in files if f.is_file() and not use_case._should_ignore_file(f)]
            
            code_files = [f for f in files if f.suffix in ['.py', '.js', '.ts', '.ps1', '.java', '.go', '.rs', '.cpp', '.c']]
            config_files = [f for f in files if f.suffix in ['.json', '.yaml', '.yml', '.toml', '.ini']]
            doc_files = [f for f in files if f.suffix in ['.md', '.rst', '.txt'] or 'README' in f.name.upper()]
            
            # Technologies
            technologies = []
            if any(f.suffix == '.py' for f in code_files):
                technologies.append('Python')
            if any(f.suffix in ['.js', '.jsx'] for f in code_files):
                technologies.append('JavaScript')
            if any(f.suffix in ['.ts', '.tsx'] for f in code_files):
                technologies.append('TypeScript')
            if any(f.suffix == '.ps1' for f in code_files):
                technologies.append('PowerShell')
            
            # Git info if requested
            git_info = {}
            if include_git and (project_path / ".git").exists():
                git_info = await self._get_git_info(project_path)
            
            # GitHub info if requested
            github_info = {}
            if include_github:
                github_info = await self._get_github_info(project_path)
            
            # Calculate score
            score = self._calculate_score(len(files), len(code_files), len(doc_files), bool(git_info))
            
            result = {
                "success": True,
                "analysis": {
                    "project_name": project_path.name,
                    "path": str(project_path),
                    "metrics": {
                        "total_files": len(files),
                        "code_files": len(code_files),
                        "config_files": len(config_files),
                        "doc_files": len(doc_files)
                    },
                    "technologies": technologies,
                    "score": score,
                    "git_info": git_info if include_git else None,
                    "github_info": github_info if include_github else None
                },
                "output": display_service.output
            }
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Analysis failed: {str(e)}"
            }
    
    async def _quick_analyze(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Quick analysis without AI or external dependencies"""
        try:
            path = args.get("path", os.getcwd())
            project_path = Path(path)
            
            if not project_path.exists():
                return {
                    "success": False,
                    "error": f"Path does not exist: {path}"
                }
            
            # Basic file counting
            files = list(project_path.rglob("*"))
            files = [f for f in files if f.is_file()]
            
            # Filter common ignore patterns
            ignore_patterns = ['.git', '__pycache__', 'node_modules', '.vscode', 'dist', 'build']
            files = [f for f in files if not any(pattern in str(f) for pattern in ignore_patterns)]
            
            code_files = [f for f in files if f.suffix in ['.py', '.js', '.ts', '.ps1', '.java', '.go', '.rs', '.cpp', '.c']]
            test_files = [f for f in files if 'test' in f.name.lower() or f.suffix == '.test']
            doc_files = [f for f in files if f.suffix in ['.md', '.rst', '.txt'] or 'README' in f.name.upper()]
            config_files = [f for f in files if f.suffix in ['.json', '.yaml', '.yml', '.toml', '.ini']]
            
            # Technology detection
            technologies = []
            if any(f.suffix == '.py' for f in code_files):
                technologies.append('Python')
            if any(f.suffix in ['.js', '.jsx'] for f in code_files):
                technologies.append('JavaScript')
            if any(f.suffix in ['.ts', '.tsx'] for f in code_files):
                technologies.append('TypeScript')
            if any(f.suffix == '.ps1' for f in code_files):
                technologies.append('PowerShell')
            
            # Git status
            git_initialized = (project_path / ".git").exists()
            
            # Simple scoring
            score = self._calculate_score(len(files), len(code_files), len(doc_files), git_initialized)
            
            # Generate suggestions
            suggestions = []
            if not git_initialized:
                suggestions.append("🌿 Inicializar Git: `git init`")
            if len(doc_files) == 0:
                suggestions.append("📚 Adicionar documentação: README.md")
            if len(test_files) == 0 and len(code_files) > 5:
                suggestions.append("🧪 Adicionar testes unitários")
            if len(config_files) == 0:
                suggestions.append("⚙️ Adicionar arquivos de configuração")
            
            return {
                "success": True,
                "project_name": project_path.name,
                "score": score,
                "metrics": {
                    "total_files": len(files),
                    "code_files": len(code_files), 
                    "test_files": len(test_files),
                    "doc_files": len(doc_files),
                    "config_files": len(config_files)
                },
                "technologies": technologies,
                "git_initialized": git_initialized,
                "suggestions": suggestions,
                "formatted_output": self._format_quick_analysis(project_path.name, score, {
                    "total": len(files),
                    "code": len(code_files),
                    "tests": len(test_files), 
                    "docs": len(doc_files),
                    "config": len(config_files)
                }, technologies, git_initialized, suggestions)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Quick analysis failed: {str(e)}"
            }
    
    async def _analyze_git_status(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze Git status and recent commits"""
        try:
            import subprocess
            
            path = args.get("path", os.getcwd())
            commit_count = args.get("commit_count", 3)
            project_path = Path(path)
            
            if not (project_path / ".git").exists():
                return {
                    "success": False,
                    "error": "Not a Git repository"
                }
            
            git_info = await self._get_git_info(project_path, commit_count)
            
            return {
                "success": True,
                "git_info": git_info
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Git analysis failed: {str(e)}"
            }
    
    async def _analyze_github_issues(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze GitHub issues and PRs"""
        try:
            import subprocess
            
            path = args.get("path", os.getcwd())
            limit = args.get("limit", 5)
            project_path = Path(path)
            
            github_info = await self._get_github_info(project_path, limit)
            
            return {
                "success": True,
                "github_info": github_info
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"GitHub analysis failed: {str(e)}"
            }
    
    async def _get_git_info(self, project_path: Path, commit_count: int = 3) -> Dict[str, Any]:
        """Get Git repository information"""
        import subprocess
        
        git_info = {}
        
        try:
            # Current branch
            result = subprocess.run(['git', 'branch', '--show-current'], 
                                  cwd=project_path, capture_output=True, text=True)
            git_info['current_branch'] = result.stdout.strip() if result.returncode == 0 else "unknown"
            
            # Recent commits
            result = subprocess.run(['git', 'log', f'-{commit_count}', '--format=%h|%s|%an|%ar'], 
                                  cwd=project_path, capture_output=True, text=True)
            if result.returncode == 0:
                commits = []
                for line in result.stdout.split('\n'):
                    if line.strip():
                        parts = line.strip().split('|', 3)
                        if len(parts) == 4:
                            commits.append({
                                'hash': parts[0],
                                'message': parts[1],
                                'author': parts[2],
                                'date': parts[3]
                            })
                git_info['recent_commits'] = commits
            
            # Modified files
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  cwd=project_path, capture_output=True, text=True)
            if result.returncode == 0:
                modified_files = len([f for f in result.stdout.split('\n') if f.strip()])
                git_info['modified_files'] = modified_files
            
        except Exception as e:
            git_info['error'] = str(e)
        
        return git_info
    
    async def _get_github_info(self, project_path: Path, limit: int = 5) -> Dict[str, Any]:
        """Get GitHub issues and PRs information"""
        import subprocess
        
        github_info = {}
        
        try:
            # Check if gh CLI is available
            result = subprocess.run(['gh', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                github_info['error'] = "GitHub CLI (gh) not installed"
                return github_info
            
            # Get open issues
            result = subprocess.run(['gh', 'issue', 'list', '--state', 'open', '--limit', str(limit),
                                   '--json', 'number,title,author,createdAt,labels'], 
                                  cwd=project_path, capture_output=True, text=True)
            
            if result.returncode == 0:
                import json
                try:
                    issues_data = json.loads(result.stdout)
                    github_info['open_issues'] = issues_data
                    github_info['open_issues_count'] = len(issues_data)
                except json.JSONDecodeError:
                    github_info['issues_error'] = "Failed to parse issues data"
            
            # Get open PRs
            result = subprocess.run(['gh', 'pr', 'list', '--state', 'open', '--limit', '3',
                                   '--json', 'number,title,author,createdAt'], 
                                  cwd=project_path, capture_output=True, text=True)
            
            if result.returncode == 0:
                try:
                    prs_data = json.loads(result.stdout)
                    github_info['open_prs'] = prs_data
                    github_info['open_prs_count'] = len(prs_data)
                except json.JSONDecodeError:
                    github_info['prs_error'] = "Failed to parse PRs data"
            
        except Exception as e:
            github_info['error'] = str(e)
        
        return github_info
    
    def _calculate_score(self, total_files: int, code_files: int, doc_files: int, has_git: bool) -> float:
        """Calculate project quality score"""
        score = 5.0  # Base score
        
        # File diversity bonus
        if code_files > 0:
            score += 2.0
        if doc_files > 0:
            score += 1.5
        
        # Git bonus
        if has_git:
            score += 1.0
        
        # Size penalty/bonus
        if total_files > 100:
            score += 0.5
        elif total_files < 5:
            score -= 1.0
        
        return min(10.0, max(0.0, score))
    
    def _format_quick_analysis(self, project_name: str, score: float, metrics: Dict, 
                             technologies: List[str], git_initialized: bool, suggestions: List[str]) -> str:
        """Format quick analysis output"""
        
        # Score color
        if score >= 7.0:
            score_emoji = "🟢"
        elif score >= 4.0:
            score_emoji = "🟡"
        else:
            score_emoji = "🔴"
        
        output = [
            "📊 RESULTADO COMPLETO:",
            "=" * 50,
            f"📊 **Análise Avançada: {project_name}**",
            f"{score_emoji} **Score: {score:.0f}/10**",
            "",
            "```",
            "📈 Métricas do Projeto:",
            f"📁 Total: {metrics['total']} arquivos",
            f"💻 Código: {metrics['code']} arquivos", 
            f"🧪 Testes: {metrics['tests']} arquivos",
            f"📚 Docs: {metrics['docs']} arquivos",
            f"⚙️ Config: {metrics['config']} arquivos",
            "```",
            "",
            f"{'✅' if git_initialized else '❌'} **Git {'inicializado' if git_initialized else 'não inicializado'}**"
        ]
        
        if not git_initialized:
            output.append("_Considere: `git init`_")
        
        output.append("")
        
        if technologies:
            output.extend([
                "🛠️ **Tecnologias:**",
                *[f"• {tech}" for tech in technologies],
                ""
            ])
        
        if suggestions:
            output.extend([
                "💡 **Sugestões:**",
                *[f"• {suggestion}" for suggestion in suggestions],
                ""
            ])
        
        # Add timestamp
        from datetime import datetime
        now = datetime.now()
        output.extend([
            f"🕒 **Analisado:** {now.strftime('%H:%M:%S')}",
            "🚀 **XKit v3.0 - Análise Avançada**"
        ])
        
        return "\n".join(output)