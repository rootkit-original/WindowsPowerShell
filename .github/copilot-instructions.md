# GitHub Copilot Instructions for XKit Project

## Project Overview
XKit is an enhanced PowerShell framework with Clean Architecture that provides:
- 🎨 Oh-my-zsh inspired experience for Windows PowerShell
- 🤖 AI-powered error handling with local @xpilot agent
- 🏗️ Clean Architecture pattern (Domain/Application/Infrastructure)
- 🔧 Git workflow automation with intelligent branching
- 📱 Telegram notifications and AI assistant integration
- 🐳 Container management (Docker/Podman) support

## Architecture Philosophy
- **Python-First**: PowerShell is minimal wrapper, Python handles all logic
- **Clean Architecture**: Dependency injection, interfaces, separation of concerns
- **Error-Driven Development**: Sophisticated error handling with Git integration
- **Configuration-Based**: Absolute paths, robust configuration system
- **Emoji-Rich UX**: Python handles Unicode properly, PowerShell stays ASCII

## Key Components

### Core Structure
```
WindowsPowerShell/
├── .github/copilot-instructions.md     # This file
├── xkit-config.ps1                     # Minimal PS config with absolute paths
├── Microsoft.PowerShell_profile.ps1    # Ultra-minimal PS profile
├── Scripts/
│   ├── xkit_main.py                   # Python entry point
│   └── xkit/                          # Clean Architecture modules
│       ├── domain/                    # Business entities & interfaces
│       ├── application/               # Use cases & orchestration
│       └── infrastructure/            # External services & implementations
└── oh-my-xkit/
    ├── oh-my-xkit.ps1                # Minimal PS framework loader
    └── plugins/                       # Thin PS wrappers calling Python
```

### Error Handling System (@xpilot)
When errors occur:
1. **Detection**: PowerShell wrappers catch errors and call Python
2. **Analysis**: Python AI agent analyzes error patterns
3. **Git Integration**: Creates error branch automatically
4. **Resolution**: Provides suggestions, auto-fixes when possible
5. **Workflow**: User can accept fixes, create tasks, or continue

## Development Guidelines

### When Working on XKit:
1. **Minimize PowerShell**: Only use PS for absolute necessities
2. **Python-Heavy**: All logic, UI, error handling in Python
3. **Clean Architecture**: Follow domain/application/infrastructure pattern
4. **Absolute Paths**: Always use configuration-based paths
5. **Error-First**: Every command should have error handling
6. **Rich UX**: Use emojis and colors in Python, plain text in PS

### Common Tasks:

#### Adding New Commands
- Create Python use case in `application/use_cases.py`
- Add minimal PS wrapper that calls `Invoke-XKitPython`
- Register in `xkit_main.py` action dispatcher

#### Extending Error Handling
- Add new error patterns in `infrastructure/error_handler.py`
- Extend XPilot analysis in `XPilotAgent` class
- Update display service for rich error presentation

#### Plugin Development
- Create Python infrastructure service
- Add thin PS plugin that delegates to Python
- Register in configuration system

### Code Patterns

#### PowerShell Pattern (MINIMAL):
```powershell
function global:new-command {
    param([Parameter(ValueFromRemainingArguments)]$args)
    Invoke-XKitPython "action-name" @args
}
```

#### Python Pattern (RICH):
```python
class NewFeatureUseCase:
    def __init__(self, dependencies...):
        # Dependency injection
    
    def execute(self, params):
        # Business logic with error handling
        try:
            result = self._do_work(params)
            return result
        except Exception as e:
            self.error_handler.handle_error(str(e), "context")
```

## Current Status
- ✅ Clean Architecture foundation implemented
- ✅ Error handling system with @xpilot agent
- ✅ Python-backed command system
- ✅ Configuration-based path management
- ✅ Rich emoji UX in Python
- 🔄 Testing integrated system
- 📋 Need to minimize PowerShell further

## Priority Tasks
1. **Simplify PowerShell**: Remove all logic, make pure wrappers
2. **Robust Configuration**: Bulletproof path resolution
3. **Error Integration**: Test @xpilot workflow end-to-end
4. **Performance**: Optimize Python startup times
5. **Documentation**: Complete user and developer docs

## Working Principles
- **Fail Fast**: Better to show clear errors than silent failures
- **User-Centric**: Rich feedback, helpful suggestions
- **Developer-Friendly**: Clean code, good separation of concerns
- **Maintainable**: Configuration-driven, testable architecture
- **Extensible**: Easy to add new features and integrations

## AI Assistant Integration
- **Gemini API**: For intelligent project analysis and suggestions  
- **Telegram Bot**: For notifications and remote interactions
- **Error Analysis**: Pattern matching and resolution suggestions
- **Context Awareness**: Understands Git, Docker, project structure

## When You Encounter Issues
1. Check `xkit-config.ps1` for path configuration
2. Verify Python dependencies and imports
3. Test Python components independently first
4. Use error handling system to debug PS integration
5. Prioritize moving logic from PS to Python

Remember: PowerShell is just the entry point. Python is the brain. 🧠