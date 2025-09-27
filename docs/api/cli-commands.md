# 📟 CLI Commands Reference

> **Complete XKit v3.0 Command-Line Interface Reference**

This document provides comprehensive reference for all XKit commands, including hybrid MCP architecture commands, legacy shortcuts, and plugin-provided functionality.

## 🎯 Quick Navigation

| Category | Commands | Description |
|----------|----------|-------------|
| [Core Commands](#core-commands) | `help`, `version`, `status`, `debug` | System information and diagnostics |
| [MCP Commands](#mcp-commands) | `mcp-status`, `mcp-servers`, `mcp-tools` | MCP server management |
| [Plugin Commands](#plugin-commands) | `plugin-list`, `plugin-load`, `plugin-reload` | Plugin system management |
| [Event Commands](#event-commands) | `events-status`, `events-history` | Event system monitoring |
| [Git Commands](#git-commands) | `git-status`, `git-branch`, `smart-commit` | Enhanced Git operations |
| [AI Commands](#ai-commands) | `ai-analyze`, `xpilot-analyze` | AI-powered assistance |
| [Legacy Shortcuts](#legacy-shortcuts) | `gs`, `ga`, `gc`, `d`, `dc` | Quick command shortcuts |

## 💻 Command Usage

### PowerShell Integration

XKit commands are available in PowerShell through multiple methods:

```powershell
# Method 1: Direct Python execution
python Scripts\xkit_main.py <command> [args]

# Method 2: PowerShell functions (when profile is loaded)
xkit-status
git-enhanced-status

# Method 3: Legacy shortcuts (oh-my-xkit style)
gs          # git status
ga .        # git add .
gcm "msg"   # git commit -m "msg"
```

### General Syntax

```bash
xkit <command> [options] [arguments]
python Scripts/xkit_main.py <command> [options] [arguments]
```

## 🏗️ Core Commands

### `help` / `show-help`

Display comprehensive help information.

```powershell
# Show general help
xkit help

# Show help for specific command (future enhancement)
xkit help git-status
```

**Output Example:**
```
🚀 XKit v3.0 - Hybrid MCP Architecture
═══════════════════════════════════════════════════

🔗 MCP Commands:
  mcp-status      - Show MCP server status
  mcp-servers     - List connected servers
  mcp-tools       - List available tools
...
```

### `version` / `show-version`

Display version and architecture information.

```powershell
xkit version
```

**Output:**
```
🚀 XKit v3.0.0
🏗️  Architecture: Hybrid MCP
🔗 MCP Protocol: Active
🧩 Plugin System: Available
📡 Event Bus: Active
🐍 Python Backend: Active
⚡ PowerShell Wrapper: Minimal
```

### `status` / `show-status`

Show comprehensive system status.

```powershell
xkit status
```

**Output Example:**
```
🚀 XKit v3.0 System Status
═══════════════════════════

🏗️  Architecture: Hybrid MCP (✅ Active)
🔌 MCP Client: ✅ Connected (3 servers)
🧩 Plugin Manager: ✅ Active (5 plugins loaded)
📡 Event Bus: ✅ Active
   Total Events: 1,234
   Processed: 1,230
   Failed: 4
   Avg Processing: 0.025s

📊 System Health: 🟢 Excellent
```

### `debug`

Detailed system diagnostics and troubleshooting information.

```powershell
xkit debug
```

**Output:**
```
🔧 XKit System Diagnostics
════════════════════════════

🏗️  Architecture: Hybrid MCP v3.0
🐍 Python Backend: ✅ Active
⚡ PowerShell Wrapper: ✅ Active
📦 Application: 🟢 Running
🔗 Services: ✅ Container initialized
🔌 MCP Client: ✅ Available

📊 System Health: 🟢 Excellent
```

## 🔌 MCP Commands

### `mcp-status`

Show status of all MCP servers.

```powershell
xkit mcp-status
```

**Output Example:**
```
🔌 MCP Servers Status
══════════════════════

✅ xkit-core (internal) - 7 tools available
✅ xkit-ai (internal) - 5 tools available  
✅ xkit-git (internal) - 8 tools available
⚠️  xkit-container (internal) - Disabled
❌ filesystem (external) - Connection failed

📊 3/5 servers active, 20 total tools
```

### `mcp-servers`

List all configured MCP servers.

```powershell
# List all servers
xkit mcp-servers

# List only active servers
xkit mcp-servers --active

# Show detailed server info
xkit mcp-servers --detailed
```

**Options:**
- `--active` - Show only connected servers
- `--detailed` - Include server configuration details
- `--tools` - Include available tools count

### `mcp-tools [server]`

List available tools from MCP servers.

```powershell
# List tools from all servers
xkit mcp-tools

# List tools from specific server
xkit mcp-tools xkit-ai

# List with descriptions
xkit mcp-tools --detailed

# Filter by tool name pattern
xkit mcp-tools --filter git-*
```

**Output Example:**
```
🔧 MCP Tools Available
═══════════════════════

📦 xkit-core (7 tools):
  • system-info - Get system information
  • project-analyze - Analyze current project  
  • config-get - Get configuration values
  • config-set - Set configuration values

🤖 xkit-ai (5 tools):
  • analyze-error - Analyze error messages
  • generate-code - Generate code from description
  • code-review - Review code for improvements

🔗 xkit-git (8 tools):
  • git-status - Enhanced git status
  • git-commit - Intelligent commit with AI
  • git-branch - Branch operations
```

## 🧩 Plugin Commands

### `plugin-list`

List all loaded plugins with their status.

```powershell
# List all plugins
xkit plugin-list

# List with detailed info
xkit plugin-list --detailed

# List only active plugins
xkit plugin-list --active
```

**Output Example:**
```
🧩 Loaded Plugins
══════════════════

✅ git-enhanced v1.2.0 (Active)
   Commands: smart-commit, ai-review, suggest-branch
   
✅ monitoring v1.0.0 (Active)  
   Commands: metrics, health-check
   
⚠️  database-plugin v0.9.0 (Error)
   Error: Missing dependency: psycopg2

📊 2/3 plugins active, 5 commands available
```

### `plugin-load <plugin>`

Load or reload a specific plugin.

```powershell
# Load plugin from file
xkit plugin-load path/to/plugin.py

# Load plugin by name
xkit plugin-load git-enhanced

# Load with verbose output
xkit plugin-load monitoring --verbose
```

### `plugin-reload <plugin>`

Hot-reload a specific plugin without restarting XKit.

```powershell
# Reload specific plugin
xkit plugin-reload git-enhanced

# Reload all plugins
xkit plugin-reload --all

# Force reload (ignore errors)
xkit plugin-reload monitoring --force
```

### `plugin-info <plugin>`

Get detailed information about a plugin.

```powershell
xkit plugin-info git-enhanced
```

**Output:**
```
📦 Plugin Information: git-enhanced
════════════════════════════════════

📝 Description: Enhanced Git operations with AI assistance
👤 Author: XKit Team
📅 Version: 1.2.0
🔗 Dependencies: gitpython>=3.1.0, openai>=1.0.0

📋 Commands Provided:
  • smart-commit - AI-powered intelligent commits
  • ai-review - AI-powered code review
  • suggest-branch - AI branch name suggestions

⚙️ Services Required:
  • ai_service - AI analysis and generation
  • git_service - Git operations interface
  • display_service - UI and notifications

📊 Status: ✅ Active (Hot-reload enabled)
🔄 Last Loaded: 2025-09-27 10:30:15
```

## 📡 Event Commands

### `events-status`

Show event system status and metrics.

```powershell
xkit events-status
```

**Output:**
```
📡 Event System Status
════════════════════════

🚌 Event Bus: ✅ Active
📊 Metrics:
  Total Events: 5,678
  Processed: 5,670
  Failed: 8
  Average Processing: 0.015s

📈 Events by Type:
  CommandExecutedEvent: 2,340
  GitOperationEvent: 1,890
  PluginLifecycleEvent: 45
  ErrorOccurredEvent: 8

🔀 Active Subscriptions: 23
⚡ Performance: 🟢 Excellent (15ms avg)
```

### `events-history [count]`

Show recent event history.

```powershell
# Show last 10 events
xkit events-history

# Show last 50 events  
xkit events-history 50

# Show events with details
xkit events-history --detailed

# Filter by event type
xkit events-history --type GitOperationEvent
```

**Output Example:**
```
📜 Recent Event History (Last 10)
════════════════════════════════════

🕐 2025-09-27 10:45:23 - CommandExecutedEvent
   Command: git-status, Success: ✅, Duration: 0.12s

🕐 2025-09-27 10:45:20 - GitOperationEvent  
   Operation: status, Branch: main, Success: ✅

🕐 2025-09-27 10:45:18 - PluginLifecycleEvent
   Plugin: git-enhanced, Event: command_registered
```

### `events-subscribe <event-type>`

Subscribe to real-time events (for debugging).

```powershell
# Subscribe to all events
xkit events-subscribe "*"

# Subscribe to specific event type
xkit events-subscribe CommandExecutedEvent

# Subscribe with filter
xkit events-subscribe GitOperationEvent --filter "success=true"
```

## 🔗 Git Commands (Enhanced)

### `git-status`

Enhanced git status with AI insights and MCP integration.

```powershell
# Basic enhanced status
xkit git-status

# Compact format
xkit git-status --compact

# Include branch information
xkit git-status --branch

# Include AI suggestions
xkit git-status --ai-insights
```

**Output Example:**
```
📁 Repository Status: my-project (main)
════════════════════════════════════════

🌿 Branch: main (🔄 2 ahead, 1 behind origin/main)

📊 Working Directory:
  📝 Modified: 3 files
    • src/main.py (45 lines changed)
    • docs/README.md (12 lines changed)  
    • tests/test_main.py (8 lines changed)

  📋 Staged: 1 file
    • src/utils.py (new file)

  ❓ Untracked: 2 files  
    • temp/debug.log
    • .vscode/settings.json

💡 AI Suggestions:
  • Consider staging README.md changes for documentation
  • Add .vscode/ to .gitignore
  • Run tests before committing main.py changes
```

### `git-branch`

Enhanced branch operations with AI suggestions.

```powershell
# List branches with enhanced info
xkit git-branch

# Create new branch with AI naming
xkit git-branch --create --ai-name

# Switch to branch
xkit git-branch --switch feature/new-api

# Delete merged branches
xkit git-branch --cleanup
```

### `smart-commit`

AI-powered intelligent commit functionality.

```powershell
# Smart commit with AI-generated message
xkit smart-commit

# Smart commit specific files
xkit smart-commit src/main.py tests/test_main.py

# Review before committing
xkit smart-commit --review

# Conventional commits format
xkit smart-commit --conventional
```

**Workflow:**
1. Analyzes staged changes
2. Generates appropriate commit message using AI
3. Shows preview for confirmation
4. Commits with generated message

### `git-create-branch`

Create new branch with intelligent naming suggestions.

```powershell
# Create branch with AI-suggested name
xkit git-create-branch

# Create branch with custom name
xkit git-create-branch feature/user-authentication

# Create from specific commit
xkit git-create-branch --from abc1234 hotfix/critical-bug
```

## 🤖 AI Commands

### `ai-analyze [target]`

AI-powered analysis and assistance.

```powershell
# Analyze current directory/project
xkit ai-analyze

# Analyze specific file
xkit ai-analyze src/main.py

# Analyze git repository
xkit ai-analyze --git

# Analyze with specific focus
xkit ai-analyze --focus security,performance
```

**Output Example:**
```
🤖 AI Project Analysis
═══════════════════════

📊 Code Quality: 8.5/10
🔒 Security: 9/10  
⚡ Performance: 7/10

💡 Key Findings:
  • ✅ Well-structured Python codebase
  • ⚠️  Missing error handling in api.py:45
  • 🚀 Consider adding async operations for better performance
  • 🔒 API keys should be moved to environment variables

🎯 Recommended Actions:
  1. Add try-catch blocks to API functions
  2. Implement async/await for database operations
  3. Move secrets to .env file
  4. Add comprehensive logging
```

### `ai-explain-code [file]`

Get AI explanations for code functionality.

```powershell
# Explain current file
xkit ai-explain-code

# Explain specific file
xkit ai-explain-code src/complex_algorithm.py

# Explain code snippet from clipboard
xkit ai-explain-code --clipboard

# Explain with technical level
xkit ai-explain-code --level beginner
```

### `xpilot-analyze [error]`

XPilot AI agent for error analysis and suggestions.

```powershell
# Analyze last error automatically
xkit xpilot-analyze

# Analyze specific error message
xkit xpilot-analyze "ModuleNotFoundError: No module named 'requests'"

# Analyze with context
xkit xpilot-analyze --context git,python,web-development

# Get step-by-step fix
xkit xpilot-analyze --fix-steps
```

**Output Example:**
```
🤖 @xpilot Error Analysis
═════════════════════════

❌ Error: ModuleNotFoundError: No module named 'requests'

🔍 Analysis:
The error indicates that the 'requests' library is not installed 
in your current Python environment. This is a common dependency 
management issue.

💡 Suggested Solutions:
  1. Install requests: pip install requests
  2. Check virtual environment: pip list | grep requests  
  3. Add to requirements.txt for future deployments

🚀 Quick Fix:
Run: pip install requests && python your_script.py

🎓 Prevention:
Consider using requirements.txt or pyproject.toml for dependency management.
```

## 🎨 Legacy Shortcuts

Quick command shortcuts for common operations (oh-my-xkit style).

### Git Shortcuts

```powershell
gs              # git status
ga <files>      # git add <files>
gaa             # git add --all
gc <args>       # git commit <args>
gcm "message"   # git commit -m "message"
gp              # git push
gl              # git pull
gco <branch>    # git checkout <branch>
gb              # git branch
gd              # git diff
glog            # git log --oneline --graph --decorate
```

### Docker Shortcuts

```powershell
d <args>        # docker <args>
dc <args>       # docker-compose <args>
dps             # docker ps
di              # docker images
```

### Navigation Shortcuts

```powershell
..              # cd ..
...             # cd ../..
....            # cd ../../..
```

### File Operation Shortcuts

```powershell
ll              # Get-ChildItem -Force (detailed listing)
la              # Get-ChildItem -Force -Hidden (include hidden)
```

### PowerShell Profile Shortcuts

```powershell
reload-profile  # Reload PowerShell profile
edit-profile    # Edit profile in VS Code
```

## 🔧 Advanced Usage

### Command Chaining

```powershell
# Chain multiple XKit commands
xkit git-status && xkit ai-analyze --git

# Use with PowerShell pipeline  
xkit plugin-list | Select-String "Active"
```

### Configuration

```powershell
# Set configuration values
xkit config-set ai.enabled true
xkit config-set display.theme dark
xkit config-set git.auto_push false

# Get configuration values
xkit config-get ai.provider
xkit config-get display.theme
```

### Scripting Integration

```powershell
# Use in PowerShell scripts
$status = xkit git-status --json | ConvertFrom-Json
if ($status.dirty) {
    Write-Warning "Repository has uncommitted changes"
}

# Capture command output
$analysis = xkit ai-analyze --format json
$recommendations = ($analysis | ConvertFrom-Json).recommendations
```

### Environment Variables

Configure XKit behavior through environment variables:

```powershell
# Enable debug mode
$env:XKIT_DEBUG = "true"

# Set AI provider
$env:XKIT_AI_PROVIDER = "gemini"

# Configure MCP servers
$env:XKIT_MCP_CONFIG = "custom-mcp-config.json"

# Set plugin directories
$env:XKIT_PLUGIN_DIRS = "plugins;custom-plugins"
```

## 🆘 Troubleshooting Commands

### System Diagnosis

```powershell
# Check system requirements
xkit doctor

# Test all components
xkit test-system

# Verify installation
xkit verify-install

# Show detailed logs
xkit logs --tail 50
```

### Performance Monitoring

```powershell
# Show performance metrics
xkit metrics

# Monitor real-time performance
xkit monitor --realtime

# Performance profiling
xkit profile-command git-status
```

### Recovery Commands

```powershell
# Reset to defaults
xkit reset-config

# Clear cache
xkit clear-cache

# Restart services
xkit restart-services

# Emergency mode (minimal functionality)
xkit emergency-mode
```

## 🔗 Related Documentation

- **[Core API](core-api.md)** - Python API reference
- **[Plugin API](plugin-api.md)** - Plugin development guide  
- **[MCP Protocol](mcp-protocol.md)** - MCP integration details
- **[Event API](event-api.md)** - Event system reference

---

**Last Updated**: September 2025 | **Version**: v3.0.0  
**💙 Made with love by the XKit Community**