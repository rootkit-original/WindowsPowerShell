# 🔧 API Reference - XKit v2.1

## 🐍 Python API

### Core Components

#### Domain Layer
```python
from xkit.domain.entities import Project, Error
from xkit.domain.interfaces import IFileSystem, IDisplayService
```

#### Application Layer
```python
from xkit.application.use_cases import (
    ShowVersionUseCase,
    ShowHelpUseCase, 
    ShowStatusUseCase
)
```

#### Infrastructure Layer
```python
from xkit.infrastructure.display import DisplayService
from xkit.infrastructure.filesystem import FileSystemService
from xkit.infrastructure.ai_service import GeminiAIService
```

### 📝 Usage Examples

#### Criar Novo Comando
```python
# 1. Adicionar use case
class NewFeatureUseCase:
    def execute(self, params):
        # Lógica do comando
        pass

# 2. Registrar em xkit_main.py
actions["new-feature"] = new_feature_use_case.execute

# 3. Adicionar função PowerShell
function global:xnew-feature { 
    Invoke-XKit "new-feature" @args 
}
```

#### Error Handling
```python
try:
    result = some_operation()
except Exception as e:
    error_handler.handle_error(str(e), "context")
```