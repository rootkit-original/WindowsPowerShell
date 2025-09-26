# 🤝 Como Contribuir - XKit v2.1

Obrigado pelo interesse em contribuir com o XKit! Este guia vai te orientar no processo.

## 🎯 Visão Geral

O XKit segue **GitHub Flow Modificado** - veja [BRANCHING_STRATEGY.md](BRANCHING_STRATEGY.md) para detalhes completos.

## 🌿 Workflow de Contribuição

### 1. 🍴 Fork & Clone

```powershell
# Fork no GitHub, depois clone
git clone https://github.com/seu-usuario/xkit.git
cd xkit

# Adicione upstream
git remote add upstream https://github.com/user/xkit.git
```

### 2. 🎯 Escolha o Tipo de Contribuição

| Tipo | Branch Base | Padrão de Nome | Exemplo |
|------|-------------|----------------|---------|
| **Nova funcionalidade** | `develop` | `feature/nome` | `feature/postman-integration` |
| **Correção de bug** | `develop` | `fix/descrição` | `fix/error-handler-crash` |
| **Documentação** | `develop` | `docs/área` | `docs/api-reference` |
| **Refatoração** | `develop` | `refactor/área` | `refactor/clean-architecture` |
| **Hotfix urgente** | `main` | `hotfix/versão-bug` | `hotfix/v2.1.3-memory-leak` |

### 3. 🚀 Criar Branch de Trabalho

```powershell
# Para feature/fix/docs/refactor
git checkout develop
git pull upstream develop
git checkout -b feature/minha-nova-funcionalidade

# Para hotfix
git checkout main  
git pull upstream main
git checkout -b hotfix/v2.1.3-fix-critico
```

### 4. 💻 Desenvolver

#### 🏗️ **Estrutura do Código**
- **PowerShell**: Apenas ponte minimal em `oh-my-xkit/plugins/`
- **Python**: Lógica de negócio em `Scripts/xkit/`
- **Clean Architecture**: Domain/Application/Infrastructure

#### 📝 **Padrão de Commits**
Usamos **Conventional Commits**:

```powershell
# Formato: tipo(escopo): descrição
git commit -m "feat(git): adicionar comando xrebase inteligente"
git commit -m "fix(error): corrigir crash no sistema @xpilot"
git commit -m "docs(api): atualizar referência do GitService"
git commit -m "refactor(domain): extrair ErrorEntity para domain layer"
git commit -m "chore(deps): atualizar dependências Python"
```

**Tipos permitidos:**
- `feat` - Nova funcionalidade
- `fix` - Correção de bug
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