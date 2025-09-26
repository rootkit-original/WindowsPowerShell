# 🎯 Guia de Uso - XKit v2.1

Referência completa de todos os comandos e funcionalidades do XKit v2.1.

## 📁 Comandos Git

| Comando | Git Equivalente | Descrição | Exemplo |
|---------|----------------|-----------|---------|
| `xstatus` | `git status` | Mostra status do repositório | `xstatus` |
| `xadd` | `git add` | Adiciona arquivos ao stage | `xadd .` |
| `xcommit` | `git commit` | Faz commit das mudanças | `xcommit -m "feat: nova feature"` |
| `xpush` | `git push` | Envia mudanças para remote | `xpush origin main` |
| `xlog` | `git log` | Mostra histórico de commits | `xlog --oneline` |
| `xbranch` | `git branch` | Gerencia branches | `xbranch feature/nova` |
| `xcheckout` | `git checkout` | Troca de branch | `xcheckout main` |

## 🐳 Comandos Container

| Comando | Podman/Docker Equivalente | Descrição | Exemplo |
|---------|--------------------------|-----------|---------|
| `xpodman` | `podman` | Comando podman direto | `xpodman run -it ubuntu` |
| `xcontainers` | `podman ps` | Lista containers | `xcontainers -a` |
| `ximages` | `podman images` | Lista imagens | `ximages` |

## 🤖 IA e Telegram

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `question` | Pergunta ao assistente AI | `question "Como otimizar Python?"` |
| `tg` | Envia mensagem Telegram | `tg "Deploy concluído!"` |

## 🛡️ Error Handling

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `xerr` | Mostra detalhes do último erro | `xerr` |
| `xfix` | Tenta corrigir erro automaticamente | `xfix` |
| `xtest-error` | Testa o sistema de error handling | `xtest-error` |

## 🔧 Enhanced Commands

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `xgit` | Git com error handling avançado | `xgit status` |
| `xpython` | Python com error handling | `xpython script.py` |
| `xdocker` | Docker com error handling | `xdocker run hello-world` |
| `xnpm` | NPM com error handling | `xnpm install` |

## 💡 Sistema

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `xkit-help` | Mostra ajuda completa | `xkit-help` |
| `xkit-version` | Mostra informações da versão | `xkit-version` |
| `xkit-status` | Status detalhado do projeto | `xkit-status` |
| `xkit-reload` | Recarrega o profile | `xkit-reload` |

## 🎯 Exemplos Práticos

### Workflow Git Completo

```powershell
# 1. Ver status atual
xstatus

# 2. Adicionar mudanças
xadd .

# 3. Fazer commit
xcommit -m "feat: implementar login de usuário"

# 4. Enviar para repositório
xpush
```

### Gerenciar Containers

```powershell
# Ver containers rodando
xcontainers

# Ver todas as imagens
ximages

# Rodar novo container
xpodman run -d --name meu-app nginx
```

### Usar IA para Desenvolvimento

```powershell
# Pedir ajuda com código
question "Como implementar autenticação JWT em Python?"

# Pedir review de código
question "Este código está otimizado? [cola o código]"
```

### Sistema de Error Handling

```powershell
# Testar o sistema
xtest-error

# Se ocorrer erro real, usar:
xerr    # Ver detalhes
xfix    # Tentar correção automática
```

---

*Para mais detalhes, use `xkit-help` no terminal.*