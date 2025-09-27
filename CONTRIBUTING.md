# 🤝 Como Contribuir - XKit v3.0.0

Obrigado pelo interesse em contribuir com o XKit v3.0.0! Este guia vai te orientar no desenvolvimento com a nova Hybrid MCP Architecture.

## 🎯 Visão Geral v3.0.0

O XKit v3.0.0 é uma plataforma de desenvolvimento moderna com:

- 🔌 **Hybrid MCP Architecture** - Extensibilidade via Model Context Protocol
- 🧩 **Plugin System** - Hot-reload e dependency injection
- 📡 **Event-Driven Design** - Comunicação assíncrona via event bus
- 🏗️ **Hexagonal Architecture** - Clean separation com ports/adapters
- 🤖 **AI-First** - Gemini 2.0 Flash integrado nativamente

## 🌿 Workflow de Contribuição v3.0.0

### 1. 🍴 Fork & Clone

```powershell
# Fork no GitHub, depois clone
git clone https://github.com/seu-usuario/WindowsPowerShell.git
cd WindowsPowerShell

# Adicione upstream
git remote add upstream https://github.com/rootkit-original/WindowsPowerShell.git
```

### 2. 🎯 Escolha o Tipo de Contribuição

| Tipo | Branch Base | Padrão de Nome | Exemplo |
|------|-------------|----------------|---------|
| **MCP Server** | `develop` | `feature/mcp-<server>` | `feature/mcp-github-server` |
| **Plugin** | `develop` | `feature/plugin-<name>` | `feature/plugin-docker-compose` |
| **AI Integration** | `develop` | `feature/ai-<feature>` | `feature/ai-code-review` |
| **Core Architecture** | `develop` | `feature/core-<area>` | `feature/core-event-bus` |
| **Bug Fix** | `develop` | `fix/descrição` | `fix/mcp-connection-timeout` |
| **Documentation** | `develop` | `docs/área` | `docs/mcp-server-guide` |
| **Hotfix** | `main` | `hotfix/v3.0.x-bug` | `hotfix/v3.0.1-startup-fail` |

### 3. 🚀 Criar Branch de Trabalho

```powershell
# Para features/fix/docs
git checkout develop
git pull upstream develop
git checkout -b feature/mcp-new-server

# Para hotfix
git checkout main  
git pull upstream main
git checkout -b hotfix/v3.0.1-fix-critico
```

### 4. 💻 Desenvolver com Hybrid MCP Architecture

#### 🏗️ **Estrutura do Código v3.0.0**
- **PowerShell**: Minimal wrapper em `Microsoft.PowerShell_profile.ps1`
- **Python Core**: Lógica em `Scripts/xkit/`
  - `core/` - Domain & Application layers
  - `adapters/` - External integrations  
  - `mcp/` - MCP servers and client
  - `plugins/` - Plugin system
  - `events/` - Event-driven architecture
- **Clean Architecture**: Domain/Application/Infrastructure

#### 📝 **Padrão de Commits v3.0.0**
Usamos **Conventional Commits** com escopos específicos:

```powershell
# MCP-related
git commit -m "feat(mcp): add GitHub integration MCP server"
git commit -m "fix(mcp): resolve connection timeout issues"

# Plugin system
git commit -m "feat(plugins): implement hot-reload mechanism"
git commit -m "fix(plugins): handle plugin loading errors"

# Event system
git commit -m "feat(events): add command execution events"
git commit -m "fix(events): prevent event loop blocking"

# AI integration
git commit -m "feat(ai): add code review capabilities"
git commit -m "fix(ai): handle Gemini API rate limits"

# Core architecture
git commit -m "feat(core): implement dependency injection container"
git commit -m "refactor(core): migrate to hexagonal architecture"
```

**Tipos e Escopos:**
- `feat(mcp|plugins|events|ai|core)` - Nova funcionalidade
- `fix(mcp|plugins|events|ai|core)` - Correção de bug
- `docs(api|mcp|plugins|usage)` - Documentação
- `refactor(core|adapters|infrastructure)` - Refatoração
- `test(unit|integration|e2e)` - Testes
- `chore(deps|config|build)` - Manutenção
- `docs` - Documentação
- `style` - Formatação de código
- `refactor` - Refatoração sem mudança de funcionalidade
- `test` - Adição/correção de testes
- `chore` - Tarefas de manutenção

### 5. 🧪 Testar

```powershell
# Teste manual básico
pwsh -Command "& './xkit-minimal.ps1'; xkit-help"

# Se tiver testes automatizados
python -m pytest Scripts/tests/

# Teste error handling
xtest-error
```

### 6. 📤 Push & Pull Request

```powershell
# Push da branch
git push origin feature/minha-nova-funcionalidade

# No GitHub:
# 1. Criar Pull Request
# 2. Base: develop (ou main para hotfix)  
# 3. Preencher template do PR
# 4. Solicitar review
```

## 📋 Template de Pull Request

```markdown
## 📝 Descrição
Breve descrição das mudanças.

## 🎯 Tipo de Mudança
- [ ] 🐛 Bug fix (correção que resolve um problema)  
- [ ] ✨ Nova feature (mudança que adiciona funcionalidade)
- [ ] 💥 Breaking change (correção/feature que quebra compatibilidade)
- [ ] 📚 Documentação (mudança apenas na documentação)
- [ ] 🔧 Refatoração (mudança que não corrige bug nem adiciona feature)

## 🧪 Como Testar
1. Passos para testar as mudanças
2. Comandos específicos para executar
3. Resultados esperados

## 📸 Screenshots
Se aplicável, adicione screenshots.

## ✅ Checklist
- [ ] 📝 Código segue convenções do projeto
- [ ] 🧪 Testes passam localmente  
- [ ] 📚 Documentação atualizada
- [ ] 🌿 Branch está atualizada com base
- [ ] 💬 Descrição clara das mudanças
```

## 🏗️ Diretrizes de Arquitetura

### 🐍 **Python Layer (Negócio)**
```python
# Scripts/xkit/domain/ - Entidades puras
class GitRepository:
    def __init__(self, path: str):
        self.path = path

# Scripts/xkit/application/ - Casos de uso
class GitStatusUseCase:
    def execute(self) -> GitStatus:
        # Lógica de negócio aqui
        pass

# Scripts/xkit/infrastructure/ - Implementações
class FileSystemGitRepository:
    def get_status(self) -> GitStatus:
        # Implementação específica
        pass
```

### ⚡ **PowerShell Layer (Ponte)**
```powershell
# oh-my-xkit/plugins/git/git.plugin.ps1
function global:xstatus {
    param([Parameter(ValueFromRemainingArguments)]$args)
    Invoke-XKitPython "git-status" @args
}
```

### 📊 **Princípios de Design**
1. **PowerShell É Ponte** - Mínima lógica, só chamadas Python
2. **Python É Cérebro** - Toda UX rica e lógica de negócio
3. **Clean Architecture** - Separação clara de responsabilidades
4. **Error-First** - Todo comando deve ter tratamento de erro
5. **Rich UX** - Emojis e feedback visual em Python

## 🐛 Reportando Issues

### 🔍 **Antes de Reportar**
1. ✅ Procure por issues similares existentes
2. ✅ Teste na versão mais recente
3. ✅ Reproduza o problema consistentemente

### 📝 **Template de Issue**
```markdown
## 🐛 Descrição do Bug
Descrição clara e concisa do problema.

## 🔄 Reproduzir
1. Execute comando '...'
2. Veja erro '...'
3. Resultado esperado era '...'

## 💻 Ambiente
- **XKit Version**: `xkit-version`
- **OS**: Windows 10/11
- **PowerShell**: `$PSVersionTable.PSVersion`
- **Python**: `python --version`

## 📸 Screenshots
Se aplicável, adicione screenshots do erro.

## 📋 Logs
```
Cole logs relevantes aqui
```
```

## 🎯 Áreas que Precisam de Contribuição

### 🚀 **Features em Desenvolvimento**
- [ ] **Integração Postman** - Geração automática de collections
- [ ] **Git Workflows Avançados** - Merge strategies inteligentes  
- [ ] **Container Orchestration** - Kubernetes support
- [ ] **AI Error Prediction** - Prevenção proativa de erros

### 📚 **Documentação**
- [ ] **API Reference** - Documentação completa da API Python
- [ ] **Tutorial Videos** - Screencasts de funcionalidades
- [ ] **Examples Gallery** - Casos de uso práticos
- [ ] **Architecture Deep-dive** - Guia detalhado da arquitetura

### 🧪 **Testes & Qualidade**
- [ ] **Unit Tests** - Cobertura dos use cases
- [ ] **Integration Tests** - Testes end-to-end
- [ ] **Performance Tests** - Benchmarks de performance
- [ ] **CI/CD Pipeline** - Automação completa

## 🏆 Reconhecimentos

Contribuidores são reconhecidos em:
- 📜 **CHANGELOG.md** - Créditos por versão
- 🎖️ **GitHub Contributors** - Seção no README
- 🌟 **Hall of Fame** - Maiores contribuidores

## 📞 Suporte

- 💬 **Discord**: [Link do servidor]
- 📧 **Email**: xkit-dev@domain.com
- 🐙 **Issues**: Use GitHub Issues para discussão
- 🤖 **AI Help**: `question "como contribuir com feature X"`

## 📄 Código de Conduta

Este projeto adere ao [Contributor Covenant](https://contributor-covenant.org/). Esperamos que todos os participantes sigam estas diretrizes para manter uma comunidade acolhedora.

---

**Obrigado por tornar o XKit ainda melhor!** 🚀✨