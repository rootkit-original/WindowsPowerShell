"""
PowerShell Adapter
Adapter for integrating with PowerShell commands and environment
"""
import asyncio
import subprocess
import logging
from typing import Dict, List, Optional, Any, Tuple

from ...core.ports import ICommandService, IDisplayService
from ...core.ports.command_port import CommandResult


class PowerShellAdapter:
    """Adapter for PowerShell integration"""
    
    def __init__(self, display_service: IDisplayService):
        self.display_service = display_service
        self.logger = logging.getLogger(__name__)
        self.powershell_path = "powershell.exe"
    
    async def execute_powershell(self, command: str, 
                               capture_output: bool = True) -> CommandResult:
        """Execute a PowerShell command"""
        start_time = asyncio.get_event_loop().time()
        
        try:
            # Prepare command
            ps_command = [
                self.powershell_path,
                "-NoProfile",
                "-ExecutionPolicy", "Bypass",
                "-Command", command
            ]
            
            # Execute command
            process = await asyncio.create_subprocess_exec(
                *ps_command,
                stdout=subprocess.PIPE if capture_output else None,
                stderr=subprocess.PIPE if capture_output else None,
                text=True
            )
            
            stdout, stderr = await process.communicate()
            execution_time = asyncio.get_event_loop().time() - start_time
            
            success = process.returncode == 0
            
            return CommandResult(
                success=success,
                output=stdout.strip() if stdout else None,
                error=stderr.strip() if stderr else None,
                execution_time=execution_time,
                metadata={"return_code": process.returncode}
            )
            
        except Exception as e:
            execution_time = asyncio.get_event_loop().time() - start_time
            self.logger.error(f"PowerShell execution failed: {e}")
            
            return CommandResult(
                success=False,
                error=str(e),
                execution_time=execution_time
            )
    
    async def invoke_xkit_python(self, action: str, args: List[str] = None) -> CommandResult:
        """Invoke XKit Python main entry point"""
        if args is None:
            args = []
        
        # Build PowerShell command to call Python
        python_script = r"$env:USERPROFILE\Documents\WindowsPowerShell\Scripts\xkit_main.py"
        ps_command = f"python '{python_script}' {action} {' '.join(args)}"
        
        return await self.execute_powershell(ps_command)
    
    def format_powershell_output(self, result: CommandResult) -> str:
        """Format PowerShell command result for display"""
        if result.success:
            return result.output or ""
        else:
            error_msg = result.error or "Unknown error"
            return f"❌ PowerShell Error: {error_msg}"
    
    def escape_powershell_string(self, value: str) -> str:
        """Escape string for safe PowerShell execution"""
        # Basic escaping for PowerShell strings
        return value.replace("'", "''").replace('"', '`"')
    
    def build_powershell_args(self, args_dict: Dict[str, Any]) -> str:
        """Build PowerShell argument string from dictionary"""
        ps_args = []
        
        for key, value in args_dict.items():
            if isinstance(value, bool):
                if value:
                    ps_args.append(f"-{key}")
            elif isinstance(value, (int, float)):
                ps_args.append(f"-{key} {value}")
            elif isinstance(value, str):
                escaped = self.escape_powershell_string(value)
                ps_args.append(f"-{key} '{escaped}'")
            elif isinstance(value, list):
                items = [f"'{self.escape_powershell_string(str(item))}'"
                        for item in value]
                ps_args.append(f"-{key} @({','.join(items)})")
        
        return " ".join(ps_args)
    
    async def test_powershell_availability(self) -> bool:
        """Test if PowerShell is available"""
        try:
            result = await self.execute_powershell("$PSVersionTable.PSVersion.Major")
            return result.success and result.output
        except Exception:
            return False
    
    async def get_powershell_version(self) -> Optional[str]:
        """Get PowerShell version"""
        try:
            result = await self.execute_powershell("$PSVersionTable.PSVersion.ToString()")
            return result.output if result.success else None
        except Exception:
            return None
    
    async def get_environment_info(self) -> Dict[str, str]:
        """Get PowerShell environment information"""
        info = {}
        
        try:
            # Get basic environment info
            commands = {
                "ps_version": "$PSVersionTable.PSVersion.ToString()",
                "execution_policy": "Get-ExecutionPolicy",
                "current_user": "$env:USERNAME",
                "computer_name": "$env:COMPUTERNAME",
                "ps_profile": "$PROFILE",
                "current_dir": "Get-Location | Select-Object -ExpandProperty Path"
            }
            
            for key, command in commands.items():
                result = await self.execute_powershell(command)
                info[key] = result.output if result.success else "unknown"
                
        except Exception as e:
            self.logger.error(f"Failed to get environment info: {e}")
        
        return info