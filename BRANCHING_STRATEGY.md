# 🌿 XKit Branching Strategy

## 🎯 GitHub Flow Modificado

O XKit utiliza uma estratégia de branching baseada no **GitHub Flow Modificado**, otimizada para desenvolvimento ágil de frameworks com estabilidade.

## 🏗️ Estrutura de Branches

### 📋 Branches Principais

| Branch | Propósito | Proteção | Deploy |
|--------|-----------|-----------|---------|
| `main` | **Produção estável** - Código pronto para release | 🛡️ Protegido | ✅ Auto |
| `develop` | **Integração contínua** - Features testadas | 🛡️ Semi-protegido | 🧪 Staging |

### 🚀 Branches de Trabalho

| Padrão | Propósito | Exemplo | Merge Para |
|--------|-----------|---------|------------|
| `feature/*` | Novas funcionalidades | `feature/ai-error-detection` | `develop` |
| `hotfix/*` | Correções urgentes | `hotfix/v2.1.3-memory-leak` | `main` + `develop` |
| `docs/*` | Melhorias de documentação | `docs/api-reference-update` | `develop` |
| `refactor/*` | Refatoração sem nova funcionalidade | `refactor/clean-architecture` | `develop` |
| `chore/*` | Tarefas de manutenção | `chore/update-dependencies` | `develop` |

## 🔄 Workflow de Desenvolvimento

### 1. 🆕 Nova Funcionalidade

```powershell
# 1. Atualizar develop
git checkout develop
git pull origin develop

# 2. Criar feature branch
git checkout -b feature/nome-da-funcionalidade

# 3. Desenvolver, commit, push
git add .
git commit -m "feat: implementar nova funcionalidade"
git push origin feature/nome-da-funcionalidade

# 4. Criar Pull Request para develop
# 5. Code review + merge
# 6. Delete branch
git branch -d feature/nome-da-funcionalidade
```

### 2. 🐛 Hotfix Urgente

```powershell
# 1. Branch a partir do main
git checkout main
git pull origin main
git checkout -b hotfix/v2.1.3-fix-critical-bug

# 2. Corrigir, commit, push
git add .
git commit -m "fix: corrigir bug crítico"
git push origin hotfix/v2.1.3-fix-critical-bug

# 3. PR para main (release imediato)
# 4. PR para develop (manter sincronia)
# 5. Tag de versão no main
git tag -a v2.1.3 -m "Hotfix v2.1.3"
```

### 3. 📚 Release Process

```powershell
# 1. Preparar release no develop
git checkout develop
git pull origin develop

# 2. Merge develop → main
git checkout main
git pull origin main
git merge develop --no-ff -m "chore: release v2.2.0"

# 3. Tag da versão
git tag -a v2.2.0 -m "Release v2.2.0

✨ Features:
- Nova funcionalidade X
- Melhoria Y

🐛 Bug Fixes:
- Correção Z

📚 Documentation:
- Atualização de docs"

# 4. Push tudo
git push origin main --tags
```

## 📊 Regras de Branch

### 🛡️ Proteções do Branch `main`
- ✅ Require pull request reviews (1+ approvals)
- ✅ Require status checks to pass
- ✅ Require branches to be up to date
- ✅ Restrict pushes to main
- ✅ No force pushes

### 🔒 Proteções do Branch `develop`
- ✅ Require pull request reviews
- ✅ Allow maintainers to bypass
- ❌ Allow force pushes (para rebase limpo)

### 📝 Convenções de Naming

#### ✅ Correto:
```
feature/ai-error-detection
feature/telegram-integration
hotfix/v2.1.3-memory-leak
docs/update-api-reference
refactor/clean-architecture-domain
chore/update-python-dependencies
```

#### ❌ Incorreto:
```
fix-bug                    # Use: hotfix/v2.1.3-bug-name
new-feature               # Use: feature/feature-name
documentation             # Use: docs/what-you-are-updating
```

## 🚀 Comandos Úteis

### 📋 Status e Limpeza
```powershell
# Ver todas as branches
git branch -a

# Limpar branches merged
git branch --merged develop | grep -v "main\|develop\|master" | xargs -n 1 git branch -d

# Sincronizar com remoto
git remote prune origin

# Ver branches não merged
git branch --no-merged develop
```

### 🔄 Sincronização
```powershell
# Atualizar develop com main (após hotfix)
git checkout develop
git pull origin develop
git merge main --no-ff -m "chore: sync hotfix to develop"

# Rebase feature branch (manter histórico limpo)
git checkout feature/minha-feature
git rebase develop
```

## 🎯 Por que GitHub Flow Modificado?

### ✅ **Vantagens para XKit:**

1. **🚀 Simplicidade** - Fácil de entender e implementar
2. **⚡ Agilidade** - Deploy rápido de features
3. **🛡️ Estabilidade** - Main sempre estável para releases
4. **🔧 Flexibilidade** - Hotfixes independentes
5. **👥 Colaboração** - Code review obrigatório
6. **📦 Versionamento** - Semântico com tags claras

### 🎪 **Comparação com outras estratégias:**

| Estratégia | Complexidade | XKit Fit | Motivo |
|------------|--------------|----------|---------|
| **GitHub Flow Simples** | ⭐⭐ | ❌ | Sem develop = caos |
| **GitHub Flow Modificado** | ⭐⭐⭐ | ✅ | **Perfeito equilíbrio** |
| **Git Flow Completo** | ⭐⭐⭐⭐⭐ | ❌ | Muito complexo |
| **Trunk-based** | ⭐⭐ | ❌ | Requer CI/CD avançado |

## 🔮 Roadmap de Branches

### 🎯 **Próximas Features (develop)**
- `feature/enhanced-error-handling` 
- `feature/postman-integration`
- `feature/advanced-git-workflows`

### 📚 **Documentação (docs/)**
- `docs/api-complete-reference`
- `docs/contributor-guide-update`

### 🏗️ **Refatorações (refactor/)**
- `refactor/python-infrastructure-layer`
- `refactor/powershell-minimal-wrapper`

## 📞 Suporte

- 💬 **Issues**: Use GitHub Issues para discussão
- 📖 **Docs**: Consulte CONTRIBUTING.md para detalhes
- 🤖 **AI Help**: Use `question "git workflow question"`

---

**Mantido por**: XKit Development Team  
**Última atualização**: 2025-09-26  
**Versão**: 1.0