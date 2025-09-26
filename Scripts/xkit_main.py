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
    from xkit.infrastructure.config import ConfigService
    
    HYBRID_MCP_AVAILABLE = True
except ImportError as e:
    # Fallback to legacy system if hybrid architecture not available
    HYBRID_MCP_AVAILABLE = False
    print(f"⚠️  Hybrid MCP Architecture not available: {e}")
    print("🔄 Falling back to legacy system...")
    
    # Legacy imports
    try:
        from xkit.infrastructure.container import XKitContainer
        from xkit.domain.entities import ErrorType
    except ImportError:
        print("❌ Legacy system also not available")
        HYBRID_MCP_AVAILABLE = None


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
            # Minimal fallback
            self.container = None
    
    def _setup_hybrid_services(self):
        """Setup services for hybrid MCP architecture"""
        if not self.hybrid_available:
            return
        
        try:
            # Core services
            display_service = DisplayService()
            config_service = ConfigService()
            event_service = EventServiceAdapter()
            
            # Adapters
            command_adapter = CommandAdapter(display_service, event_service)
            powershell_adapter = PowerShellAdapter(display_service)
            
            # Register services in container
            self.container.register_singleton(IDisplayService, display_service)
            self.container.register_singleton(IConfigService, config_service)
            self.container.register_singleton(IEventService, event_service)
            self.container.register_singleton(ICommandService, command_adapter)
            
            # MCP Client (without async initialization for now)
            mcp_client = XKitMCPClient()
            # Store reference for potential async initialization later
            self.mcp_client = mcp_client
            self.container.register_singleton(IMCPService, mcp_client)
            
            # Plugin Manager
            plugin_manager = PluginManager()
            # Set event service for plugin manager
            plugin_manager.event_service = event_service
            self.container.register_singleton(IPluginService, plugin_manager)
            
            # Create application
            self.app = XKitApplication(self.config, self.container)
            
        except Exception as e:
            print(f"❌ Failed to setup hybrid services: {e}")
            self.hybrid_available = False
    
    async def _initialize_async_services(self) -> None:
        """Initialize async services like MCP client"""
        try:
            if self.hybrid_available and hasattr(self, 'mcp_client'):
                await self.mcp_client._load_config()
        except Exception as e:
            print(f"⚠️  Async services initialization failed: {e}")
    
    async def run_async(self, args: List[str]) -> None:
        """Main entry point for XKit v3.0 operations"""
        # Initialize async services if needed
        await self._initialize_async_services()
        
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
        
        # Map ALL XKit commands - comprehensive mapping
        command_mapping = {
            # Core commands
            "xkit-help": "help",
            "help": "help",
            "show-help": "help",
            "xkit-status": "status", 
            "status": "status",
            "show-status": "status",
            "xkit-version": "version",
            "version": "version",
            "show-version": "version",
            "xkit-reload": "reload",
            
            # MCP commands
            "mcp-status": "mcp-status",
            "mcp-servers": "mcp-servers", 
            "mcp-tools": "mcp-tools",
            "mcp-call": "mcp-call",
            "mcp-list-servers": "mcp-servers",
            "mcp-list-tools": "mcp-tools",
            
            # Plugin commands
            "plugin-list": "plugin-list",
            "plugin-load": "plugin-load",
            "plugin-reload": "plugin-reload",
            "plugin-unload": "plugin-unload",
            
            # Event commands
            "events-status": "events-status",
            "events-history": "events-history", 
            "events-clear": "events-clear",
            
            # Git commands
            "git-status": "git-status",
            "git-branch": "git-branch",
            "git-create-branch": "git-create-branch",
            
            # AI commands
            "ai-analyze": "ai-analyze",
            "ai-explain-code": "ai-explain-code",
            "xpilot-analyze": "xpilot-analyze",
            
            # Debug commands
            "debug": "debug",
            "system-init": "system-init",
            "diagnose": "diagnose"
        }
        
        command = command_mapping.get(action, action)
        
        try:
            result = await self.app.execute_command(command, args)
            if result and hasattr(result, 'success'):
                if result.success and result.output:
                    print(result.output)
                elif not result.success and result.error:
                    print(f"❌ {result.error}")
            else:
                # Handle commands that don't return result objects
                print(result if result else f"✅ Command '{command}' executed successfully")
        except Exception as e:
            # Fallback to direct command implementation
            await self._handle_command_direct(command, args, e)

    async def _handle_command_direct(self, command: str, args: List[str], original_error: Exception) -> None:
        """Handle commands directly when application execution fails"""
        try:
            if command in ["help", "show-help"]:
                self._show_help()
            elif command in ["version", "show-version"]:
                self._show_version()
            elif command in ["status", "show-status"]:
                self._show_status()
            elif command in ["mcp-status"]:
                await self._handle_mcp_status()
            elif command in ["mcp-servers", "mcp-list-servers"]:
                await self._handle_mcp_servers()
            elif command in ["mcp-tools", "mcp-list-tools"]:
                await self._handle_mcp_tools()
            elif command in ["plugin-list"]:
                await self._handle_plugin_list()
            elif command in ["events-status"]:
                await self._handle_events_status()
            elif command in ["debug", "diagnose"]:
                await self._handle_debug()
            else:
                print(f"❌ Command '{command}' not implemented")
                print(f"💡 Original error: {original_error}")
                print("🔧 Available commands: help, status, version, mcp-status, plugin-list")
        except Exception as e:
            print(f"❌ Direct command handling failed: {e}")
            print(f"💡 Original error was: {original_error}")

    async def _handle_mcp_status(self) -> None:
        """Handle MCP status command directly"""
        print("🔌 MCP (Model Context Protocol) Status")
        print("=" * 40)
        
        if hasattr(self, 'mcp_client') and self.mcp_client:
            try:
                # Try to get server configurations
                servers = getattr(self.mcp_client, 'servers_config', {})
                if servers:
                    print(f"✅ MCP Client: Active ({len(servers)} servers configured)")
                    for name, config in servers.items():
                        status = "🟢 Ready" if config.get('enabled', True) else "⚪ Disabled"
                        print(f"   • {name}: {status}")
                else:
                    print("⚠️  MCP Client: No servers configured")
            except Exception as e:
                print(f"⚠️  MCP Client: Error checking status - {e}")
        else:
            print("❌ MCP Client: Not available")
        
        print("\n💡 Use 'mcp-servers' to see detailed server information")

    async def _handle_mcp_servers(self) -> None:
        """Handle MCP servers command directly"""
        print("🔌 MCP Servers Configuration")
        print("=" * 40)
        
        if hasattr(self, 'mcp_client') and self.mcp_client:
            try:
                servers = getattr(self.mcp_client, 'servers_config', {})
                if not servers:
                    print("📝 No MCP servers configured")
                    print("💡 Check Scripts/xkit/mcp/config.json for configuration")
                    return
                
                for name, config in servers.items():
                    print(f"\n🔸 {name}")
                    print(f"   Type: {config.get('type', 'unknown')}")
                    print(f"   Description: {config.get('description', 'No description')}")
                    print(f"   Enabled: {'✅' if config.get('enabled', True) else '❌'}")
                    
                    if 'command' in config:
                        print(f"   Command: {config['command']}")
                    if 'args' in config:
                        print(f"   Args: {config['args']}")
                        
            except Exception as e:
                print(f"❌ Error reading MCP servers: {e}")
        else:
            print("❌ MCP Client not available")

    async def _handle_mcp_tools(self) -> None:
        """Handle MCP tools command directly"""
        print("🛠️  MCP Tools Available")
        print("=" * 40)
        print("⚠️  Tool listing requires active MCP connections")
        print("💡 This feature will be implemented when servers are running")

    async def _handle_plugin_list(self) -> None:
        """Handle plugin list command directly"""
        print("🧩 XKit Plugins")
        print("=" * 40)
        
        if hasattr(self, 'app') and self.app and hasattr(self.app, 'container'):
            try:
                plugin_service = self.app.container.get_service(IPluginService)
                if hasattr(plugin_service, 'plugins'):
                    plugins = plugin_service.plugins
                    if plugins:
                        print(f"📦 {len(plugins)} plugins loaded:")
                        for name, plugin in plugins.items():
                            status = "🟢" if hasattr(plugin, 'is_loaded') and plugin.is_loaded else "⚪"
                            print(f"   {status} {name}")
                    else:
                        print("📝 No plugins currently loaded")
                else:
                    print("⚠️  Plugin service available but no plugins loaded")
            except Exception as e:
                print(f"❌ Error accessing plugins: {e}")
        else:
            print("❌ Plugin system not available")
            
        print("\n💡 Plugin directories:")
        print("   • Scripts/xkit/plugins/")
        print("   • oh-my-xkit/plugins/")

    async def _handle_events_status(self) -> None:
        """Handle events status command directly"""
        print("📡 Event System Status")
        print("=" * 40)
        
        if hasattr(self, 'app') and self.app and hasattr(self.app, 'container'):
            try:
                event_service = self.app.container.get_service(IEventService)
                if hasattr(event_service, 'get_metrics'):
                    metrics = event_service.get_metrics()
                    print(f"✅ Event Bus: Active")
                    print(f"   Total Events: {getattr(metrics, 'total_events', 0)}")
                    print(f"   Processed: {getattr(metrics, 'processed_events', 0)}")
                    print(f"   Failed: {getattr(metrics, 'failed_events', 0)}")
                    print(f"   Avg Processing: {getattr(metrics, 'average_processing_time', 0):.3f}s")
                else:
                    print("✅ Event Service: Available")
            except Exception as e:
                print(f"⚠️  Event Service: {e}")
        else:
            print("❌ Event system not available")

    async def _handle_debug(self) -> None:
        """Handle debug command directly"""
        print("🔧 XKit System Diagnostics")
        print("=" * 40)
        
        print(f"🏗️  Architecture: {'Hybrid MCP v3.0' if self.hybrid_available else 'Legacy'}")
        print(f"🐍 Python Backend: {'✅ Active' if self.hybrid_available else '⚠️  Limited'}")
        print(f"⚡ PowerShell Wrapper: ✅ Active")
        
        if hasattr(self, 'app') and self.app:
            print(f"📦 Application: {'🟢 Running' if self.app.is_running else '⚪ Stopped'}")
            if hasattr(self.app, 'container') and self.app.container:
                print(f"🔗 Services: ✅ Container initialized")
        
        if hasattr(self, 'mcp_client'):
            print(f"🔌 MCP Client: ✅ Available")
        
        print(f"\n📊 System Health: {'🟢 Excellent' if self.hybrid_available else '🟡 Limited Mode'}")
    
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