# Changelog

Todas as mudanças notáveis deste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [2.1.0] - 2025-09-26

### ✨ Adicionado

#### 🎯 Prompt Personalizado
- Prompt estilo bash/zsh: `Usuario@COMPUTADOR [branch] ~/path`
- Detecção automática de branch Git
- Cores personalizadas para melhor visibilidade
- Path simplificado com `~` para home directory

#### 🐳 Container Management Completo  
- Detecção automática do `podman-compose v1.5.0`
- Comandos `compose-up` e `compose-down` integrados
- Comando `container-status` unificado para diagnóstico
- Auto-detecção de arquivos compose no projeto
- Suporte completo a Podman e Docker engines

#### 🤖 Integração Inteligente com AI
- **Gemini AI** integrado para sugestões contextuais
- Comando `xkit-ai` para análise inteligente do ambiente
- Comando `xkit-solve` para resolução específica de problemas
- Análise automática do contexto do projeto atual

#### 📱 Sistema de Notificações
- **Telegram Bot** integrado para alertas
- Notificações automáticas de anomalias detectadas
- Sistema de logging de interações importantes
- Monitoramento proativo do ambiente

#### 🎨 Interface Ultra-Compacta
- Header compacto: `🪟 📁projeto 🌿branch ✓ 🐳container 🐍💙`
- Informações contextuais em tempo real
- Status visual com emojis significativos  
- Compatibilidade com estilo oh-my-zsh

### 🏗️ Melhorado

#### Clean Architecture
- Separação clara em camadas Domain/Application/Infrastructure
- Injeção de dependência implementada corretamente
- Interfaces bem definidas para testabilidade
- Código organizado e manutenível

#### Performance e Confiabilidade
- Carregamento otimizado do perfil PowerShell
- Detecção eficiente de ferramentas instaladas
- Cache inteligente para evitar consultas desnecessárias
- Tratamento robusto de erros e exceções

#### Documentação
- README.md completo com exemplos práticos
- INSTALL.md com guia passo-a-passo detalhado
- USAGE.md com manual completo de comandos
- ARCHITECTURE.md com documentação técnica profunda

### 🗂️ Organizado

#### Estrutura de Arquivos
- Arquivos legacy removidos e código limpo mantido
- Pasta `Scripts/tools/` criada para utilitários
- Documentação centralizada na raiz do projeto
- Separação clara entre código core e ferramentas auxiliares

#### Comandos Simplificados
- Interface unificada através de `xkit-*` commands
- Remoção de duplicações e comandos obsoletos
- Comandos intuitivos e bem documentados
- Help system contextual integrado

### 🔧 Técnico

#### Requisitos de Sistema
- **Windows 10/11** - Sistema operacional suportado
- **PowerShell 5.1+** - Shell moderno requerido
- **Python 3.11+** - Runtime para core do XKit
- **Git** - Para detecção de contexto de repositório

#### APIs e Integrações
- **Gemini AI API** - Para inteligência artificial
- **Telegram Bot API** - Para notificações
- **Podman/Docker** - Para gerenciamento de containers
- **podman-compose** - Para orquestração de serviços

#### Configurações
```powershell
$env:GEMINI_API_KEY = 'sua_api_key_aqui'
$env:TELEGRAM_TOKEN = 'seu_token_aqui'  
$env:ADMIN_ID = 'seu_id_aqui'
```

## [Unreleased] - Futuras Versões

### 🚀 Planejado para v2.2
- [ ] Dashboard web opcional para métricas
- [ ] Suporte a múltiplos projetos simultâneos
- [ ] Plugin system para extensibilidade
- [ ] Integração com VS Code

### 🔮 Planejado para v2.3
- [ ] AI model switching (Gemini/GPT/Local)
- [ ] Métricas de produtividade avançadas
- [ ] Exportação de relatórios de desenvolvimento
- [ ] Integração com mais container engines

## Estrutura Final

```
WindowsPowerShell/
├── README.md                           # Documentação principal  
├── INSTALL.md                          # Guia de instalação
├── USAGE.md                           # Manual de uso
├── ARCHITECTURE.md                    # Documentação técnica
├── CHANGELOG.md                       # Este arquivo
├── Microsoft.PowerShell_profile.ps1   # Perfil otimizado
├── gh-copilot.ps1                     # GitHub Copilot integration
└── Scripts/
    ├── xkit_compact.py               # ⭐ Aplicação principal
    ├── xkit/                         # 🏗️ Clean Architecture
    │   ├── domain/                   # Entidades de negócio
    │   ├── application/              # Casos de uso  
    │   └── infrastructure/           # Implementações
    └── tools/                        # 🔧 Utilitários
        ├── xkit-final-validator.py    # Validador do sistema
        └── test-prompt.py            # Teste do prompt
```

## Comandos Principais

### Interface
- `xkit-help` - Lista todos comandos disponíveis
- `xkit-status` - Status detalhado do ambiente
- `xkit-info` - Informações do projeto atual

### AI Integration  
- `xkit-ai` - Sugestões inteligentes baseadas no contexto
- `xkit-solve "problema"` - Resolução específica de problemas

### Container Management
- `compose-up` - Subir serviços via compose
- `compose-down` - Parar todos os serviços
- `container-status` - Status completo dos containers

### Utilitários
- `xkit-reload` - Recarregar perfil PowerShell

---

**XKit v2.1** representa uma evolução completa com foco em usabilidade, inteligência artificial e gerenciamento avançado de containers em ambiente Windows.