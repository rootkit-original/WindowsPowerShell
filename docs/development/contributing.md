# 🤝 Contributing to XKit v3.0

> **Complete guide for contributing to XKit development**

Welcome to the XKit contributor community! This guide will help you get started with contributing to XKit v3.0's hybrid MCP architecture.

## 🎯 Quick Start

### For New Contributors

1. **🍴 Fork & Clone**: Fork the repository and clone your fork locally
2. **🛠️ Setup**: Follow the [development setup](#development-setup) guide
3. **🐛 Find Issue**: Look for issues labeled `good first issue` or `help wanted`
4. **💬 Discuss**: Comment on the issue to discuss your approach
5. **🔨 Develop**: Create a feature branch and implement your changes
6. **✅ Test**: Run tests and ensure quality gates pass
7. **📝 Document**: Update documentation for your changes
8. **🚀 Submit**: Create a pull request with detailed description

### For Experienced Contributors

1. **🏗️ Architecture**: Understand the [hybrid MCP architecture](../ARCHITECTURE.md)
2. **🎯 Roadmap**: Check the [project roadmap](../ROADMAP.md) for priorities
3. **💡 RFC Process**: For significant changes, start with an RFC discussion
4. **🤖 AI Integration**: Consider how changes fit with AI-powered features
5. **🔌 Extensibility**: Ensure changes support plugin and MCP extensibility

## 📋 Development Setup

### Prerequisites

```powershell
# Required versions
PowerShell 5.1+           # Windows PowerShell or PowerShell Core
Python 3.11+              # Main development language
Git 2.30+                 # Version control
VS Code (recommended)     # IDE with XKit extensions
```

### Environment Setup

```bash
# 1. Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/WindowsPowerShell.git
cd WindowsPowerShell

# 2. Create development environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install development dependencies
pip install -r requirements-dev.txt
pip install -e .  # Install XKit in editable mode

# 4. Install pre-commit hooks
pre-commit install

# 5. Verify setup
python Scripts/xkit_main.py status
python Scripts/xkit_main.py version
```

### IDE Configuration

#### VS Code Setup

Install recommended extensions:
- Python (Microsoft)
- PowerShell (Microsoft)  
- GitLens (GitKraken)
- Better Comments (Aaron Bond)
- Error Lens (Alexander)

**VS Code Settings** (`.vscode/settings.json`):
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["--line-length=88"],
    "python.sortImports.args": ["--profile", "black"],
    "powershell.codeFormatting.preset": "OTBS",
    "files.associations": {
        "*.ps1": "powershell",
        "*.psm1": "powershell",
        "*.psd1": "powershell"
    }
}
```

## 🏗️ Architecture Guidelines

### Hybrid MCP Architecture Principles

#### 1. **Python-First Development**
- Business logic in Python (Scripts/xkit/)
- PowerShell as minimal wrapper only
- Rich features through Python ecosystem

#### 2. **MCP Integration**
- Extend functionality via MCP servers
- Internal servers for core features
- External servers for third-party integration

#### 3. **Plugin System**
- Hot-reloadable modular components
- Event-driven communication
- Clean separation of concerns

#### 4. **Event-Driven Design**
- Central event bus for loose coupling
- Async event processing
- Reactive patterns for responsiveness

### Code Organization

```
Scripts/xkit/
├── core/                 # 💎 Core Domain Layer
│   ├── application.py   # Main application orchestrator
│   ├── container.py     # Dependency injection
│   └── ports/           # Interface definitions
├── domain/              # 🎯 Business Domain
│   ├── entities/        # Domain entities
│   └── models/          # Value objects
├── adapters/            # 🔌 External Adapters
│   ├── cli/            # Command-line interface
│   └── external/       # External service adapters
├── mcp/                 # 🔗 MCP Integration
│   ├── client.py       # MCP client
│   ├── servers/        # Internal MCP servers
│   └── protocol.py     # Protocol implementation
├── plugins/             # 🧩 Plugin System
│   ├── manager.py      # Plugin management
│   └── base.py         # Plugin interfaces
├── events/              # 📡 Event System
│   ├── bus.py          # Central event bus
│   └── events.py       # Event definitions
└── infrastructure/     # 🔧 Infrastructure
    ├── git.py          # Git operations
    ├── ai_service.py   # AI integration
    └── display.py      # UI services
```

## 📝 Contribution Types

### 🐛 Bug Fixes

**Process:**
1. Create issue using [bug report template](../.github/ISSUE_TEMPLATE/bug_report.yml)
2. Create branch: `fix/issue-description`
3. Write failing test that reproduces the bug
4. Fix the bug with minimal changes
5. Ensure all tests pass
6. Update documentation if needed

**Example Bug Fix:**
```python
# Before: Bug in git status parsing
def parse_git_status(output: str) -> GitStatus:
    lines = output.split('\n')  # Bug: doesn't handle empty output
    return GitStatus(files=lines)

# After: Fixed with proper error handling
def parse_git_status(output: str) -> GitStatus:
    if not output.strip():
        return GitStatus(files=[])
    
    lines = [line for line in output.split('\n') if line.strip()]
    return GitStatus(files=lines)
```

### ✨ Feature Development

**Process:**
1. Create issue using [feature request template](../.github/ISSUE_TEMPLATE/feature_request.yml)
2. Discuss design in issue comments or RFC
3. Create branch: `feature/feature-name`
4. Implement following architecture principles
5. Add comprehensive tests
6. Update API documentation
7. Add usage examples

**Feature Development Checklist:**
- [ ] Feature follows hybrid architecture principles
- [ ] Integrates with MCP/Plugin/Event systems appropriately
- [ ] Has comprehensive test coverage (>80%)
- [ ] Includes API documentation
- [ ] Provides usage examples
- [ ] Considers backward compatibility
- [ ] Handles errors gracefully

### 🧩 Plugin Development

**Process:**
1. Use [plugin development template](../.github/ISSUE_TEMPLATE/plugin_development.yml)
2. Follow [Plugin Development Guide](plugin-development.md)
3. Create plugin in `Scripts/xkit/plugins/`
4. Implement XKitPlugin interface
5. Add comprehensive tests
6. Document plugin API and usage

**Plugin Contribution Guidelines:**
```python
class ContributedPlugin(XKitPlugin):
    """
    Well-documented plugin following XKit standards
    
    This plugin provides [clear description of functionality]
    """
    
    def __init__(self):
        metadata = PluginMetadata(
            name="contributed-plugin",
            version="1.0.0",
            description="Clear, concise description",
            author="Your Name <email@example.com>",
            dependencies=["minimal-deps>=1.0.0"],  # Keep minimal
            provides=["clear-command-names"],
            requires=["essential-services-only"],
            hot_reload=True,
            priority=100  # Default priority
        )
        super().__init__(metadata)
    
    async def load(self) -> None:
        """Load with clear documentation of side effects"""
        # Implement loading logic
        pass
    
    # Clear, well-tested command implementations
    async def example_command(self, args: List[str]) -> str:
        """
        Example command with clear docstring
        
        Args:
            args: Command arguments
            
        Returns:
            Human-readable result string
        """
        # Implementation with error handling
        pass
```

### 🔌 MCP Server Development

**Process:**
1. Use [MCP server template](../.github/ISSUE_TEMPLATE/mcp_server_development.yml)
2. Follow [MCP Server Development Guide](mcp-server-development.md)
3. Implement MCPServer interface
4. Ensure protocol compliance
5. Add security considerations
6. Test with XKit integration

### 📚 Documentation

**Types of Documentation:**
- **API Reference**: Technical API documentation
- **Guides**: Step-by-step tutorials and guides
- **Examples**: Practical usage examples
- **Architecture**: Design and architecture explanations

**Documentation Standards:**
- Use clear, concise language
- Include practical examples
- Keep up-to-date with code changes
- Add diagrams for complex concepts
- Follow existing documentation style

## 🧪 Testing Guidelines

### Test Structure

```
tests/
├── unit/                # Fast unit tests
│   ├── test_core.py
│   ├── test_plugins.py
│   └── test_mcp.py
├── integration/         # Integration tests
│   ├── test_workflows.py
│   └── test_external_apis.py
├── performance/         # Performance tests
│   └── test_benchmarks.py
├── fixtures/           # Test data and fixtures
│   ├── sample_repos/
│   └── mock_responses/
└── conftest.py         # Shared test configuration
```

### Testing Requirements

**Unit Tests:**
- Test individual functions and classes
- Mock external dependencies
- Fast execution (< 1s per test)
- High coverage (>90% for new code)

**Integration Tests:**
- Test component interactions
- Use real services when possible
- Test error conditions
- Reasonable execution time (< 30s)

**Performance Tests:**
- Benchmark critical paths
- Prevent performance regressions
- Test under realistic load
- Memory usage validation

### Test Examples

```python
# Unit test example
@pytest.mark.asyncio
async def test_git_status_parsing():
    """Test git status output parsing"""
    mock_output = """
     M modified_file.py
    A  added_file.py
    ?? untracked_file.py
    """
    
    status = parse_git_status(mock_output)
    
    assert len(status.modified_files) == 1
    assert len(status.staged_files) == 1
    assert len(status.untracked_files) == 1
    assert "modified_file.py" in status.modified_files


# Integration test example
@pytest.mark.integration
async def test_mcp_server_integration():
    """Test MCP server integration with XKit"""
    client = XKitMCPClient()
    
    # Test server connection
    connected = await client.connect_server("test-server")
    assert connected
    
    # Test tool listing
    tools = await client.list_tools("test-server")
    assert len(tools) > 0
    
    # Test tool execution
    result = await client.call_tool("test-server", "test-tool", {})
    assert not result.isError
```

### Performance Testing

```python
@pytest.mark.performance
async def test_command_execution_performance():
    """Test command execution performance"""
    start_time = time.time()
    
    # Execute command multiple times
    for _ in range(100):
        result = await execute_command("git-status", [])
        assert result.success
    
    end_time = time.time()
    avg_time = (end_time - start_time) / 100
    
    # Performance assertion (adjust based on requirements)
    assert avg_time < 0.1  # Average under 100ms
```

## 🔍 Code Review Process

### Before Submitting PR

**Self-Review Checklist:**
- [ ] Code follows architecture principles
- [ ] All tests pass locally
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] No debugging code left behind
- [ ] Security considerations addressed
- [ ] Performance impact considered

### PR Requirements

**Pull Request Template:**
```markdown
## 📋 Description
Brief description of changes and motivation.

## 🔄 Type of Change
- [ ] Bug fix (non-breaking change)
- [ ] New feature (non-breaking change)
- [ ] Breaking change (fix/feature causing existing functionality to change)
- [ ] Documentation update

## ✅ Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated  
- [ ] All tests pass
- [ ] Performance tests pass (if applicable)

## 📚 Documentation
- [ ] API documentation updated
- [ ] User guide updated (if applicable)
- [ ] Examples added (if applicable)

## 🔒 Security
- [ ] Security implications considered
- [ ] Input validation added where needed
- [ ] Authentication/authorization handled properly

## 📱 Compatibility
- [ ] Backward compatibility maintained
- [ ] Python 3.11+ compatibility verified
- [ ] PowerShell 5.1+ compatibility verified
- [ ] Cross-platform testing completed

## 🧪 Testing Instructions
Detailed instructions for reviewers to test the changes.
```

### Review Criteria

**Code Quality:**
- Follows Python/PowerShell best practices
- Proper error handling and logging
- Clear variable and function names
- Appropriate abstraction levels

**Architecture Compliance:**
- Follows hybrid MCP architecture
- Proper separation of concerns
- Event-driven patterns where appropriate
- Plugin/MCP extensibility considered

**Testing:**
- Adequate test coverage
- Tests are clear and maintainable
- Edge cases covered
- Performance implications tested

**Documentation:**
- API changes documented
- User-facing changes explained
- Examples provided for new features
- Architecture decisions explained

## 🚀 Release Process

### Version Management

**Semantic Versioning:**
- `v3.x.y` - Major.Minor.Patch
- Major: Breaking changes
- Minor: New features (backward compatible)
- Patch: Bug fixes (backward compatible)

**Branch Strategy:**
- `main`: Stable production releases
- `develop`: Development branch
- `feature/*`: Feature development
- `fix/*`: Bug fixes
- `release/*`: Release preparation

### Release Workflow

1. **Development**: Work on `develop` branch
2. **Feature Freeze**: Create `release/v3.x.y` branch
3. **Testing**: Comprehensive testing of release branch
4. **Documentation**: Update release notes and documentation
5. **Merge**: Merge to `main` and tag release
6. **Deployment**: Automated deployment via GitHub Actions

## 🤝 Community Guidelines

### Communication

**GitHub Discussions**: General questions and discussions
**Issues**: Bug reports and feature requests
**Pull Requests**: Code contributions and reviews
**Discord/Chat**: Real-time community interaction

### Code of Conduct

- **Be respectful**: Treat all community members with respect
- **Be constructive**: Provide helpful feedback and suggestions
- **Be collaborative**: Work together to improve XKit
- **Be inclusive**: Welcome contributors of all backgrounds and skill levels

### Recognition

**Contributors are recognized through:**
- GitHub contributor graphs
- Release notes acknowledgments
- Community spotlight features
- Maintainer promotion opportunities

## 🎖️ Contributor Levels

### 🌱 New Contributor
- First-time contributors
- Focus on documentation, small bugs
- Mentorship and guidance provided

### 🌿 Regular Contributor
- Multiple contributions accepted
- Familiar with codebase and processes
- Can review smaller pull requests

### 🌳 Core Contributor
- Significant contributions to project
- Deep understanding of architecture
- Can mentor new contributors
- Reviews major pull requests

### 🏛️ Maintainer
- Long-term commitment to project
- Full repository access
- Release management responsibilities
- Community leadership role

## 📚 Resources

### Development Resources
- **[Architecture Guide](../ARCHITECTURE.md)** - Understand system design
- **[API Documentation](../docs/api/)** - Complete API reference
- **[Plugin Development](plugin-development.md)** - Create plugins
- **[MCP Server Guide](mcp-server-development.md)** - Develop MCP servers

### Learning Resources
- **[Python Best Practices](https://docs.python-guide.org/)**
- **[PowerShell Documentation](https://docs.microsoft.com/powershell/)**
- **[MCP Protocol Spec](https://modelcontextprotocol.io/)**
- **[Async Programming](https://docs.python.org/3/library/asyncio.html)**

### Tools and Utilities
- **Pre-commit Hooks**: Automated code quality checks
- **GitHub Actions**: CI/CD automation
- **Testing Framework**: pytest with async support
- **Documentation**: MkDocs with Material theme

---

## 🎉 Thank You!

Thank you for contributing to XKit! Your contributions help make PowerShell development more productive and enjoyable for developers worldwide.

**Questions?** Join our community discussions or reach out to maintainers.

**Made with 💙 by the XKit Community**