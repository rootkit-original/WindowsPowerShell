"""
AI Service Port
Interface for AI analysis and assistance services
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class AnalysisType(Enum):
    """Types of AI analysis"""
    ERROR_ANALYSIS = "error_analysis"
    CODE_REVIEW = "code_review"
    SUGGESTION = "suggestion"
    EXPLANATION = "explanation"
    OPTIMIZATION = "optimization"
    DEBUGGING = "debugging"


@dataclass
class AIAnalysisResult:
    """Result of AI analysis"""
    analysis_type: AnalysisType
    confidence: float
    findings: List[str]
    suggestions: List[str]
    auto_fixable: bool = False
    fix_commands: List[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.fix_commands is None:
            self.fix_commands = []
        if self.metadata is None:
            self.metadata = {}


@dataclass
class ErrorContext:
    """Context information for error analysis"""
    error_message: str
    error_type: str
    stack_trace: Optional[str] = None
    command: Optional[str] = None
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    environment: Dict[str, str] = None
    
    def __post_init__(self):
        if self.environment is None:
            self.environment = {}


class IAIService(ABC):
    """Port for AI services"""
    
    @abstractmethod
    async def analyze_error(self, error_context: ErrorContext) -> AIAnalysisResult:
        """Analyze an error and provide suggestions"""
        pass
    
    @abstractmethod
    async def explain_code(self, code: str, language: str = "python",
                          context: Dict[str, str] = None) -> AIAnalysisResult:
        """Explain what code does"""
        pass
    
    @abstractmethod
    async def suggest_improvements(self, code: str, language: str = "python",
                                 focus: str = "general") -> AIAnalysisResult:
        """Suggest code improvements"""
        pass
    
    @abstractmethod
    async def debug_assistance(self, problem_description: str,
                             code_context: str = "",
                             error_logs: str = "") -> AIAnalysisResult:
        """Provide debugging assistance"""
        pass
    
    @abstractmethod
    async def generate_fix(self, error_context: ErrorContext) -> Optional[str]:
        """Generate automated fix for error"""
        pass
    
    @abstractmethod
    async def validate_fix(self, original_error: str, proposed_fix: str) -> bool:
        """Validate if a proposed fix addresses the error"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if AI service is available"""
        pass
    
    @abstractmethod
    async def get_model_info(self) -> Dict[str, str]:
        """Get information about the AI model being used"""
        pass