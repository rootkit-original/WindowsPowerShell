# XKit v2.1 - Arquitetura Técnica

## 🏗️ Clean Architecture Overview

O XKit segue os princípios de Clean Architecture, mantendo separação clara de responsabilidades e facilitando manutenção e testes.

## 📐 Estrutura das Camadas

```
Scripts/xkit/
├── domain/                 # Regras de negócio
│   ├── entities.py        # Entidades principais  
│   └── interfaces.py      # Contratos/Abstrações
├── application/           # Casos de uso
│   └── use_cases.py      # Lógica de aplicação
└── infrastructure/       # Implementações
    ├── compact_display.py    # Interface compacta
    ├── ai_service.py        # Integração Gemini AI
    ├── telegram_service.py  # Notificações Telegram
    ├── environment.py       # Detecção ambiente
    ├── container.py         # Gerenciamento containers
    ├── git.py              # Operações Git
    └── file_system.py      # Sistema de arquivos
```

## 🎯 Domain Layer

### Entities (Entidades de Negócio)

```python
@dataclass
class DevelopmentContext:
    """Contexto completo de desenvolvimento"""
    project: ProjectInfo
    git: Optional[GitInfo] = None
    readme: Optional[ReadmeInfo] = None
    container: Optional[ContainerInfo] = None
    environment: Optional[EnvironmentInfo] = None

@dataclass  
class ProjectInfo:
    """Informações do projeto"""
    name: str
    path: Path
    type: str
    technologies: List[str]
    
@dataclass
class ContainerInfo:
    """Informações de containers"""
    engine_type: str  # 'podman', 'docker'
    engine_path: Path
    is_available: bool
    has_compose: bool = False
```

### Interfaces (Contratos)

```python
class IProjectRepository(ABC):
    """Contrato para operações de projeto"""
    @abstractmethod
    def get_project_info(self, path: Path) -> ProjectInfo:
        pass

class IAIService(ABC):
    """Contrato para serviços de AI"""  
    @abstractmethod
    def analyze_context(self, context: str) -> str:
        pass
        
class INotificationService(ABC):
    """Contrato para notificações"""
    @abstractmethod
    def send_alert(self, message: str) -> bool:
        pass
```

## ⚙️ Application Layer

### Use Cases (Casos de Uso)

```python
class AnalyzeProjectUseCase:
    """Analisa o contexto do projeto atual"""
    
    def __init__(self, file_repo, git_repo, container_repo, analyzer):
        self.file_repo = file_repo
        self.git_repo = git_repo  
        self.container_repo = container_repo
        self.analyzer = analyzer
        
    def execute(self, project_path: Path) -> DevelopmentContext:
        # Lógica de análise...
        return context

class ShowAISuggestionsUseCase:
    """Mostra sugestões da AI baseadas no contexto"""
    
    def execute(self, context: DevelopmentContext) -> None:
        suggestions = self.ai_service.analyze_context(context)
        self.display.show_ai_suggestions(suggestions)
```

### Principais Use Cases

- **AnalyzeProjectUseCase** - Análise completa do projeto
- **ShowWelcomeUseCase** - Interface de boas-vindas
- **ShowStatusUseCase** - Status detalhado do sistema
- **ShowAISuggestionsUseCase** - Sugestões inteligentes
- **AskAISolutionUseCase** - Resolução de problemas
- **ExecuteContainerCommandUseCase** - Comandos de container

## 🔧 Infrastructure Layer

### Services (Implementações)

#### CompactDisplayService
```python
class CompactDisplayService:
    """Interface compacta estilo oh-my-zsh"""
    
    def show_compact_header(self, context: DevelopmentContext):
        """Mostra header compacto com informações essenciais"""
        # 🪟 📁projeto 🌿branch ✓ 🐳container 🐍💙
        
    def show_ai_suggestions(self, suggestions: List[str]):
        """Exibe sugestões da AI de forma compacta"""
```

#### GeminiAIService  
```python
class GeminiAIService:
    """Integração com Gemini AI da Google"""
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.base_url = 'https://generativelanguage.googleapis.com'
        
    def analyze_context(self, context: str) -> str:
        """Análise inteligente do contexto"""
        
    def solve_problem(self, problem: str, context: str) -> str:
        """Resolução de problemas específicos"""
```

#### TelegramService
```python
class TelegramService:
    """Notificações via Telegram Bot"""
    
    def __init__(self):
        self.token = os.getenv('TELEGRAM_TOKEN') 
        self.admin_id = os.getenv('ADMIN_ID')
        
    def send_alert(self, message: str) -> bool:
        """Envia alertas para o administrador"""
        
    def send_anomaly_report(self, anomalies: List[str]) -> bool:
        """Relatório de anomalias detectadas"""
```

#### EnvironmentDetector
```python
class EnvironmentDetector:
    """Detecção avançada do ambiente"""
    
    def detect_environment(self) -> EnvironmentInfo:
        """Detecta Windows/WSL/Container/Cloud"""
        
    def detect_development_tools(self) -> Dict[str, bool]:
        """Detecta ferramentas de desenvolvimento"""
        # Python, Node.js, .NET, Java, etc.
```

## 🚀 Application Entry Point

### XKitCompactApplication

```python
class XKitCompactApplication:
    """Ponto de entrada principal da aplicação"""
    
    def __init__(self):
        # Dependency Injection
        self._setup_dependencies()
        
    def _setup_dependencies(self):
        """Configuração de injeção de dependência"""
        # Infrastructure
        self.file_system = FileSystemRepository()
        self.git_repo = GitRepository() 
        self.container_repo = ContainerRepository()
        
        # Services  
        self.display_service = CompactDisplayService()
        self.ai_service = GeminiAIService()
        self.telegram_service = TelegramService()
        
        # Use Cases
        self.analyze_project = AnalyzeProjectUseCase(...)
        self.show_welcome = ShowWelcomeUseCase(...)
        
    def run(self, args: List[str]) -> None:
        """Executa comando baseado nos argumentos"""
        command = args[0] if args else 'welcome'
        self._route_command(command, args[1:])
```

## 🔄 Data Flow

### Fluxo de Análise de Projeto

1. **Entry Point** - `xkit_compact.py` recebe comando
2. **Application** - XKitCompactApplication roteia para use case  
3. **Use Case** - AnalyzeProjectUseCase coordena análise
4. **Repositories** - Coletam dados (filesystem, git, containers)
5. **Domain** - Cria DevelopmentContext com regras de negócio
6. **Services** - AI analisa contexto, Telegram envia alertas
7. **Display** - CompactDisplayService apresenta resultado

### Fluxo de Comando AI

1. **Usuário** executa `xkit-ai "pergunta"`
2. **Application** chama AskAISolutionUseCase  
3. **Use Case** coleta contexto atual
4. **AI Service** processa pergunta + contexto
5. **Display Service** formata e exibe resposta
6. **Telegram Service** envia log da interação (opcional)

## 🧪 Dependency Injection

### Padrão de Injeção

```python
# Construção das dependências
def _setup_dependencies(self):
    # Infrastructure layer (implementações concretas)
    file_repo = FileSystemRepository()
    git_repo = GitRepository()
    container_repo = ContainerRepository()
    
    # Services layer  
    display = CompactDisplayService()
    ai = GeminiAIService()
    telegram = TelegramService()
    
    # Application layer (casos de uso)
    self.analyze_project = AnalyzeProjectUseCase(
        file_repo, git_repo, container_repo, analyzer
    )
    self.show_ai = ShowAISuggestionsUseCase(display, ai)
```

### Benefícios

- **Testabilidade** - Mocks fáceis para testes
- **Flexibilidade** - Troca de implementações sem alterar regras
- **Manutenibilidade** - Mudanças isoladas por camada
- **Single Responsibility** - Cada classe tem uma responsabilidade

## 🔧 Configuration Management

### Environment Variables

```python
# Configurações padrão no perfil PowerShell
$env:GEMINI_API_KEY = 'chave_da_api'
$env:TELEGRAM_TOKEN = 'token_do_bot'  
$env:ADMIN_ID = 'seu_telegram_id'

# Configurações opcionais
$env:XKIT_DEBUG = 'true'
$env:XKIT_CACHE_TTL = '300'
$env:CONTAINER_ENGINE = 'podman'
```

### Configuration Classes

```python
@dataclass
class XKitConfig:
    """Configurações centralizadas"""
    gemini_api_key: str
    telegram_token: str
    admin_id: str
    debug_mode: bool = False
    cache_ttl: int = 300
    
    @classmethod
    def from_environment(cls) -> 'XKitConfig':
        return cls(
            gemini_api_key=os.getenv('GEMINI_API_KEY', ''),
            telegram_token=os.getenv('TELEGRAM_TOKEN', ''),
            admin_id=os.getenv('ADMIN_ID', ''),
            debug_mode=os.getenv('XKIT_DEBUG', '').lower() == 'true',
            cache_ttl=int(os.getenv('XKIT_CACHE_TTL', '300'))
        )
```

## 🎯 Design Patterns

### Repository Pattern
- Abstrai acesso a dados (filesystem, git, containers)
- Permite testes com mocks
- Facilita mudanças de implementação

### Strategy Pattern  
- ContainerService suporta Podman/Docker
- DisplayService pode ter temas diferentes
- AIService pode usar diferentes provedores

### Observer Pattern
- TelegramService observa anomalias
- DisplayService observa mudanças de contexto
- Logs automáticos de eventos importantes

### Command Pattern
- Cada comando do CLI é um Command object
- Facilita undo/redo (futuro)
- Permite queuing de comandos

## 📊 Error Handling

### Estratégia de Erros

```python
class XKitException(Exception):
    """Exceção base do XKit"""
    pass

class ContainerNotAvailableException(XKitException):
    """Container engine não disponível"""
    pass

class AIServiceException(XKitException):
    """Erro no serviço de AI"""
    pass

# Tratamento centralizado
try:
    result = use_case.execute()
except XKitException as e:
    display_service.show_error(e)
    telegram_service.send_error_alert(e)
```

### Logging

```python
import logging

logger = logging.getLogger('xkit')
logger.setLevel(logging.INFO)

# Logs estruturados
logger.info("Project analyzed", extra={
    'project_name': project.name,
    'technologies': project.technologies,
    'has_containers': bool(container_info)
})
```

## 🧪 Testing Strategy

### Unit Tests
```python
class TestAnalyzeProjectUseCase:
    def test_analyze_python_project(self):
        # Mock repositories
        file_repo = Mock()
        git_repo = Mock()  
        container_repo = Mock()
        
        # Setup mocks
        file_repo.get_project_info.return_value = ProjectInfo(...)
        
        # Test use case
        use_case = AnalyzeProjectUseCase(file_repo, git_repo, container_repo)
        result = use_case.execute(Path('/test'))
        
        # Assertions
        assert result.project.name == 'test'
```

### Integration Tests
- Testes com APIs reais (opcional)
- Validação de comandos PowerShell
- Testes de interface compacta

## 🚀 Performance Considerations

### Otimizações

- **Lazy Loading** - Serviços carregam apenas quando necessário
- **Caching** - Resultados de análise são cachéados
- **Async Operations** - Chamadas de API não bloqueantes (futuro)
- **Minimal Dependencies** - Apenas imports necessários

### Métricas

```python
@dataclass 
class PerformanceMetrics:
    startup_time: float
    analysis_time: float
    ai_response_time: float
    memory_usage: int
```

---

**Esta arquitetura garante que o XKit seja maintível, testável e extensível, seguindo as melhores práticas de desenvolvimento de software.**