"""
AI Service - Integração com Gemini AI para decisões inteligentes
"""
import os
import json
import requests
import asyncio
from typing import Optional, Dict, Any
from ..domain.interfaces import IDisplayService
from ..domain.entities import DevelopmentContext
from ..core.ports.ai_port import IAIService, AIAnalysisResult, ErrorContext, AnalysisType


class GeminiAIService(IAIService):
    """Serviço de integração com Gemini AI"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY', 'AIzaSyAad7j529fLDYA9IiTabQIOQ5jVv-cdLuo')
        self.model_name = "models/gemini-2.0-flash"  # Modelo testado e funcionando
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        
    def is_available(self) -> bool:
        """Verifica se o serviço está disponível"""
        return bool(self.api_key)

    # IAIService interface implementation
    async def analyze_error(self, error_context: ErrorContext) -> AIAnalysisResult:
        """Analyze an error and provide suggestions"""
        if not self.is_available():
            return AIAnalysisResult(
                analysis_type=AnalysisType.ERROR_ANALYSIS,
                confidence=0.0,
                findings=["AI service not available - check GEMINI_API_KEY"],
                suggestions=[],
                auto_fixable=False
            )
        
        prompt = f"""
Analise este erro de programação e forneça sugestões em português:

Erro: {error_context.error_message}
Contexto: {error_context.context}
Ambiente: {error_context.environment}

Forneça:
1. Análise do problema (máximo 2 linhas)
2. 2-3 sugestões práticas de correção
3. Comandos específicos se aplicável
"""
        
        try:
            response = await self._async_call_gemini(prompt)
            if response:
                suggestions = self._extract_suggestions(response)
                return AIAnalysisResult(
                    analysis_type=AnalysisType.ERROR_ANALYSIS,
                    confidence=0.8,
                    findings=[response],
                    suggestions=suggestions,
                    auto_fixable=len(suggestions) > 0
                )
        except Exception as e:
            pass
        
        return AIAnalysisResult(
            analysis_type=AnalysisType.ERROR_ANALYSIS,
            confidence=0.0,
            findings=["Erro ao conectar com o serviço AI"],
            suggestions=[],
            auto_fixable=False
        )

    async def explain_code(self, code: str, language: str = "python",
                          context: Dict[str, str] = None) -> AIAnalysisResult:
        """Explain what code does"""
        if not self.is_available():
            return AIAnalysisResult(
                analysis_type=AnalysisType.EXPLANATION,
                confidence=0.0,
                findings=["AI service not available - check GEMINI_API_KEY"],
                suggestions=[],
                auto_fixable=False
            )
        
        prompt = f"""
Explique este código {language} em português de forma clara e didática:

```{language}
{code}
```

Forneça:
1. O que o código faz (resumo em 1-2 linhas)
2. Como funciona (explicação detalhada)
3. Possíveis melhorias ou observações
"""
        
        try:
            response = await self._async_call_gemini(prompt)
            if response:
                suggestions = self._extract_suggestions(response)
                return AIAnalysisResult(
                    analysis_type=AnalysisType.EXPLANATION,
                    confidence=0.9,
                    findings=[response],
                    suggestions=suggestions,
                    auto_fixable=False
                )
        except Exception as e:
            pass
        
        return AIAnalysisResult(
            analysis_type=AnalysisType.EXPLANATION,
            confidence=0.0,
            findings=["Erro ao explicar código"],
            suggestions=[],
            auto_fixable=False
        )

    async def suggest_improvements(self, code: str, language: str = "python",
                                 focus: str = "general") -> AIAnalysisResult:
        """Suggest code improvements"""
        if not self.is_available():
            return AIAnalysisResult(
                analysis_type=AnalysisType.SUGGESTION,
                confidence=0.0,
                findings=["AI service not available - check GEMINI_API_KEY"],
                suggestions=[],
                auto_fixable=False
            )
        
        prompt = f"""
Analise este código {language} e sugira melhorias focando em: {focus}

```{language}
{code}
```

Forneça sugestões em português sobre:
1. Performance e otimização
2. Legibilidade e estrutura
3. Boas práticas e padrões
4. Correções ou melhorias específicas

Seja específico e prático nas sugestões.
"""
        
        try:
            response = await self._async_call_gemini(prompt)
            if response:
                suggestions = self._extract_suggestions(response)
                return AIAnalysisResult(
                    analysis_type=AnalysisType.SUGGESTION,
                    confidence=0.85,
                    findings=[response],
                    suggestions=suggestions,
                    auto_fixable=False
                )
        except Exception as e:
            pass
        
        return AIAnalysisResult(
            analysis_type=AnalysisType.SUGGESTION,
            confidence=0.0,
            findings=["Erro ao sugerir melhorias"],
            suggestions=[],
            auto_fixable=False
        )

    async def debug_assistance(self, problem_description: str,
                             code_context: str = "",
                             error_logs: str = "") -> AIAnalysisResult:
        """Provide debugging assistance"""
        prompt = f"""
Ajude a debugar/analisar este tópico em português com resposta COMPLETA e BEM ESTRUTURADA:

Tópico: {problem_description}

Código relacionado:
{code_context if code_context else 'Não fornecido'}

Logs de erro:
{error_logs if error_logs else 'Não fornecido'}

Forneça uma análise COMPLETA seguindo esta estrutura:

## 1. Análise do Problema
- Explicação clara do tópico/problema

## 2. Possíveis Causas  
- Liste as principais causas (se aplicável)

## 3. Passos para Debug/Resolução
- Passo a passo detalhado

## 4. Soluções e Exemplos
- Soluções práticas com exemplos de código quando aplicável
- Code snippets completos

IMPORTANTE: Complete toda a resposta sem cortar no meio.
"""
        
        try:
            response = await self._async_call_gemini(prompt)
            if response:
                suggestions = self._extract_suggestions(response)
                return AIAnalysisResult(
                    analysis_type=AnalysisType.DEBUGGING,
                    confidence=0.8,
                    findings=[response],
                    suggestions=suggestions,
                    auto_fixable=False
                )
        except Exception:
            pass
        
        return AIAnalysisResult(
            analysis_type=AnalysisType.DEBUGGING,
            confidence=0.0,
            findings=["Erro no debug assistance"],
            suggestions=[],
            auto_fixable=False
        )

    async def generate_fix(self, error_context: ErrorContext) -> Optional[str]:
        """Generate automated fix for error"""
        # Implementação básica - pode ser expandida
        analysis = await self.analyze_error(error_context)
        if analysis.suggestions:
            return analysis.suggestions[0] if analysis.suggestions else None
        return None

    async def validate_fix(self, original_error: str, proposed_fix: str) -> bool:
        """Validate if a proposed fix addresses the error"""
        # Implementação básica - validação por AI
        return len(proposed_fix.strip()) > 0

    async def get_model_info(self) -> Dict[str, str]:
        """Get information about the AI model being used"""
        return {
            "model": "gemini-1.5-flash",
            "provider": "Google AI",
            "version": "1.0",
            "available": str(self.is_available())
        }

    async def _async_call_gemini(self, prompt: str) -> Optional[str]:
        """Async version of Gemini API call"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._call_gemini, prompt)

    def _call_gemini(self, prompt: str) -> Optional[str]:
        """Chama a API do Gemini"""
        try:
            print(f"DEBUG: Calling Gemini with API key: {'YES' if self.api_key else 'NO'}")
            
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
                    'maxOutputTokens': 3000,  # Aumentado para respostas muito completas
                }
            }
            
            endpoint = f"{self.base_url}/{self.model_name}:generateContent"
            
            response = requests.post(
                f"{endpoint}?key={self.api_key}",
                headers=headers,
                json=data,
                timeout=30  # Aumentado para respostas maiores
            )
            
            print(f"DEBUG: Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"DEBUG: Response JSON: {result}")
                if 'candidates' in result and result['candidates']:
                    return result['candidates'][0]['content']['parts'][0]['text']
            else:
                print(f"DEBUG: Error response: {response.text}")
            
            return None
            
        except Exception as e:
            print(f"DEBUG: Exception calling Gemini: {e}")
            return None

    def _extract_suggestions(self, response: str) -> list[str]:
        """Extract suggestions from AI response"""
        lines = response.split('\n')
        suggestions = []
        for line in lines:
            line = line.strip()
            if line and (line.startswith('-') or line.startswith('•') or 
                        line.startswith('1.') or line.startswith('2.') or line.startswith('3.')):
                suggestions.append(line)
        return suggestions[:5]  # Limit to 5 suggestions

    # Legacy methods for backward compatibility
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
        
        Problema: {problem}
        
        Forneça uma solução específica em português (máximo 3 linhas):
        """
        
        return self._call_gemini(prompt)
    
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