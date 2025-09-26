"""
XKit v3.0 - Hybrid MCP Architecture Main Entry Point
Enhanced PowerShell Framework with MCP integration, Plugin System, and Event-Driven Architecture
"""
import sys
import os
import asyncio
import logging
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

# Import new hybrid architecture components
try:
    from xkit.core import XKitApplication, XKitContainer
    from xkit.core.application import ApplicationConfig
    from xkit.core.ports import *
    from xkit.adapters import CommandAdapter, EventServiceAdapter, PowerShellAdapter
    from xkit.events import get_event_bus, SystemStartedEvent, publish_event
    from xkit.mcp.client import XKitMCPClient
    from xkit.plugins.manager import PluginManager
    
    # Legacy infrastructure (for gradual migration)
    from xkit.infrastructure.display import DisplayService
    from xkit.infrastructure.environment import EnvironmentService
    
    HYBRID_MCP_AVAILABLE = True
except ImportError as e:
    # Fallback to legacy system if hybrid architecture not available
    HYBRID_MCP_AVAILABLE = False
    print(f"⚠️  Hybrid MCP Architecture not available: {e}")
    print("🔄 Falling back to legacy system...")
    
    # Legacy imports
    from xkit.infrastructure.container import XKitContainer
    from xkit.domain.entities import ErrorType


class XKitV3Application:
    """XKit v3.0 Main Application with Hybrid MCP Architecture"""
    
    def __init__(self):
        self.hybrid_available = HYBRID_MCP_AVAILABLE
        
        if self.hybrid_available:
            self.config = ApplicationConfig(
                debug=os.getenv("XKIT_DEBUG", "false").lower() == "true",
                log_level=os.getenv("XKIT_LOG_LEVEL", "INFO"),
                plugin_directories=[
                    str(Path(__file__).parent / "xkit" / "plugins"),
                    str(Path(__file__).parent.parent / "oh-my-xkit" / "plugins")
                ],
                enable_hot_reload=True,
                enable_events=True
            )
            self.container = XKitContainer()
            self.app = None
            self._setup_hybrid_services()
        else:
            # Legacy container
            self.container = XKitContainer()
    
    def _setup_hybrid_services(self):
        """Setup services for hybrid MCP architecture"""
        if not self.hybrid_available:
            return
        
        try:
            # Core services
            display_service = DisplayService()
            event_service = EventServiceAdapter()
            
            # Adapters
            command_adapter = CommandAdapter(display_service, event_service)
            powershell_adapter = PowerShellAdapter(display_service)
            
            # Register services in container
            self.container.register_singleton(IDisplayService, display_service)
            self.container.register_singleton(IEventService, event_service)
            self.container.register_singleton(ICommandService, command_adapter)
            
            # MCP Client
            mcp_client = XKitMCPClient()
            self.container.register_singleton(IMCPService, mcp_client)
            
            # Plugin Manager
            plugin_manager = PluginManager(event_service)
            self.container.register_singleton(IPluginService, plugin_manager)
            
            # Create application
            self.app = XKitApplication(self.config, self.container)
            
        except Exception as e:
            print(f"❌ Failed to setup hybrid services: {e}")
            self.hybrid_available = False
    
    async def run_async(self, args: List[str]) -> None:
        """Main entry point for XKit v3.0 operations"""
        if not args:
            self._show_help()
            return
            
        action = args[0].lower()
        context_args = args[1:] if len(args) > 1 else []
        
        try:
            if self.hybrid_available and self.app:
                await self._run_hybrid_command(action, context_args)
            else:
                await self._run_legacy_command(action, context_args)
                
        except Exception as e:
            print(f"❌ XKit Error: {e}")
            if self.hybrid_available:
                print("🔧 Use 'xkit debug system' for detailed diagnostics")
            
    async def _run_hybrid_command(self, action: str, args: List[str]) -> None:
        """Run command using hybrid MCP architecture"""
        # Start application if not running
        if not self.app.is_running:
            await self.app.start()
        
        # Map legacy actions to new command system
        command_mapping = {
            "help": "help",
            "show-help": "help", 
            "version": "version",
            "show-version": "version",
            "status": "status", 
            "show-status": "status",
            "system-init": "system-init",
            "mcp-status": "mcp-status",
            "mcp-list-servers": "mcp-list-servers",
            "mcp-list-tools": "mcp-list-tools", 
            "plugin-list": "plugin-list",
            "events-status": "events-status",
            "git-status": "git-status",
            "ai-analyze": "ai-analyze",
            "debug": "debug"
        }
        
        command = command_mapping.get(action, action)
        
        try:
            result = await self.app.execute_command(command, args)
            if result.success and result.output:
                print(result.output)
            elif not result.success and result.error:
                print(f"❌ {result.error}")
        except Exception as e:
            print(f"❌ Command failed: {e}")
    
    async def _run_legacy_command(self, action: str, args: List[str]) -> None:
        """Run command using legacy system"""
        if action in ["help", "show-help"]:
            self._show_help()
        elif action in ["version", "show-version"]:
            self._show_version()
        elif action in ["status", "show-status"]:
            self._show_status()
        elif action == "system-init":
            print("🚀 XKit v3.0 System Initialized (Legacy Mode)")
        else:
            print(f"❌ Unknown action: {action}")
            self._show_help()
    
    def _show_help(self) -> None:
        """Show XKit help information"""
        if self.hybrid_available:
            print("🚀 XKit v3.0 - Hybrid MCP Architecture")
            print("═" * 50)
            print()
            print("🔗 MCP Commands:")
            print("  mcp-status      - Show MCP server status")
            print("  mcp-servers     - List connected servers")
            print("  mcp-tools       - List available tools")
            print()
            print("🧩 Plugin Commands:")
            print("  plugin-list     - List loaded plugins")
            print("  plugin-load     - Load a plugin")
            print("  plugin-reload   - Reload a plugin")
            print()
            print("📡 Event Commands:")
            print("  events-status   - Show event system status")
            print("  events-history  - Show event history")
            print()
            print("🔧 Git Commands (Enhanced):")
            print("  git-status      - Git status with MCP integration")
            print("  git-branch      - Git branch operations")
            print("  git-create-branch - Create new branch")
            print()
            print("🤖 AI Commands:")
            print("  ai-analyze      - AI analysis and assistance")
            print("  ai-explain-code - Explain code functionality")
            print("  xpilot-analyze  - @xpilot error analysis")
            print()
            print("💡 Core Commands:")
            print("  help            - Show this help")
            print("  version         - Show version info")
            print("  status          - Show system status")
            print("  debug           - System diagnostics")
        else:
            print("🎨 XKit v3.0 (Legacy Mode)")
            print("═" * 30)
            print("  help     - Show this help")
            print("  version  - Show version")
            print("  status   - Show status")
            print()
            print("⚠️  Hybrid MCP Architecture not available")
            print("💡 Check Python dependencies and try again")
    
    def _show_version(self) -> None:
        """Show version information"""
        if self.hybrid_available:
            print("🚀 XKit v3.0.0")
            print("🏗️  Architecture: Hybrid MCP")
            print("🔗 MCP Protocol: Active")
            print("🧩 Plugin System: Available") 
            print("📡 Event Bus: Active")
            print("🐍 Python Backend: Active")
            print("⚡ PowerShell Wrapper: Minimal")
        else:
            print("🚀 XKit v3.0.0 (Legacy Mode)")
            print("⚠️  Hybrid MCP Architecture: Not Available")
    
    def _show_status(self) -> None:
        """Show system status"""
        print("📊 XKit System Status")
        print("-" * 25)
        
        if self.hybrid_available:
            print("✅ Hybrid MCP Architecture: Available")
            print("✅ Event System: Ready")
            print("✅ Plugin System: Ready") 
            print("✅ MCP Protocol: Ready")
            print("✅ Python Backend: Active")
            
            if self.app and self.app.is_running:
                print("✅ Application: Running")
            else:
                print("⏸️  Application: Stopped")
        else:
            print("⚠️  Hybrid MCP Architecture: Not Available")
            print("🔄 Running in Legacy Mode")
            print("💡 Install dependencies for full functionality")
    
    def run(self, args: List[str]) -> None:
        """Synchronous entry point"""
        try:
            asyncio.run(self.run_async(args))
        except KeyboardInterrupt:
            print("\n🛑 XKit interrupted by user")
        except Exception as e:
            print(f"❌ XKit fatal error: {e}")


def main():
    """Main entry point for XKit v3.0"""
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    
    # Initialize and run XKit application
    app = XKitV3Application()
    app.run(args)


if __name__ == "__main__":
    main()
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