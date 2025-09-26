"""
Command Adapter
Adapter that implements ICommandService using the existing infrastructure
"""
import asyncio
import logging
from typing import Dict, List, Optional, Any, Callable

from ...core.ports import ICommandService, IDisplayService, IEventService
from ...core.ports.command_port import CommandResult
from ...events import CommandExecutedEvent, CommandFailedEvent


class CommandAdapter(ICommandService):
    """Command service adapter using existing XKit infrastructure"""
    
    def __init__(self, display_service: IDisplayService, 
                 event_service: Optional[IEventService] = None):
        self.display_service = display_service
        self.event_service = event_service
        self.logger = logging.getLogger(__name__)
        
        # Command registry
        self._commands: Dict[str, Dict[str, Any]] = {}
        self._handlers: Dict[str, Callable] = {}
        
        # Register default commands
        self._register_default_commands()
    
    def _register_default_commands(self) -> None:
        """Register default XKit commands"""
        default_commands = {
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
        """Handle help command"""
        if args and len(args) > 0:
            # Help for specific command
            command = args[0]
            help_text = self.get_command_help(command)
            if help_text:
                return f"📖 {command}: {help_text}"
            else:
                return f"❓ No help available for command: {command}"
        else:
            # General help
            commands = self.list_available_commands()
            categories = self._group_commands_by_category()
            
            help_lines = ["🚀 XKit Commands:"]
            for category, cmds in categories.items():
                help_lines.append(f"\n📂 {category.title()}:")
                for cmd in cmds:
                    desc = self.get_command_help(cmd)
                    help_lines.append(f"  • {cmd} - {desc}")
            
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