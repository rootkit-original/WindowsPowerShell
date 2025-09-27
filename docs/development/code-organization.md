# 🏗️ Code Organization Standards

> **Comprehensive guidelines for organizing XKit v3.0 project structure and code**

## 🎯 **Overview**

This document establishes the organizational standards for the XKit v3.0 codebase, ensuring consistent structure, maintainable code, and clear separation of concerns following hexagonal architecture principles.

## 📁 **Project Structure Standards**

### **Root Directory Organization**
```
WindowsPowerShell/                    ← Repository root
├── docs/                            ← Documentation (organized by purpose)
│   ├── README.md                    ← Documentation index
│   ├── api/                         ← API reference documentation
│   ├── architecture/                ← Architecture and design docs
│   ├── development/                 ← Development guides and standards
│   └── deployment/                  ← Deployment and operations guides
├── Scripts/                         ← Core XKit implementation
│   ├── xkit_main.py                ← Main entry point
│   └── xkit/                        ← Core XKit modules
├── tests/                           ← All test files
├── templates/                       ← Boilerplate templates
├── *.md                            ← Project-level documentation
└── *.ps1                           ← PowerShell integration scripts
```

### **Core Module Organization (`Scripts/xkit/`)**
```
Scripts/xkit/                        ← Core XKit framework
├── __init__.py                      ← Package initialization
├── core/                           ← Domain layer (business logic)
│   ├── domain/                     ← Core business entities
│   ├── application/                ← Use cases and app services  
│   └── ports/                      ← Interface definitions
├── adapters/                       ← Infrastructure adapters
│   ├── cli/                        ← CLI interface adapter
│   ├── external/                   ← External API adapters
│   └── persistence/                ← Data persistence adapters
├── infrastructure/                 ← Infrastructure services
│   ├── config.py                   ← Configuration management
│   ├── logging.py                  ← Logging infrastructure
│   └── services/                   ← Infrastructure services
├── plugins/                        ← Plugin system
│   ├── base.py                     ← Plugin interfaces
│   ├── manager.py                  ← Plugin management
│   ├── loader.py                   ← Dynamic plugin loading
│   ├── core/                       ← Essential system plugins
│   └── integrations/               ← Third-party integrations
├── mcp/                           ← MCP (Model Context Protocol)
│   ├── client.py                   ← MCP client implementation
│   ├── servers/                    ← Built-in MCP servers
│   └── config.json                 ← MCP server configuration
└── events/                         ← Event system
    ├── bus.py                      ← Event bus implementation
    ├── events.py                   ← Event definitions
    └── handlers/                   ← Event handlers
```

## 🏛️ **Architecture Layer Standards**

### **Domain Layer (`core/domain/`)**
```python
# Entities: Core business objects
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Project:
    """Core project entity"""
    path: str
    name: str
    type: ProjectType
    files: List[ProjectFile]
    
    def calculate_score(self) -> float:
        """Business logic belongs in entities"""
        return self._scoring_algorithm()
```

### **Application Layer (`core/application/`)**
```python
# Use Cases: Application business rules
from abc import ABC, abstractmethod

class AnalyzeProjectUseCase:
    """Use case: Analyze a project"""
    
    def __init__(self, project_repo: IProjectRepository):
        self.project_repo = project_repo
    
    async def execute(self, project_path: str) -> ProjectAnalysisResult:
        """Execute the use case"""
        project = await self.project_repo.load_project(project_path)
        return project.analyze()
```

### **Ports (`core/ports/`)**
```python
# Interfaces: Abstract contracts
from abc import ABC, abstractmethod

class IProjectRepository(ABC):
    """Port: Project data access interface"""
    
    @abstractmethod
    async def load_project(self, path: str) -> Project:
        """Load project from path"""
        pass
```

### **Adapters (`adapters/`)**
```python
# Adapters: Implement ports
from core.ports.project_port import IProjectRepository

class FileSystemProjectAdapter(IProjectRepository):
    """Adapter: File system project access"""
    
    async def load_project(self, path: str) -> Project:
        """Implementation of the port"""
        # File system specific logic
        pass
```

## 📦 **Module Standards**

### **Import Organization**
Follow this order for imports:

```python
# 1. Standard library
import os
import json
from pathlib import Path
from typing import Dict, List, Optional

# 2. Third-party packages
import aiofiles
from pydantic import BaseModel

# 3. XKit framework (absolute imports)
from xkit.core.domain.entities import Project
from xkit.core.ports.project_port import IProjectRepository
from xkit.events.bus import EventBus

# 4. Local module (relative imports within same package only)
from .helpers import utility_function
```

### **File Naming Conventions**

| File Type | Convention | Examples |
|-----------|------------|----------|
| **Modules** | `snake_case.py` | `project_analyzer.py`, `config_service.py` |
| **Classes** | `PascalCase` | `ProjectAnalyzer`, `ConfigService` |
| **Functions** | `snake_case` | `analyze_project()`, `load_config()` |
| **Constants** | `UPPER_SNAKE_CASE` | `DEFAULT_TIMEOUT`, `MAX_RETRIES` |
| **Private** | `_leading_underscore` | `_internal_method()`, `_private_var` |

## 🔧 **Code Standards**

### **Class Organization**
```python
class XKitService:
    """
    Service description
    
    Attributes:
        public_attr: Description
    """
    
    # 1. Class variables (constants)
    DEFAULT_TIMEOUT = 30
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize service"""
        # 2. Instance attributes
        self.config = config
        self._logger = logging.getLogger(__name__)
        self._internal_state = None
    
    # 3. Properties
    @property
    def status(self) -> str:
        """Service status"""
        return self._status
    
    # 4. Public methods (alphabetically)
    async def analyze(self, target: str) -> AnalysisResult:
        """Public method"""
        pass
    
    def configure(self, settings: Dict[str, Any]) -> None:
        """Public method"""
        pass
    
    # 5. Private methods (alphabetically)
    def _calculate_score(self, data: Any) -> float:
        """Private helper method"""
        pass
    
    def _validate_input(self, input_data: Any) -> bool:
        """Private validation method"""
        pass
```

### **Function Standards**
```python
async def analyze_project(
    project_path: str,
    options: Optional[AnalysisOptions] = None
) -> AnalysisResult:
    """
    Analyze a project and return results
    
    Args:
        project_path: Absolute path to project directory
        options: Analysis configuration options
        
    Returns:
        AnalysisResult: Comprehensive analysis results
        
    Raises:
        ProjectNotFoundError: If project path doesn't exist
        AnalysisError: If analysis fails
    """
    # Implementation
    pass
```

## 🗂️ **Documentation Organization**

### **Documentation Structure**
```
docs/
├── README.md                        ← Navigation hub
├── api/                            ← API references
│   ├── core-api.md                 ← Core Python API
│   ├── plugin-api.md               ← Plugin development API
│   ├── mcp-protocol.md             ← MCP protocol reference
│   └── cli-commands.md             ← Command-line interface
├── architecture/                   ← Design documentation
│   ├── README.md                   ← Architecture overview
│   ├── plugin-system.md            ← Plugin architecture
│   ├── event-system.md             ← Event-driven design
│   └── hexagonal.md                ← Hexagonal architecture
├── development/                    ← Developer guides
│   ├── contributing.md             ← How to contribute
│   ├── plugin-development.md       ← Plugin development guide
│   ├── plugin-standards.md         ← Plugin coding standards
│   ├── code-organization.md        ← This document
│   └── testing.md                  ← Testing guidelines
└── deployment/                     ← Operations documentation
    ├── installation.md             ← Installation guide
    ├── configuration.md            ← Configuration reference
    └── troubleshooting.md          ← Common issues
```

### **Documentation Standards**
- **Naming**: Use kebab-case for file names (`plugin-development.md`)
- **Headers**: Use hierarchical emoji headers for visual organization
- **Links**: Use relative links within docs (`[link](../api/core-api.md)`)
- **Code Examples**: Include working, tested code examples
- **Tables**: Use tables for reference information
- **Emojis**: Consistent emoji usage for visual structure

## 🧪 **Test Organization**

### **Test Structure**
```
tests/
├── unit/                           ← Unit tests
│   ├── core/                       ← Core logic tests
│   ├── plugins/                    ← Plugin tests
│   └── mcp/                        ← MCP system tests
├── integration/                    ← Integration tests
│   ├── plugin_manager_test.py      ← Plugin system integration
│   └── mcp_integration_test.py     ← MCP integration
├── fixtures/                       ← Test data and fixtures
│   ├── sample_projects/            ← Sample project structures
│   └── config_fixtures.json       ← Configuration test data
└── conftest.py                     ← Pytest configuration
```

### **Test Naming**
```python
# Test file: test_{module_name}.py
# Test class: Test{ClassName}
# Test method: test_{method_name}_{scenario}

class TestProjectAnalyzer:
    """Test project analyzer functionality"""
    
    async def test_analyze_project_success(self):
        """Test successful project analysis"""
        pass
    
    async def test_analyze_project_invalid_path_raises_error(self):
        """Test error handling for invalid paths"""
        pass
```

## 🔄 **Configuration Organization**

### **Configuration Structure**
```
config/                             ← Configuration files (gitignored)
├── xkit.json                       ← Main XKit configuration
├── plugins/                        ← Plugin configurations
│   ├── telegram.json              ← Plugin-specific config
│   └── project_analyzer.json      ← Plugin-specific config
└── mcp/                           ← MCP server configurations
    └── servers.json               ← MCP server definitions

.env                               ← Environment variables (gitignored)
.env.example                       ← Environment template (committed)
```

### **Configuration Standards**
```python
# Configuration access pattern
from xkit.infrastructure.config import XKitConfigService

class MyService:
    def __init__(self, config_service: XKitConfigService):
        self.config = config_service
    
    async def initialize(self):
        """Load configuration"""
        # Get main config
        main_config = await self.config.get_main_config()
        
        # Get plugin-specific config
        plugin_config = await self.config.get_plugin_config("my-plugin")
        
        # Get environment variables
        api_key = self.config.get_env("MY_API_KEY")
```

## 📊 **Quality Organization**

### **Quality Tools Configuration**
```
pyproject.toml                      ← Python project configuration
├── [tool.black]                    ← Code formatting
├── [tool.isort]                    ← Import sorting  
├── [tool.pytest]                   ← Test configuration
└── [tool.mypy]                     ← Type checking

.flake8                            ← Linting configuration
.gitignore                         ← Version control ignores
.pre-commit-config.yaml            ← Pre-commit hooks (future)
```

### **Code Quality Standards**
- **Type Hints**: All public APIs must have type hints
- **Docstrings**: All modules, classes, and public functions
- **Error Handling**: Explicit exception handling with logging
- **Logging**: Structured logging with appropriate levels
- **Testing**: Minimum 80% code coverage for critical paths

## 🚀 **Deployment Organization**

### **Deployment Structure**
```
Scripts/                           ← Deployment scripts
├── install-xkit-v3.ps1           ← Main installation script
├── setup/                         ← Setup utilities
└── maintenance/                   ← Maintenance scripts

oh-my-xkit/                        ← Optional framework extensions
├── plugins/                       ← Community plugins
└── themes/                        ← UI themes
```

## 🔗 **Integration Standards**

### **External Integrations**
```python
# Pattern for external service integration
from adapters.external.base import ExternalServiceAdapter

class GitHubAdapter(ExternalServiceAdapter):
    """GitHub API integration"""
    
    def __init__(self, api_key: str):
        super().__init__("GitHub", "https://api.github.com")
        self.api_key = api_key
    
    async def get_repository_info(self, repo: str) -> Dict[str, Any]:
        """Get repository information"""
        return await self._make_request(f"/repos/{repo}")
```

### **Plugin Integrations**
```python
# Pattern for plugin-to-plugin communication
class MyPlugin(XKitCorePlugin):
    async def _initialize_services(self):
        """Initialize with other plugins"""
        # Get services from other plugins
        github_service = self.get_service("github_integration")
        telegram_service = self.get_service("telegram_service")
        
        # Register cross-plugin dependencies
        if github_service and telegram_service:
            self.cross_plugin_integration = CrossPluginService(
                github_service, telegram_service
            )
```

## 📈 **Metrics and Monitoring**

### **Performance Monitoring**
```python
# Pattern for performance tracking
import time
from functools import wraps

def track_performance(func):
    """Decorator for performance tracking"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info(f"{func.__name__} completed in {duration:.2f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"{func.__name__} failed after {duration:.2f}s: {e}")
            raise
    return wrapper
```

## 🔗 **Related Standards**

- **[Plugin Development Standards](./plugin-standards.md)** - Plugin-specific guidelines
- **[API Documentation](../api/)** - API reference standards
- **[Architecture Documentation](../architecture/)** - System design principles
- **[Testing Guidelines](./testing.md)** - Testing strategies and patterns

---

**Document Version**: v1.0  
**Last Updated**: September 27, 2025  
**Maintained by**: @rootkit-original

> 💡 **These standards evolve with the project** - Contribute improvements through PRs!