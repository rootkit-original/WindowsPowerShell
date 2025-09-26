"""
Command Adapter
Adapter that implements ICommandService using the existing infrastructure
"""
import asyncio
import logging
from typing import Dict, List, Optional, Any, Callable

from ...core.ports import ICommandService, IDisplayService, IEventService, IAIService
from ...core.ports.command_port import CommandResult
from ...core.ports.ai_port import ErrorContext
from ...events import CommandExecutedEvent, CommandFailedEvent


class CommandAdapter(ICommandService):
    """Command service adapter using existing XKit infrastructure"""
    
    def __init__(self, display_service: IDisplayService, 
                 event_service: Optional[IEventService] = None,
                 ai_service: Optional[IAIService] = None):
        self.display_service = display_service
        self.event_service = event_service
        self.ai_service = ai_service
        self.logger = logging.getLogger(__name__)
        
        # Command registry
        self._commands: Dict[str, Dict[str, Any]] = {}
        self._handlers: Dict[str, Callable] = {}
        
        # Register default commands
        self._register_default_commands()
    
    def _register_default_commands(self) -> None:
        """Register default XKit commands"""
        default_commands = {
            # Core commands
            "help": {
                "handler": self._handle_help,
                "description": "Show help information",
                "category": "core"
            },
            "status": {
                "handler": self._handle_status,
                "description": "Show system status",
                "category": "core"
            },
            "version": {
                "handler": self._handle_version,
                "description": "Show XKit version",
                "category": "core"
            },
            "list-commands": {
                "handler": self._handle_list_commands,
                "description": "List all available commands",
                "category": "core"
            },
            
            # MCP commands
            "mcp-status": {
                "handler": self._handle_mcp_status,
                "description": "Show MCP system status",
                "category": "mcp"
            },
            "mcp-servers": {
                "handler": self._handle_mcp_servers,
                "description": "List MCP servers",
                "category": "mcp"
            },
            "mcp-tools": {
                "handler": self._handle_mcp_tools,
                "description": "List MCP tools",
                "category": "mcp"
            },
            
            # Plugin commands
            "plugin-list": {
                "handler": self._handle_plugin_list,
                "description": "List loaded plugins",
                "category": "plugins"
            },
            
            # Event commands
            "events-status": {
                "handler": self._handle_events_status,
                "description": "Show event system status",
                "category": "events"
            },
            
            # Debug commands
            "debug": {
                "handler": self._handle_debug,
                "description": "System diagnostics",
                "category": "debug"
            },
            
            # AI commands
            "ai-analyze": {
                "handler": self._handle_ai_analyze,
                "description": "AI-powered analysis and suggestions",
                "category": "ai"
            },
            "ai-explain-code": {
                "handler": self._handle_ai_explain,
                "description": "AI code explanation",
                "category": "ai"
            },
            "ai-suggest": {
                "handler": self._handle_ai_suggest,
                "description": "AI improvement suggestions",
                "category": "ai"
            }
        }
        
        for cmd, info in default_commands.items():
            self._commands[cmd] = info
            self._handlers[cmd] = info["handler"]
    
    async def execute_command(self, command: str, args: List[str] = None, 
                            context: Dict[str, Any] = None) -> CommandResult:
        """Execute a command"""
        start_time = asyncio.get_event_loop().time()
        
        if args is None:
            args = []
        if context is None:
            context = {}
        
        try:
            # Validate command
            if not self.validate_command(command, args):
                error = f"Invalid command or arguments: {command}"
                await self._publish_command_failed(command, args, error)
                return CommandResult(
                    success=False,
                    error=error,
                    execution_time=asyncio.get_event_loop().time() - start_time
                )
            
            # Get handler
            handler = self._handlers.get(command)
            if not handler:
                error = f"No handler found for command: {command}"
                await self._publish_command_failed(command, args, error)
                return CommandResult(
                    success=False,
                    error=error,
                    execution_time=asyncio.get_event_loop().time() - start_time
                )
            
            # Execute handler
            if asyncio.iscoroutinefunction(handler):
                result = await handler(args, context)
            else:
                result = handler(args, context)
            
            execution_time = asyncio.get_event_loop().time() - start_time
            
            # Create result
            command_result = CommandResult(
                success=True,
                output=result,
                execution_time=execution_time,
                metadata={"command": command, "args": args}
            )
            
            # Publish success event
            await self._publish_command_executed(command, args, result, execution_time)
            
            return command_result
            
        except Exception as e:
            execution_time = asyncio.get_event_loop().time() - start_time
            error_msg = str(e)
            
            self.logger.error(f"Command execution failed: {command} - {error_msg}")
            
            # Publish failure event
            await self._publish_command_failed(command, args, error_msg)
            
            return CommandResult(
                success=False,
                error=error_msg,
                execution_time=execution_time
            )
    
    def list_available_commands(self) -> List[str]:
        """Get list of available commands"""
        return sorted(self._commands.keys())
    
    def get_command_help(self, command: str) -> Optional[str]:
        """Get help text for a specific command"""
        if command not in self._commands:
            return None
        
        cmd_info = self._commands[command]
        return cmd_info.get("description", "No description available")
    
    def register_command(self, command: str, handler: callable, 
                        description: str = "", category: str = "general") -> bool:
        """Register a new command handler"""
        try:
            self._commands[command] = {
                "handler": handler,
                "description": description,
                "category": category
            }
            self._handlers[command] = handler
            
            self.logger.info(f"Registered command: {command} ({category})")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to register command {command}: {e}")
            return False
    
    def unregister_command(self, command: str) -> bool:
        """Unregister a command handler"""
        if command not in self._commands:
            return False
        
        try:
            del self._commands[command]
            del self._handlers[command]
            
            self.logger.info(f"Unregistered command: {command}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to unregister command {command}: {e}")
            return False
    
    def validate_command(self, command: str, args: List[str] = None) -> bool:
        """Validate command and arguments before execution"""
        if not command or not isinstance(command, str):
            return False
        
        if command not in self._commands:
            return False
        
        # Basic argument validation (could be enhanced)
        if args is not None and not isinstance(args, list):
            return False
        
        return True
    
    # Default command handlers
    async def _handle_help(self, args: List[str], context: Dict[str, Any]) -> str:
        """Handle help command with detailed examples and usage"""
        if args and len(args) > 0:
            # Help for specific command with detailed usage
            command = args[0]
            return self._get_detailed_command_help(command)
        else:
            # Enhanced general help with examples
            return self._get_comprehensive_help()
    
    def _get_comprehensive_help(self) -> str:
        """Get comprehensive help with examples and usage patterns"""
        help_lines = [
            "🚀 XKit v3.0 - Hybrid MCP Architecture",
            "═" * 50,
            "",
            "💡 Standardized Command Structure:",
            "  xkit <command> <params>     # New standardized format",
            "  <command> <params>          # Legacy format (still works)",
            "",
            "🌟 Quick Start Examples:",
            "  xkit help                   # Show this help",
            "  xkit status                 # Check system status", 
            "  xkit version                # Show version info",
            "  xkit mcp status             # Check MCP servers",
            "  xkit plugin list            # List loaded plugins",
            "",
            "🔗 MCP (Model Context Protocol) Commands:",
            "  xkit mcp status             Show MCP servers and connection status",
            "  xkit mcp servers            List all configured MCP servers with details", 
            "  xkit mcp tools              List tools available from MCP servers",
            "  xkit mcp call <tool>        Execute an MCP tool",
            "",
            "🧩 Plugin System Commands:",
            "  xkit plugin list            Show loaded plugins and their status",
            "  xkit plugin load <name>     Load a specific plugin",
            "  xkit plugin reload <name>   Reload a plugin with hot-reload",
            "  xkit plugin unload <name>   Unload a plugin",
            "",
            "📡 Event System Commands:",
            "  xkit events status          Show event bus metrics and activity",
            "  xkit events history         Show recent event history",
            "  xkit events clear           Clear event history",
            "",
            "� Git Integration Commands:",
            "  xkit git status             Enhanced git status with MCP integration",
            "  xkit git branch             List and manage branches",
            "  xkit git create-branch      Create new branch with XKit conventions",
            "",
            "🤖 AI Assistant Commands:",
            "  xkit ai analyze <text>      AI-powered analysis and suggestions",
            "  xkit ai explain <code>      Explain code functionality",
            "  xkit ai suggest <context>   Get improvement suggestions",
            "",
            "💎 Core System Commands:",
            "  xkit help [command]         Show help (detailed help for specific command)",
            "  xkit status                 Show complete system status and health",
            "  xkit version                Show XKit version and architecture info",
            "  xkit config [key] [value]   Manage XKit configuration",
            "  xkit init                   Initialize XKit system",
            "",
            "🔧 Debug and Diagnostics:",
            "  xkit debug                  Run system diagnostics and health checks",
            "  xkit debug system           Detailed system diagnostics",
            "  xkit debug mcp              Debug MCP connections",
            "  xkit debug plugins          Debug plugin system",
            "",
            "🎯 Usage Pattern Examples:",
            "  # Check everything is working",
            "  xkit status",
            "",
            "  # Work with MCP servers",
            "  xkit mcp status",
            "  xkit mcp servers",
            "",
            "  # Manage plugins", 
            "  xkit plugin list",
            "  xkit plugin load my-plugin",
            "",
            "  # Use AI features",
            "  xkit ai analyze \"explain this error\"",
            "",
            "  # Git operations with XKit enhancements",
            "  xkit git status",
            "  xkit git create-branch feature my-new-feature",
            "",
            "📚 Command Structure Benefits:",
            "  • Consistent: All commands follow xkit <command> <params> pattern",
            "  • Hierarchical: Related commands grouped (mcp, plugin, events, etc.)",
            "  • Discoverable: Easy to explore with tab completion",
            "  • Backward Compatible: Old command names still work",
            "",
            "🌟 Pro Tips:",
            "  • Use TAB completion: type 'xkit m[TAB]' to see mcp commands",
            "  • Commands are case-insensitive: XKIT STATUS works too",
            "  • Get detailed help: xkit help mcp (shows all mcp subcommands)",
            "  • Use 'xkit debug' if any command isn't working as expected",
            "",
            "💡 Architecture:",
            "  • PowerShell provides the xkit command interface",
            "  • Python backend handles all complex logic and processing",
            "  • MCP protocol enables extensible tool integration",
            "  • Plugin system supports hot-reload for development",
            ""
        ]
        
        return "\n".join(help_lines)
    
    def _get_detailed_command_help(self, command: str) -> str:
        """Get detailed help for a specific command"""
        detailed_help = {
            "help": {
                "description": "Show help information with examples and usage patterns",
                "usage": [
                    "help                    # Show general help with all commands",
                    "help <command>          # Show detailed help for specific command"
                ],
                "examples": [
                    "help                    # Show this comprehensive help",
                    "help mcp-status         # Get detailed help for mcp-status command",
                    "help plugin-list        # Learn how to use plugin-list command"
                ]
            },
            "status": {
                "description": "Show complete XKit system status and health information",
                "usage": ["status                     # Show system status"],
                "examples": [
                    "status                  # Check if XKit is running properly",
                    "# Shows: Architecture status, services health, component status"
                ]
            },
            "version": {
                "description": "Display XKit version and architecture information",
                "usage": ["version                    # Show version info"],
                "examples": [
                    "version                 # See current XKit version and architecture",
                    "# Shows: v3.0.0, Hybrid MCP Architecture, components status"
                ]
            },
            "mcp-status": {
                "description": "Check Model Context Protocol servers status and connections",
                "usage": ["mcp-status                 # Show MCP system status"],
                "examples": [
                    "mcp-status              # Check if MCP servers are running",
                    "# Shows: Connection status, server count, health info"
                ]
            },
            "mcp-servers": {
                "description": "List all configured MCP servers with detailed information",
                "usage": ["mcp-servers                # List MCP servers"],
                "examples": [
                    "mcp-servers             # See all available MCP servers",
                    "# Shows: Server names, types, status, descriptions, commands"
                ]
            },
            "mcp-tools": {
                "description": "Display tools available from connected MCP servers",
                "usage": ["mcp-tools                  # List available MCP tools"],
                "examples": [
                    "mcp-tools               # See what tools you can use",
                    "# Shows: Tool names, descriptions, server sources"
                ]
            },
            "plugin-list": {
                "description": "Show loaded plugins and their current status",
                "usage": ["plugin-list                # List loaded plugins"],
                "examples": [
                    "plugin-list             # See what plugins are loaded",
                    "# Shows: Plugin names, versions, status, capabilities"
                ]
            },
            "events-status": {
                "description": "Display event system metrics and activity information",
                "usage": ["events-status              # Show event bus status"],
                "examples": [
                    "events-status           # Check event system health",
                    "# Shows: Event counts, processing times, error rates"
                ]
            },
            "debug": {
                "description": "Run comprehensive system diagnostics and health checks",
                "usage": ["debug                      # Run system diagnostics"],
                "examples": [
                    "debug                   # Diagnose any system issues",
                    "# Shows: Component health, error details, troubleshooting tips"
                ]
            },
            "list-commands": {
                "description": "List all available commands organized by category",
                "usage": ["list-commands              # List all commands"],
                "examples": [
                    "list-commands           # See all available commands",
                    "# Shows: Commands grouped by category (Core, MCP, Plugins, etc.)"
                ]
            }
        }
        
        if command not in detailed_help:
            return f"❓ No detailed help available for command: {command}\n💡 Use 'list-commands' to see available commands"
        
        info = detailed_help[command]
        help_lines = [
            f"📖 {command.upper()} - Detailed Help",
            "═" * (len(command) + 20),
            "",
            f"📝 Description:",
            f"  {info['description']}",
            "",
            f"🔧 Usage:",
        ]
        
        for usage in info['usage']:
            help_lines.append(f"  {usage}")
        
        help_lines.extend([
            "",
            f"💡 Examples:",
        ])
        
        for example in info['examples']:
            help_lines.append(f"  {example}")
        
        help_lines.extend([
            "",
            f"🌟 Tips:",
            f"  • This command works in PowerShell through Python backend",
            f"  • Use 'help' without arguments to see all commands",
            f"  • Use 'debug' if this command isn't working properly"
        ])
        
        return "\n".join(help_lines)
    
    async def _handle_status(self, args: List[str], context: Dict[str, Any]) -> str:
        """Handle status command"""
        return "✅ XKit system is running (Hybrid MCP Architecture v3.0)"
    
    async def _handle_version(self, args: List[str], context: Dict[str, Any]) -> str:
        """Handle version command"""
        return "🏗️ XKit v3.0.0 (Hybrid MCP Architecture)"
    
    async def _handle_list_commands(self, args: List[str], context: Dict[str, Any]) -> str:
        """Handle list-commands command"""
        commands = self.list_available_commands()
        categories = self._group_commands_by_category()
        
        result_lines = [f"📋 Available Commands ({len(commands)} total):"]
        for category, cmds in categories.items():
            result_lines.append(f"\n📂 {category.title()}: {', '.join(cmds)}")
        
        return "\n".join(result_lines)
    
    def _group_commands_by_category(self) -> Dict[str, List[str]]:
        """Group commands by category"""
        categories = {}
        
        for command, info in self._commands.items():
            category = info.get("category", "general")
            if category not in categories:
                categories[category] = []
            categories[category].append(command)
        
        # Sort commands within each category
        for category in categories:
            categories[category].sort()
        
        return categories

    # New command handlers for MCP, Plugins, Events, Debug
    async def _handle_mcp_status(self, args: List[str], context: Dict[str, Any]) -> str:
        """Handle MCP status command"""
        return "🔌 MCP Status: System operational (placeholder implementation)"

    async def _handle_mcp_servers(self, args: List[str], context: Dict[str, Any]) -> str:
        """Handle MCP servers command"""
        return "🔌 MCP Servers: 5 servers configured (placeholder implementation)"

    async def _handle_mcp_tools(self, args: List[str], context: Dict[str, Any]) -> str:
        """Handle MCP tools command"""
        return "🛠️  MCP Tools: Available tools listing (placeholder implementation)"

    async def _handle_plugin_list(self, args: List[str], context: Dict[str, Any]) -> str:
        """Handle plugin list command"""
        return "🧩 Plugins: No plugins currently loaded (placeholder implementation)"

    async def _handle_events_status(self, args: List[str], context: Dict[str, Any]) -> str:
        """Handle events status command"""
        return "📡 Event System: Active and operational (placeholder implementation)"

    async def _handle_debug(self, args: List[str], context: Dict[str, Any]) -> str:
        """Handle debug command"""
        return "🔧 Debug: XKit v3.0 Hybrid MCP Architecture operational (placeholder implementation)"
    
    async def _publish_command_executed(self, command: str, args: List[str], 
                                       result: Any, execution_time: float) -> None:
        """Publish command executed event"""
        if not self.event_service:
            return
        
        event = CommandExecutedEvent(
            command=command,
            args=args,
            result=result,
            success=True,
            execution_time=execution_time,
            source="command_adapter"
        )
        
        await self.event_service.publish(event)
    
    async def _publish_command_failed(self, command: str, args: List[str], 
                                     error_message: str) -> None:
        """Publish command failed event"""
        if not self.event_service:
            return
        
        event = CommandFailedEvent(
            command=command,
            args=args,
            error_message=error_message,
            error_type="execution_error",
            source="command_adapter"
        )
        
        await self.event_service.publish(event)

    # AI Command Handlers
    def _format_ai_response(self, title: str, query: str, result) -> str:
        """Format AI response with clean console output"""
        if result.confidence == 0:
            error_msg = f"❌ {title} Failed: {result.findings[0] if result.findings else 'Unknown error'}"
            print(error_msg)
            return error_msg
        
        # Print directly for better formatting
        print()
        print("="*60)
        print(f"🤖 {title}")
        print("="*60)
        print(f"📝 Query: {query}")
        print(f"🎯 Confidence: {result.confidence:.0%}")
        print("─"*60)
        print()
        
        # Findings/Analysis
        if result.findings:
            print("🔍 ANALYSIS:")
            for finding in result.findings:
                # Clean up the finding text and print line by line
                clean_finding = finding.replace("**", "").strip()
                # Split by newlines and print each line
                for line in clean_finding.split('\n'):
                    if line.strip():
                        print(line)
            print()
        
        # Suggestions
        if result.suggestions:
            print("💡 SUGGESTIONS:")
            for i, suggestion in enumerate(result.suggestions, 1):
                clean_suggestion = suggestion.replace("**", "").strip()
                print(f"   {i}. {clean_suggestion}")
            print()
        
        # Footer
        print("─"*60)
        print("✅ Analysis completed successfully")
        print("="*60)
        print()
        
        # Return a simple confirmation message
        return f"✅ {title} completed successfully"

    async def _handle_ai_analyze(self, args: List[str], context: Dict[str, Any]) -> str:
        """Handle AI analysis command"""
        if not args:
            return """🤖 XKit AI Analysis

Usage: xkit ai analyze "your question or text"

The AI analysis feature uses advanced AI models to provide:
• Code analysis and insights
• Problem-solving suggestions  
• Architecture recommendations
• Best practice advice

Example:
  xkit ai analyze "how to optimize this Python function"
  xkit ai analyze "explain this error message"
  xkit ai analyze "suggest improvements for this code"

💡 Tip: Use quotes around complex text with spaces"""

        if not self.ai_service or not self.ai_service.is_available():
            return """❌ AI Service Not Available

The AI service is not configured or the API key is missing.

🔧 Setup Instructions:
1. Configure GEMINI_API_KEY in your environment
2. Make sure the key is valid and active
3. Restart XKit

💡 Your key should be set in PowerShell profile:
$env:GEMINI_API_KEY = 'your-api-key-here'"""

        query = " ".join(args)
        
        try:
            # Use debug_assistance for general analysis
            result = await self.ai_service.debug_assistance(
                problem_description=query,
                code_context="",
                error_logs=""
            )
            
            return self._format_ai_response("AI ERROR ANALYSIS", query, result)
                
        except Exception as e:
            return f"❌ AI Service Error: {str(e)}"

    async def _handle_ai_explain(self, args: List[str], context: Dict[str, Any]) -> str:
        """Handle AI code explanation command"""
        if not args:
            return """🤖 XKit AI Code Explanation

Usage: xkit ai explain "your code here"

The AI explanation feature provides:
• Line-by-line code breakdown
• Function and class explanations
• Algorithm analysis
• Performance insights

Example:
  xkit ai explain "def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)"

💡 Tip: Works best with complete functions or code blocks"""
        
        if not self.ai_service or not self.ai_service.is_available():
            return """❌ AI Service Not Available

Configure GEMINI_API_KEY to enable AI code explanation."""

        code = " ".join(args)
        
        try:
            result = await self.ai_service.explain_code(
                code=code,
                language="python",  # Default, could be enhanced to detect language
                context=context
            )
            
            return self._format_ai_response("AI CODE EXPLANATION", code, result)
                
        except Exception as e:
            return f"❌ AI Service Error: {str(e)}"

    async def _handle_ai_suggest(self, args: List[str], context: Dict[str, Any]) -> str:
        """Handle AI suggestions command"""
        if not args:
            return """🤖 XKit AI Suggestions

Usage: xkit ai suggest "describe what you want to improve"

Get AI-powered suggestions for:
• Code optimization
• Architecture improvements  
• Tool recommendations
• Best practices

Example:
  xkit ai suggest "make this API faster"
  xkit ai suggest "improve error handling"

💡 Context-aware suggestions based on your XKit environment"""

        if not self.ai_service or not self.ai_service.is_available():
            return """❌ AI Service Not Available

Configure GEMINI_API_KEY to enable AI suggestions."""

        context_text = " ".join(args)
        
        try:
            # Treat the suggestion request as code to be improved
            result = await self.ai_service.suggest_improvements(
                code=context_text,
                language="general",
                focus="optimization"
            )
            
            return self._format_ai_response("AI SUGGESTIONS", context_text, result)
                
        except Exception as e:
            return f"❌ AI Service Error: {str(e)}"