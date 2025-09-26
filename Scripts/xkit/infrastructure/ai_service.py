"""
AI Service - Integração com Gemini AI para decisões inteligentes
"""
import os
import json
import requests
from typing import Optional, Dict, Any
from ..domain.interfaces import IDisplayService
from ..domain.entities import DevelopmentContext


class GeminiAIService:
    """Serviço de integração com Gemini AI"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        
    def is_available(self) -> bool:
        """Verifica se o serviço está disponível"""
        return bool(self.api_key)
    
    def analyze_project_context(self, context: DevelopmentContext) -> Optional[str]:
        """Analisa o contexto do projeto e sugere ações"""
        if not self.is_available():
            return None
            
        prompt = self._build_context_prompt(context)
        return self._call_gemini(prompt)
    
    def suggest_solution(self, problem: str, context: DevelopmentContext) -> Optional[str]:
        """Sugere soluções para problemas específicos"""
        if not self.is_available():
            return None
            
        prompt = f"""
        Contexto do projeto:
        - Projeto: {context.project.name}
        - Tecnologias: {', '.join(context.project.technologies)}
        - Git: {'Sim' if context.is_git_project else 'Não'}
        - Container: {'Sim' if context.has_containers else 'Não'}
        
        Problema: {problem}
        
        Forneça uma solução concisa e prática em português:
        """
        
        return self._call_gemini(prompt)
    
    def detect_anomalies(self, context: DevelopmentContext) -> Optional[Dict[str, Any]]:
        """Detecta anomalias no projeto"""
        anomalies = {}
        
        # Verifica inconsistências básicas
        if context.is_git_project and context.git:
            if context.git.changes_count > 10:
                anomalies['many_changes'] = f"Muitas mudanças não commitadas: {context.git.changes_count}"
        
        # Verifica tecnologias sem arquivos de configuração
        tech_checks = {
            'Python': ['requirements.txt', 'pyproject.toml', 'setup.py'],
            'Node.js': ['package.json'],
            'Docker': ['Dockerfile', 'docker-compose.yml'],
        }
        
        for tech in context.project.technologies:
            if tech in tech_checks:
                has_config = any(
                    (context.project.path / config_file).exists() 
                    for config_file in tech_checks[tech]
                )
                if not has_config:
                    anomalies[f'{tech.lower()}_config'] = f"Projeto {tech} sem arquivo de configuração"
        
        return anomalies if anomalies else None
    
    def _build_context_prompt(self, context: DevelopmentContext) -> str:
        """Constrói prompt baseado no contexto"""
        prompt = f"""
        Analise este ambiente de desenvolvimento e forneça 2-3 sugestões práticas em português:
        
        Projeto: {context.project.name}
        Tipo: {context.project.type}
        Tecnologias: {', '.join(context.project.technologies)}
        """
        
        if context.is_git_project:
            prompt += f"""
        Git Branch: {context.git.current_branch}
        Mudanças pendentes: {context.git.changes_count}
        """
        
        if context.has_containers:
            prompt += f"Container Engine: {context.container.engine_type}"
        
        prompt += "\nSugestões (máximo 3 linhas cada):"
        
        return prompt
    
    def _call_gemini(self, prompt: str) -> Optional[str]:
        """Chama a API do Gemini"""
        try:
            headers = {
                'Content-Type': 'application/json',
            }
            
            data = {
                'contents': [{
                    'parts': [{
                        'text': prompt
                    }]
                }],
                'generationConfig': {
                    'temperature': 0.7,
                    'maxOutputTokens': 200,
                }
            }
            
            response = requests.post(
                f"{self.base_url}?key={self.api_key}",
                headers=headers,
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and result['candidates']:
                    return result['candidates'][0]['content']['parts'][0]['text']
            
            return None
            
        except Exception:
            return None