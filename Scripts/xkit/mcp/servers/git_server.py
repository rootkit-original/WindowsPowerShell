"""
Git MCP Server
Provides Git operations through MCP protocol
"""
import asyncio
from typing import Dict, Any, List, Optional
from pathlib import Path
import subprocess

from ..protocol import MCPServer, Tool


class XKitGitServer(MCPServer):
    """Git operations MCP server"""
    
    def __init__(self):
        super().__init__("xkit-git", "1.0.0")
    
    async def list_tools(self) -> List[Tool]:
        """List available Git tools"""
        return [
            Tool(
                name="git-status",
                description="Get current Git repository status",
                input_schema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Repository path (default: current directory)"
                        }
                    },
                    "required": []
                }
            ),
            Tool(
                name="git-branch-info",
                description="Get information about Git branches",
                input_schema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Repository path (default: current directory)"
                        },
                        "include_remote": {
                            "type": "boolean",
                            "description": "Include remote branches",
                            "default": True
                        }
                    },
                    "required": []
                }
            ),
            Tool(
                name="git-commit-info",
                description="Get recent commit information",
                input_schema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Repository path (default: current directory)"
                        },
                        "count": {
                            "type": "integer",
                            "description": "Number of commits to show",
                            "default": 10,
                            "minimum": 1,
                            "maximum": 100
                        }
                    },
                    "required": []
                }
            ),
            Tool(
                name="git-create-branch",
                description="Create a new Git branch with XKit naming conventions",
                input_schema={
                    "type": "object",
                    "properties": {
                        "branch_name": {
                            "type": "string",
                            "description": "Name for the new branch"
                        },
                        "branch_type": {
                            "type": "string",
                            "description": "Type of branch",
                            "enum": ["feature", "fix", "refactor", "docs", "test"]
                        },
                        "from_branch": {
                            "type": "string",
                            "description": "Base branch (default: current branch)"
                        }
                    },
                    "required": ["branch_name", "branch_type"]
                }
            )
        ]
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a Git tool with given arguments"""
        if name == "git-status":
            path = arguments.get("path", ".")
            return await self._git_status(path)
        elif name == "git-branch-info":
            path = arguments.get("path", ".")
            include_remote = arguments.get("include_remote", True)
            return await self._git_branch_info(path, include_remote)
        elif name == "git-commit-info":
            path = arguments.get("path", ".")
            count = arguments.get("count", 10)
            return await self._git_commit_info(path, count)
        elif name == "git-create-branch":
            branch_name = arguments.get("branch_name")
            branch_type = arguments.get("branch_type")
            from_branch = arguments.get("from_branch")
            return await self._git_create_branch(branch_name, branch_type, from_branch)
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    async def _run_git_command(self, args: List[str], cwd: str = ".") -> Dict[str, Any]:
        """Run a git command and return result"""
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip()
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Git command timed out",
                "returncode": -1
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "returncode": -1
            }
    
    async def _git_status(self, path: str) -> Dict[str, Any]:
        """Get Git repository status"""
        result = await self._run_git_command(["status", "--porcelain", "-b"], cwd=path)
        
        if not result["success"]:
            return {
                "error": "Failed to get git status",
                "details": result
            }
        
        status_lines = result["stdout"].split("\n") if result["stdout"] else []
        branch_line = status_lines[0] if status_lines else ""
        file_lines = status_lines[1:] if len(status_lines) > 1 else []
        
        return {
            "branch_info": branch_line,
            "modified_files": len([line for line in file_lines if line.startswith(" M")]),
            "added_files": len([line for line in file_lines if line.startswith("A ")]),
            "deleted_files": len([line for line in file_lines if line.startswith(" D")]),
            "untracked_files": len([line for line in file_lines if line.startswith("??")]),
            "total_changes": len(file_lines),
            "clean": len(file_lines) == 0,
            "files": file_lines,
            "source": "xkit-git-server"
        }
    
    async def _git_branch_info(self, path: str, include_remote: bool) -> Dict[str, Any]:
        """Get Git branch information"""
        args = ["branch", "-v"]
        if include_remote:
            args.append("-a")
        
        result = await self._run_git_command(args, cwd=path)
        
        if not result["success"]:
            return {
                "error": "Failed to get branch info",
                "details": result
            }
        
        branches = []
        current_branch = None
        
        for line in result["stdout"].split("\n"):
            line = line.strip()
            if line:
                is_current = line.startswith("*")
                branch_info = line[2:] if is_current else line
                parts = branch_info.split()
                
                if parts:
                    branch_name = parts[0]
                    if is_current:
                        current_branch = branch_name
                    
                    branches.append({
                        "name": branch_name,
                        "current": is_current,
                        "remote": branch_name.startswith("remotes/"),
                        "info": branch_info
                    })
        
        return {
            "current_branch": current_branch,
            "branches": branches,
            "total_branches": len(branches),
            "local_branches": len([b for b in branches if not b["remote"]]),
            "remote_branches": len([b for b in branches if b["remote"]]),
            "source": "xkit-git-server"
        }
    
    async def _git_commit_info(self, path: str, count: int) -> Dict[str, Any]:
        """Get recent commit information"""
        result = await self._run_git_command(
            ["log", f"-{count}", "--oneline", "--decorate"],
            cwd=path
        )
        
        if not result["success"]:
            return {
                "error": "Failed to get commit info",
                "details": result
            }
        
        commits = []
        for line in result["stdout"].split("\n"):
            line = line.strip()
            if line:
                parts = line.split(" ", 1)
                if len(parts) >= 2:
                    commits.append({
                        "hash": parts[0],
                        "message": parts[1]
                    })
        
        return {
            "commits": commits,
            "count": len(commits),
            "requested_count": count,
            "source": "xkit-git-server"
        }
    
    async def _git_create_branch(self, branch_name: str, branch_type: str, from_branch: Optional[str]) -> Dict[str, Any]:
        """Create a new Git branch with XKit naming conventions"""
        # Apply XKit naming convention
        full_branch_name = f"{branch_type}/{branch_name}"
        
        # Get current branch if from_branch not specified
        if not from_branch:
            current_result = await self._run_git_command(["branch", "--show-current"])
            if current_result["success"]:
                from_branch = current_result["stdout"] or "main"
            else:
                from_branch = "main"
        
        # Create branch
        result = await self._run_git_command(["checkout", "-b", full_branch_name, from_branch])
        
        return {
            "success": result["success"],
            "branch_name": full_branch_name,
            "base_branch": from_branch,
            "branch_type": branch_type,
            "naming_convention": "xkit-standard",
            "details": result,
            "source": "xkit-git-server"
        }