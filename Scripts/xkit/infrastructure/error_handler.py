"""
Infrastructure - Error Handler Implementation
"""
import re
from typing import Optional, List, Dict
from datetime import datetime
from pathlib import Path

from ..domain import (
    XKitError, XPilotAnalysis, ErrorType, ErrorSeverity,
    IErrorHandler, IXPilotAgent
)


class ErrorHandler(IErrorHandler):
    """Implementation of error handling operations"""
    
    def __init__(self):
        self.errors: List[XKitError] = []
        self.error_counter = 0
        
    def create_error(self, message: str, command: str = "", context: str = "") -> XKitError:
        """Create a new error instance with type detection"""
        self.error_counter += 1
        
        # Detect error type based on message patterns
        error_type = self._detect_error_type(message)
        severity = self._determine_severity(error_type, message)
        
        error = XKitError(
            id=self.error_counter,
            message=message,
            command=command,
            context=context,
            error_type=error_type,
            severity=severity,
            timestamp=datetime.now()
        )
        
        return error
    
    def analyze_error(self, error: XKitError) -> XPilotAnalysis:
        """Analyze error and provide resolution suggestions"""
        analysis = XPilotAnalysis(summary="", suggestions=[], confidence=0.0)
        
        # Pattern-based analysis
        if error.error_type == ErrorType.COMMAND_NOT_FOUND:
            analysis.summary = f"🔍 Command not found error detected. '{error.command}' is not available."
            analysis.suggestions = [
                "Check if required plugins are loaded",
                "Verify function definition and scope",
                "Reload Oh My XKit framework",
                "Check if command is installed"
            ]
            analysis.auto_fix_available = True
            analysis.auto_fix_script = "reload_framework"
            analysis.confidence = 0.8
            
        elif error.error_type == ErrorType.SYNTAX_ERROR:
            analysis.summary = "📝 PowerShell syntax error detected. Code structure needs correction."
            analysis.suggestions = [
                "Review PowerShell syntax rules",
                "Check bracket and quote matching",
                "Validate variable declarations",
                "Remove unsupported characters or emojis"
            ]
            analysis.confidence = 0.7
            
        elif error.error_type == ErrorType.ACCESS_DENIED:
            analysis.summary = "🔒 Access denied error. Permission or path issue detected."
            analysis.suggestions = [
                "Run PowerShell as Administrator",
                "Check file/folder permissions",
                "Verify path accessibility",
                "Check if file is locked by another process"
            ]
            analysis.confidence = 0.9
            
        elif error.error_type == ErrorType.FILE_NOT_FOUND:
            analysis.summary = "📁 File not found error. Missing resource detected."
            analysis.suggestions = [
                "Verify file path accuracy",
                "Check if file exists",
                "Review working directory",
                "Check file name spelling"
            ]
            analysis.confidence = 0.9
            
        else:
            analysis.summary = "⚠️ General error detected. Requires manual analysis."
            analysis.suggestions = [
                "Review error context and command",
                "Check XKit documentation",
                "Search for similar issues",
                "Contact support if issue persists"
            ]
            analysis.confidence = 0.3
            
        return analysis
    
    def store_error(self, error: XKitError) -> None:
        """Store error for tracking"""
        self.errors.append(error)
        
        # Keep only last 50 errors to prevent memory issues
        if len(self.errors) > 50:
            self.errors = self.errors[-50:]
    
    def get_last_error(self) -> Optional[XKitError]:
        """Get the most recent error"""
        return self.errors[-1] if self.errors else None
    
    def get_error_count(self) -> int:
        """Get total error count"""
        return self.error_counter
    
    def _detect_error_type(self, message: str) -> ErrorType:
        """Detect error type based on message patterns"""
        message_lower = message.lower()
        
        patterns = {
            ErrorType.COMMAND_NOT_FOUND: [
                r"não é reconhecido como nome de cmdlet",
                r"not recognized as.*cmdlet",
                r"command not found",
                r"termo.*não é reconhecido"
            ],
            ErrorType.SYNTAX_ERROR: [
                r"syntax error",
                r"erro de sintaxe",
                r"token.*inesperado",
                r"unexpected token",
                r"caractere.*não é permitido"
            ],
            ErrorType.ACCESS_DENIED: [
                r"access.*denied",
                r"acesso.*negado",
                r"permission.*denied",
                r"unauthorized"
            ],
            ErrorType.FILE_NOT_FOUND: [
                r"file.*not.*found",
                r"arquivo.*não.*encontrado",
                r"cannot find.*file",
                r"path.*not.*found"
            ]
        }
        
        for error_type, pattern_list in patterns.items():
            for pattern in pattern_list:
                if re.search(pattern, message_lower):
                    return error_type
                    
        return ErrorType.GENERIC
    
    def _determine_severity(self, error_type: ErrorType, message: str) -> ErrorSeverity:
        """Determine error severity"""
        severity_map = {
            ErrorType.COMMAND_NOT_FOUND: ErrorSeverity.MEDIUM,
            ErrorType.SYNTAX_ERROR: ErrorSeverity.HIGH,
            ErrorType.ACCESS_DENIED: ErrorSeverity.HIGH,
            ErrorType.FILE_NOT_FOUND: ErrorSeverity.MEDIUM,
            ErrorType.GENERIC: ErrorSeverity.LOW
        }
        
        # Check for critical keywords
        critical_keywords = ["system", "critical", "fatal", "crash"]
        if any(keyword in message.lower() for keyword in critical_keywords):
            return ErrorSeverity.CRITICAL
            
        return severity_map.get(error_type, ErrorSeverity.MEDIUM)


class XPilotAgent(IXPilotAgent):
    """Local XPilot AI agent implementation"""
    
    def __init__(self, error_handler: ErrorHandler):
        self.error_handler = error_handler
    
    def analyze_error(self, error: XKitError) -> XPilotAnalysis:
        """Analyze error with enhanced AI-like logic"""
        # Use the error handler's analysis as base
        analysis = self.error_handler.analyze_error(error)
        
        # Enhance with XPilot-specific insights
        analysis.summary = f"🤖 @xpilot analysis: {analysis.summary}"
        
        # Add context-aware suggestions
        if error.context:
            analysis.suggestions.insert(0, f"Context suggests: Review '{error.context}' operation")
        
        if error.command:
            analysis.suggestions.insert(0, f"Command-specific: Verify '{error.command}' syntax and availability")
            
        return analysis
    
    def generate_auto_fix(self, error: XKitError) -> Optional[str]:
        """Generate automatic fix script if possible"""
        if error.error_type == ErrorType.COMMAND_NOT_FOUND:
            return """
# Auto-fix for command not found
. "$env:USERPROFILE\\Documents\\WindowsPowerShell\\oh-my-xkit\\oh-my-xkit.ps1"
Write-Host "Framework reloaded - try your command again"
"""
        return None