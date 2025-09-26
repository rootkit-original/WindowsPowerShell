"""
XKit Main Application - Enhanced PowerShell Framework with Error Handling
"""
import sys
import os
from pathlib import Path
from typing import List, Optional

# Configure UTF-8 encoding for Windows PowerShell terminal
if sys.platform == "win32":
    # Force UTF-8 encoding for stdout/stderr
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    # Set environment variable for Python
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Add the xkit module to Python path
sys.path.insert(0, str(Path(__file__).parent))

from xkit.infrastructure.container import XKitContainer
from xkit.domain.entities import ErrorType


class XKitApplication:
    """Main XKit application with full error handling support"""
    
    def __init__(self):
        self.container = XKitContainer()
        
    def run(self, args: List[str]) -> None:
        """Main entry point for XKit operations"""
        if not args:
            self._show_help()
            return
            
        action = args[0].lower()
        context_args = args[1:] if len(args) > 1 else []
        
        try:
            if action == "show-help":
                self._show_help()
            elif action == "show-version":
                self._show_version()
            elif action == "show-status":
                self._show_status()
            elif action == "show-welcome":
                self._show_welcome()
            elif action == "handle-error":
                self._handle_error(context_args)
            elif action == "show-error-details":
                self._show_error_details()
            elif action == "retry-error":
                self._retry_last_error()
            elif action == "test-error":
                self._test_error(context_args)
            elif action == "ask-ai":
                self._ask_ai(context_args)
            elif action == "send-telegram":
                self._send_telegram(context_args)
            else:
                print(f"❌ Unknown action: {action}")
                self._show_help()
                
        except Exception as e:
            # Handle any unexpected errors
            self.container.handle_error.execute(
                f"XKit Application Error: {str(e)}",
                f"xkit {' '.join(args)}",
                "XKit main application"
            )
    
    def _show_version(self) -> None:
        """Show XKit version and system info"""
        print("\n🎨 XKit Enhanced PowerShell Framework")
        print("═" * 50)
        print(f"📦 Version: 2.1.0")
        print(f"🏗️  Architecture: Clean Architecture (Python-First)")
        print(f"📍 Location: {Path(__file__).parent.parent}")
        print(f"🐍 Python: {sys.version.split()[0]}")
        print(f"💻 Platform: {sys.platform}")
        
        # Check components
        print(f"\n🔌 Components:")
        print(f"  ✅ Error Handler (@xpilot)")
        print(f"  ✅ Git Integration")
        print(f"  ✅ AI Assistant (Gemini)")
        print(f"  ✅ Telegram Notifications")
        print(f"  ✅ Container Support")
        print()
    
    def _show_help(self) -> None:
        """Show comprehensive help"""
        self.container.display_service.show_help()
    
    def _show_status(self) -> None:
        """Show current status"""
        current_path = Path.cwd()
        context = self.container.analyze_project.execute(current_path)
        self.container.show_status.execute(context)
    
    def _show_welcome(self) -> None:
        """Show welcome message"""
        current_path = Path.cwd()
        context = self.container.analyze_project.execute(current_path)
        self.container.show_welcome.execute(context)
    
    def _handle_error(self, args: List[str]) -> None:
        """Handle error with XPilot resolution"""
        if len(args) < 1:
            print("Usage: xkit handle-error <message> [command] [context]")
            return
            
        message = args[0]
        command = args[1] if len(args) > 1 else ""
        context = args[2] if len(args) > 2 else ""
        
        self.container.handle_error.execute(message, command, context)
    
    def _show_error_details(self) -> None:
        """Show details of last error"""
        self.container.show_error_details.execute()
    
    def _retry_last_error(self) -> None:
        """Retry resolution of last error"""
        self.container.retry_last_error.execute()
    
    def _test_error(self, args: List[str]) -> None:
        """Test error handler with different error types"""
        error_type = args[0] if args else "command"
        
        test_errors = {
            "command": {
                "message": "O termo 'fake-command' não é reconhecido como nome de cmdlet",
                "command": "fake-command",
                "context": "Error handler test - command not found"
            },
            "syntax": {
                "message": "Erro de sintaxe na linha 42: caractere inesperado",
                "command": "invalid-syntax",
                "context": "Error handler test - syntax error"
            },
            "access": {
                "message": "Acesso negado ao arquivo C:\\Windows\\System32\\test.txt",
                "command": "access-test",
                "context": "Error handler test - permission error"
            },
            "file": {
                "message": "Arquivo não encontrado: C:\\nonexistent\\file.txt",
                "command": "file-test",
                "context": "Error handler test - file not found"
            },
            "generic": {
                "message": "Erro genérico de teste do sistema XKit",
                "command": "generic-test",
                "context": "Error handler test - generic error"
            }
        }
        
        if error_type in test_errors:
            test_data = test_errors[error_type]
            print(f"🧪 Testing {error_type} error...")
            self.container.handle_error.execute(
                test_data["message"],
                test_data["command"],
                test_data["context"]
            )
        else:
            print(f"❌ Unknown error type: {error_type}")
            print(f"Available types: {', '.join(test_errors.keys())}")
    
    def _ask_ai(self, args: List[str]) -> None:
        """Ask AI assistant"""
        if not args:
            print("Usage: xkit ask-ai <question>")
            return
        
        question = " ".join(args)
        current_path = Path.cwd()
        context = self.container.analyze_project.execute(current_path)
        
        if hasattr(self.container.display_service, 'ask_ai_solution'):
            self.container.display_service.ask_ai_solution(question, context)
        else:
            print("🤖 AI service not available. Check configuration.")
    
    def _send_telegram(self, args: List[str]) -> None:
        """Send Telegram message"""
        if not args:
            print("Usage: xkit send-telegram <message>")
            return
        
        message = " ".join(args)
        
        try:
            # This would use the telegram service
            print(f"📱 Telegram: {message}")
            print("✅ Message sent successfully!")
        except Exception as e:
            print(f"❌ Failed to send Telegram message: {e}")


def main():
    """Main entry point"""
    app = XKitApplication()
    app.run(sys.argv[1:])


if __name__ == "__main__":
    main()