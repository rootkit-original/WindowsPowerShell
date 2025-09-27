# 🧪 Testing Guide

> **Comprehensive testing strategies for XKit v3.0**

This guide covers testing methodologies, tools, and best practices for the XKit hybrid MCP architecture.

## 🎯 Testing Philosophy

### Test Pyramid

```
    /\     E2E Tests (Few)
   /  \    - Full system integration
  /____\   - User workflow validation
 /      \  
/________\  Integration Tests (Some)
|        |  - Component interaction
|        |  - Service integration
|________|  
|        |  Unit Tests (Many)
|        |  - Fast, isolated tests
|        |  - High coverage
|________|
```

### Testing Principles

- **Fast Feedback**: Unit tests should run quickly
- **Reliable**: Tests should be deterministic and stable
- **Maintainable**: Tests should be easy to understand and modify
- **Comprehensive**: Cover happy paths, edge cases, and error conditions
- **Isolated**: Tests should not depend on external systems when possible

## 🛠️ Testing Setup

### Dependencies

```bash
# Install testing dependencies
pip install pytest pytest-asyncio pytest-mock pytest-cov
pip install pytest-xdist pytest-html pytest-benchmark
pip install factory-boy faker responses

# Install development tools
pip install coverage pre-commit black isort mypy
```

### Configuration

**pytest.ini:**
```ini
[tool:pytest]
minversion = 6.0
addopts = 
    -ra -q
    --strict-markers
    --strict-config
    --cov=Scripts/xkit
    --cov-report=html:htmlcov
    --cov-report=term-missing
    --cov-report=xml
    --cov-fail-under=80
testpaths = tests
markers =
    unit: Unit tests (fast, isolated)
    integration: Integration tests (slower, real services)
    performance: Performance and benchmark tests
    slow: Tests that take a long time to run
    external: Tests requiring external services
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
```

## 🔬 Unit Testing

### Test Structure

```python
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from typing import Dict, Any

# Import modules under test
from xkit.core.application import XKitApplication
from xkit.plugins.base import XKitPlugin
from xkit.events.bus import EventBus


class TestXKitCore:
    """Test suite for XKit core functionality"""
    
    @pytest.fixture
    def mock_container(self):
        """Mock dependency container"""
        container = Mock()
        container.get_service.return_value = Mock()
        return container
    
    @pytest.fixture
    def app_instance(self, mock_container):
        """XKit application instance with mocked dependencies"""
        app = XKitApplication()
        app.container = mock_container
        return app
    
    @pytest.mark.asyncio
    async def test_application_initialization(self, app_instance):
        """Test XKit application initialization"""
        # Test setup
        assert app_instance is not None
        assert hasattr(app_instance, 'container')
        
        # Test initialization
        await app_instance.initialize()
        
        # Verify initialization steps
        app_instance.container.get_service.assert_called()
    
    @pytest.mark.asyncio
    async def test_command_execution(self, app_instance):
        """Test command execution flow"""
        # Mock command result
        expected_result = "Command executed successfully"
        app_instance.container.get_service.return_value.execute.return_value = expected_result
        
        # Execute command
        result = await app_instance.execute_command("test-command", ["arg1", "arg2"])
        
        # Verify result
        assert result == expected_result
    
    @pytest.mark.parametrize("command,args,expected", [
        ("help", [], "help output"),
        ("version", [], "3.0.0"),
        ("status", [], "system status"),
    ])
    @pytest.mark.asyncio
    async def test_core_commands(self, app_instance, command, args, expected):
        """Test core command implementations"""
        # Mock service response
        app_instance.container.get_service.return_value.execute.return_value = expected
        
        # Execute command
        result = await app_instance.execute_command(command, args)
        
        # Verify result
        assert expected in result
```

### Mocking Strategies

#### Service Mocking

```python
@pytest.fixture
def mock_services():
    """Comprehensive service mocking"""
    services = {
        'git_service': AsyncMock(),
        'ai_service': AsyncMock(),
        'display_service': Mock(),
        'event_bus': AsyncMock(),
        'config_service': Mock(),
        'mcp_client': AsyncMock()
    }
    
    # Configure common behaviors
    services['git_service'].get_status.return_value = Mock(
        branch='main', 
        is_dirty=False,
        staged_files=[],
        modified_files=[]
    )
    
    services['config_service'].get.return_value = {}
    
    return services

@pytest.fixture
def plugin_with_mocks(mock_services):
    """Plugin instance with mocked services"""
    plugin = TestPlugin()
    plugin._services = mock_services
    return plugin
```

#### External API Mocking

```python
import responses

@responses.activate
def test_external_api_integration():
    """Test external API calls with mocking"""
    # Mock external API response
    responses.add(
        responses.GET,
        "https://api.github.com/repos/owner/repo",
        json={"name": "repo", "stars": 100},
        status=200
    )
    
    # Test the function that makes API call
    result = get_repository_info("owner/repo")
    
    # Verify result
    assert result["name"] == "repo"
    assert result["stars"] == 100
```

### Testing Async Code

```python
@pytest.mark.asyncio
async def test_async_operation():
    """Test asynchronous operations"""
    # Create async mock
    async_service = AsyncMock()
    async_service.process_data.return_value = {"processed": True}
    
    # Test async function
    result = await process_with_service(async_service, "test_data")
    
    # Verify async call was made
    async_service.process_data.assert_called_once_with("test_data")
    assert result["processed"] is True

@pytest.mark.asyncio
async def test_concurrent_operations():
    """Test concurrent async operations"""
    import asyncio
    
    # Create multiple async tasks
    tasks = [
        async_operation(f"data_{i}")
        for i in range(10)
    ]
    
    # Run concurrently
    results = await asyncio.gather(*tasks)
    
    # Verify all completed successfully
    assert len(results) == 10
    assert all(result.success for result in results)
```

### Error Handling Tests

```python
def test_error_handling():
    """Test error handling scenarios"""
    
    # Test with various error conditions
    with pytest.raises(ValueError, match="Invalid input"):
        process_invalid_input("invalid_data")
    
    with pytest.raises(FileNotFoundError):
        read_nonexistent_file("/path/to/nowhere")
    
    # Test graceful error handling
    result = safe_operation_with_fallback("risky_input")
    assert result.success is False
    assert "error" in result.message.lower()

@pytest.mark.asyncio
async def test_async_error_handling():
    """Test async error handling"""
    
    # Test async exception handling
    with pytest.raises(ConnectionError):
        await connect_to_unreachable_service()
    
    # Test timeout handling
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(slow_operation(), timeout=0.1)
```

## 🔗 Integration Testing

### Component Integration

```python
@pytest.mark.integration
class TestMCPIntegration:
    """Test MCP client-server integration"""
    
    @pytest.fixture(scope="class")
    async def mcp_server(self):
        """Start test MCP server"""
        server = TestMCPServer()
        await server.start()
        yield server
        await server.stop()
    
    @pytest.fixture
    async def mcp_client(self, mcp_server):
        """MCP client connected to test server"""
        client = XKitMCPClient()
        await client.connect_server("test-server")
        return client
    
    @pytest.mark.asyncio
    async def test_tool_listing(self, mcp_client):
        """Test MCP tool listing"""
        tools = await mcp_client.list_tools("test-server")
        
        assert len(tools) > 0
        assert any(tool.name == "test-tool" for tool in tools)
    
    @pytest.mark.asyncio
    async def test_tool_execution(self, mcp_client):
        """Test MCP tool execution"""
        result = await mcp_client.call_tool(
            "test-server", 
            "test-tool", 
            {"input": "test_data"}
        )
        
        assert not result.isError
        assert "test_data" in result.content[0].text
```

### Database Integration

```python
@pytest.mark.integration
class TestDatabaseIntegration:
    """Test database operations"""
    
    @pytest.fixture(scope="class")
    def test_db(self):
        """Create test database"""
        db_path = ":memory:"  # SQLite in-memory database
        db = create_database(db_path)
        yield db
        db.close()
    
    def test_data_persistence(self, test_db):
        """Test data storage and retrieval"""
        # Insert test data
        test_record = {"id": 1, "name": "test", "value": "data"}
        insert_record(test_db, test_record)
        
        # Retrieve and verify
        retrieved = get_record(test_db, 1)
        assert retrieved["name"] == "test"
        assert retrieved["value"] == "data"
    
    def test_transaction_rollback(self, test_db):
        """Test transaction rollback on error"""
        with pytest.raises(ValueError):
            with transaction(test_db):
                insert_record(test_db, {"id": 2, "name": "test2"})
                raise ValueError("Simulated error")
        
        # Verify rollback occurred
        assert get_record(test_db, 2) is None
```

### File System Integration

```python
@pytest.mark.integration
def test_file_operations(tmp_path):
    """Test file system operations with temporary directory"""
    # Create test files
    test_file = tmp_path / "test.txt"
    test_content = "Test file content"
    test_file.write_text(test_content)
    
    # Test file operations
    result = read_file_content(str(test_file))
    assert result == test_content
    
    # Test directory operations
    result = list_directory_contents(str(tmp_path))
    assert "test.txt" in result
    
    # Test file modification
    new_content = "Modified content"
    write_file_content(str(test_file), new_content)
    
    assert test_file.read_text() == new_content
```

## ⚡ Performance Testing

### Benchmark Tests

```python
import pytest
import time
from pytest_benchmark import benchmark

def test_command_execution_performance(benchmark):
    """Benchmark command execution time"""
    
    def execute_command():
        return process_command("test-command", ["arg1", "arg2"])
    
    # Benchmark the function
    result = benchmark(execute_command)
    
    # Verify functionality
    assert result.success is True

@pytest.mark.performance
def test_concurrent_command_performance():
    """Test performance under concurrent load"""
    import concurrent.futures
    import time
    
    def execute_commands(count):
        """Execute multiple commands concurrently"""
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(process_command, "test-command", [f"arg{i}"])
                for i in range(count)
            ]
            results = [future.result() for future in futures]
        return results
    
    # Measure performance
    start_time = time.time()
    results = execute_commands(100)
    end_time = time.time()
    
    # Verify all commands completed successfully
    assert len(results) == 100
    assert all(result.success for result in results)
    
    # Performance assertion
    execution_time = end_time - start_time
    assert execution_time < 10.0  # Should complete within 10 seconds
    
    throughput = len(results) / execution_time
    assert throughput > 10  # At least 10 commands per second

@pytest.mark.performance
async def test_memory_usage():
    """Test memory usage remains reasonable"""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    # Perform memory-intensive operations
    for i in range(1000):
        await memory_intensive_operation(f"data_{i}")
    
    final_memory = process.memory_info().rss
    memory_increase = final_memory - initial_memory
    
    # Memory increase should be reasonable
    assert memory_increase < 50 * 1024 * 1024  # Less than 50MB increase
```

### Load Testing

```python
@pytest.mark.performance
class TestLoadHandling:
    """Test system behavior under load"""
    
    @pytest.mark.asyncio
    async def test_event_bus_load(self):
        """Test event bus performance under high load"""
        event_bus = EventBus()
        
        # Publish many events concurrently
        async def publish_events(count):
            tasks = [
                event_bus.publish(TestEvent(f"event_{i}"))
                for i in range(count)
            ]
            await asyncio.gather(*tasks)
        
        start_time = time.time()
        await publish_events(10000)
        end_time = time.time()
        
        # Verify performance
        execution_time = end_time - start_time
        events_per_second = 10000 / execution_time
        
        assert events_per_second > 1000  # At least 1000 events/sec
    
    @pytest.mark.asyncio
    async def test_plugin_manager_load(self):
        """Test plugin manager under load"""
        plugin_manager = PluginManager()
        
        # Load many plugins concurrently
        plugins = [create_test_plugin(f"plugin_{i}") for i in range(50)]
        
        start_time = time.time()
        await asyncio.gather(*[
            plugin_manager.load_plugin(plugin)
            for plugin in plugins
        ])
        end_time = time.time()
        
        # Verify all plugins loaded
        assert len(plugin_manager.loaded_plugins) == 50
        
        # Verify reasonable load time
        load_time = end_time - start_time
        assert load_time < 5.0  # Should load within 5 seconds
```

## 🔍 End-to-End Testing

### User Workflow Tests

```python
@pytest.mark.e2e
class TestUserWorkflows:
    """Test complete user workflows"""
    
    @pytest.fixture
    def xkit_session(self):
        """Full XKit session for E2E testing"""
        session = XKitTestSession()
        session.start()
        yield session
        session.stop()
    
    def test_git_workflow(self, xkit_session, tmp_path):
        """Test complete Git workflow"""
        # Setup test repository
        repo_path = tmp_path / "test_repo"
        setup_test_git_repo(repo_path)
        
        # Change to repository directory
        xkit_session.change_directory(str(repo_path))
        
        # Execute Git commands through XKit
        status_result = xkit_session.execute("git-status")
        assert "clean working tree" in status_result.output
        
        # Create and add file
        test_file = repo_path / "new_file.txt"
        test_file.write_text("Test content")
        
        add_result = xkit_session.execute("git", ["add", "new_file.txt"])
        assert add_result.success
        
        # Use AI-powered commit
        commit_result = xkit_session.execute("smart-commit")
        assert commit_result.success
        assert "committed" in commit_result.output.lower()
    
    def test_plugin_development_workflow(self, xkit_session, tmp_path):
        """Test plugin development workflow"""
        # Create plugin directory
        plugin_dir = tmp_path / "my_plugin"
        plugin_dir.mkdir()
        
        # Generate plugin template
        template_result = xkit_session.execute("plugin-template", [str(plugin_dir)])
        assert template_result.success
        
        # Load plugin
        load_result = xkit_session.execute("plugin-load", [str(plugin_dir)])
        assert load_result.success
        
        # Verify plugin is active
        list_result = xkit_session.execute("plugin-list")
        assert "my_plugin" in list_result.output
        
        # Test hot reload
        reload_result = xkit_session.execute("plugin-reload", ["my_plugin"])
        assert reload_result.success
```

### Cross-Platform Testing

```python
@pytest.mark.parametrize("platform", ["windows", "linux", "macos"])
def test_cross_platform_compatibility(platform):
    """Test cross-platform compatibility"""
    if sys.platform.startswith("win") and platform != "windows":
        pytest.skip("Platform-specific test")
    elif sys.platform.startswith("linux") and platform != "linux":
        pytest.skip("Platform-specific test")
    elif sys.platform.startswith("darwin") and platform != "macos":
        pytest.skip("Platform-specific test")
    
    # Test platform-specific functionality
    result = get_platform_specific_info()
    assert result.platform == platform
    assert result.is_supported is True
```

## 🔒 Security Testing

### Input Validation Tests

```python
def test_input_sanitization():
    """Test input sanitization and validation"""
    # Test SQL injection prevention
    malicious_input = "'; DROP TABLE users; --"
    result = safe_database_query(malicious_input)
    assert "error" in result.lower() or result == ""
    
    # Test command injection prevention
    malicious_command = "ls; rm -rf /"
    result = safe_command_execution(malicious_command)
    assert not result.success
    
    # Test path traversal prevention
    malicious_path = "../../../etc/passwd"
    result = safe_file_access(malicious_path)
    assert not result.success

def test_authentication_and_authorization():
    """Test authentication and authorization"""
    # Test unauthenticated access
    with pytest.raises(AuthenticationError):
        access_protected_resource(None)
    
    # Test insufficient permissions
    limited_user = create_test_user(permissions=["read"])
    with pytest.raises(AuthorizationError):
        delete_resource(limited_user, "sensitive_resource")
    
    # Test proper access
    admin_user = create_test_user(permissions=["read", "write", "delete"])
    result = delete_resource(admin_user, "test_resource")
    assert result.success
```

### Vulnerability Testing

```python
@pytest.mark.security
def test_secret_handling():
    """Test secure handling of secrets"""
    # Test secrets are not logged
    with capture_logs() as log_capture:
        process_with_secret("secret_api_key_123")
    
    logs = log_capture.get_logs()
    assert "secret_api_key_123" not in logs
    assert "***" in logs  # Verify secret is masked
    
    # Test secrets are not exposed in error messages
    with pytest.raises(APIError) as exc_info:
        api_call_with_invalid_secret("invalid_secret")
    
    error_message = str(exc_info.value)
    assert "invalid_secret" not in error_message

@pytest.mark.security
def test_data_encryption():
    """Test data encryption and decryption"""
    sensitive_data = "sensitive user information"
    
    # Test encryption
    encrypted = encrypt_data(sensitive_data)
    assert encrypted != sensitive_data
    assert len(encrypted) > len(sensitive_data)
    
    # Test decryption
    decrypted = decrypt_data(encrypted)
    assert decrypted == sensitive_data
    
    # Test encryption with different keys produces different results
    encrypted2 = encrypt_data(sensitive_data, different_key=True)
    assert encrypted2 != encrypted
```

## 📊 Test Reporting

### Coverage Reports

```python
# Generate coverage reports
pytest --cov=Scripts/xkit --cov-report=html --cov-report=term

# Coverage configuration in .coveragerc
[run]
source = Scripts/xkit
omit = 
    */tests/*
    */venv/*
    */__pycache__/*
    */migrations/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:

[html]
directory = htmlcov
```

### Test Reports

```python
# Generate HTML test report
pytest --html=report.html --self-contained-html

# Generate JUnit XML report for CI
pytest --junit-xml=junit.xml
```

### Continuous Integration

```yaml
# GitHub Actions test workflow
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: [3.11, 3.12]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .[dev]
    
    - name: Run tests
      run: |
        pytest tests/ -v \
          --cov=Scripts/xkit \
          --cov-report=xml \
          --junit-xml=junit.xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

## 🛠️ Testing Tools

### Custom Test Utilities

```python
# conftest.py - Shared test configuration
import pytest
import asyncio
import tempfile
from pathlib import Path

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def temp_git_repo():
    """Create temporary Git repository"""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir)
        # Initialize Git repo
        subprocess.run(["git", "init"], cwd=repo_path, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo_path)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_path)
        yield repo_path

@pytest.fixture
def mock_ai_service():
    """Mock AI service for testing"""
    service = Mock()
    service.analyze.return_value = {
        "summary": "Test analysis",
        "suggestions": ["Test suggestion"]
    }
    return service

class XKitTestSession:
    """Test session for E2E testing"""
    
    def __init__(self):
        self.app = None
        self.output_buffer = []
    
    def start(self):
        """Start test session"""
        self.app = XKitApplication()
        # Configure for testing
        
    def execute(self, command, args=None):
        """Execute command in test session"""
        args = args or []
        result = self.app.execute_command(command, args)
        self.output_buffer.append(result)
        return result
    
    def get_output(self):
        """Get all output from session"""
        return "\n".join(str(result) for result in self.output_buffer)
```

### Test Data Factories

```python
import factory
from factory import Faker

class GitStatusFactory(factory.Factory):
    """Factory for creating GitStatus test objects"""
    
    class Meta:
        model = GitStatus
    
    branch = "main"
    is_dirty = False
    staged_files = factory.List([])
    modified_files = factory.List([])
    untracked_files = factory.List([])

class PluginMetadataFactory(factory.Factory):
    """Factory for creating PluginMetadata test objects"""
    
    class Meta:
        model = PluginMetadata
    
    name = Faker('slug')
    version = "1.0.0"
    description = Faker('sentence')
    author = Faker('name')
    dependencies = factory.List([])
    provides = factory.List([])
    requires = factory.List([])

# Usage in tests
def test_with_factory_data():
    git_status = GitStatusFactory(is_dirty=True, modified_files=["test.py"])
    assert git_status.is_dirty is True
    assert "test.py" in git_status.modified_files
```

## 🔗 Related Documentation

- **[Contributing Guide](contributing.md)** - How to contribute to XKit
- **[Plugin Development](plugin-development.md)** - Creating custom plugins
- **[MCP Server Development](mcp-server-development.md)** - Building MCP servers

---

**Last Updated**: September 2025 | **Version**: v3.0.0  
**💙 Made with love by the XKit Community**