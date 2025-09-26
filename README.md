# 🎨 XKit v2.1 - Kit de Desenvolvimento Windows Inteligente

> **Sistema inteligente de desenvolvimento Windows com arquitetura Python-first e ponte PowerShell ultra-minimal**

[![Version](https://img.shields.io/badge/version-2.1.2-blue.svg)](https://github.com/user/xkit)
[![PowerShell](https://img.shields.io/badge/PowerShell-5.1%2B-blue.svg)](https://github.com/PowerShell/PowerShell)
[![Python](https://img.shields.io/badge/Python-3.11+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Visão Geral

O XKit v2.1 é um framework de desenvolvimento com arquitetura Clean e ponte minimal PowerShell:

- **🐍 Python-First** - Toda lógica de negócio em Python com Clean Architecture
- **⚡ PowerShell Minimal** - Ponte ultra-simples chamando Python
- **🤖 Error Handling IA** - Sistema @xpilot para tratamento inteligente de erros
- **🏗️ Clean Architecture** - Domínio/Aplicação/Infraestrutura bem definidos
- **📱 Integrações IA** - Gemini AI + Telegram para notificações
- **🎨 Interface Rica** - Emojis e UX elaborada em Python

## ✨ Recursos Principais

- 🎨 **Oh-my-zsh inspired** para Windows PowerShell
- 🤖 **IA integrada** com error handling inteligente (@xpilot)
- 🏗️ **Clean Architecture** (Domain/Application/Infrastructure) 
- 🔧 **Git workflow** automatizado com branching inteligente
- 📱 **Telegram notifications** e assistente AI
- 🐳 **Container management** (Docker/Podman) integrado
- 🎯 **Comandos padronizados** com prefixo 'x' e nomes intuitivos

## 🚀 Instalação Rápida

```powershell
# Clone o repositório
git clone https://github.com/user/xkit.git "$env:USERPROFILE\Documents\WindowsPowerShell"

# Execute o setup (instala dependências Python)
python Scripts\xkit-setup.py

# Recarregue o PowerShell
powershell
```

## 🎯 Comandos Principais

### 📁 Git Commands

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `xstatus` | git status | `xstatus` |
| `xadd` | git add | `xadd .` |
| `xcommit` | git commit | `xcommit -m "feat: nova funcionalidade"` |
| `xpush` | git push | `xpush origin main` |
| `xlog` | git log | `xlog --graph` |
| `xbranch` | git branch | `xbranch feature/nova-feature` |
| `xcheckout` | git checkout | `xcheckout main` |

### 🐳 Container Commands

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `xpodman` | Podman geral | `xpodman ps -a` |
| `xcontainers` | Lista containers | `xcontainers` |
| `ximages` | Lista imagens | `ximages` |

## 🏗️ Arquitetura

```
XKit v2.1 Architecture
├── PowerShell Layer (Minimal)
│   ├── Microsoft.PowerShell_profile.ps1  # Profile básico
│   ├── xkit-minimal.ps1                  # Loader principal
│   └── oh-my-xkit/                       # Framework plugins
│       ├── oh-my-xkit.ps1               # Core do framework
│       └── plugins/                      # Plugins específicos
├── Python Layer (Business Logic)
│   ├── xkit_main.py                     # Ponto de entrada
│   └── xkit/                            # Clean Architecture
│       ├── domain/                      # Entidades de negócio
│       ├── application/                 # Casos de uso
│       └── infrastructure/              # Serviços externos
└── Configuration
    ├── Environment variables            # Configuração de paths
    └── UTF-8 setup                     # Suporte a emojis
```

## 🤖 Sistema @xpilot

O XKit inclui um sistema inteligente de tratamento de erros:

- **Análise automática** - IA analisa padrões de erro
- **Sugestões contextuais** - Oferece soluções baseadas no contexto
- **Git integration** - Cria branches para correções
- **Telegram alerts** - Notificações de erro por Telegram

```powershell
# Exemplo: erro é automaticamente tratado pelo @xpilot
PS> xcommit -m "fix bug"
❌ Error detected: git staging area empty
🤖 @xpilot suggestion: Run 'xadd .' first
📝 Auto-creating branch: error/empty-staging-area
```

## 📊 Performance

- ⚡ **Startup**: < 200ms para inicialização do Python
- 🧠 **Memória**: ~15MB footprint típico
- 🔄 **Resposta**: Comandos instantâneos via Python cache

## 🛠️ Desenvolvimento

### Estrutura do Plugin

```powershell
# PowerShell Plugin (Minimal)
function global:meu-comando {
    param([Parameter(ValueFromRemainingArguments)]$args)
    Invoke-XKitPython "meu-comando" @args
}
```

```python
# Python Use Case (Rich Logic)
class MeuComandoUseCase:
    def __init__(self, display_service, git_service):
        self.display = display_service
        self.git = git_service
    
    def execute(self, args):
        try:
            # Lógica de negócio complexa aqui
            result = self._process(args)
            self.display.success("✅ Comando executado!")
            return result
        except Exception as e:
            self.error_handler.handle("meu-comando", str(e))
```

## 📚 Documentação

- [📖 USAGE.md](USAGE.md) - Guia de uso completo
- [🔧 INSTALL.md](INSTALL.md) - Instalação detalhada  
- [🏗️ ARCHITECTURE.md](ARCHITECTURE.md) - Arquitetura técnica
- [🐛 TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Solução de problemas
- [📝 API.md](API.md) - Referência da API Python

## 🤝 Contribuindo

1. **Fork** o projeto
2. **Clone** localmente
3. **Crie** branch para sua feature
4. **Teste** com o sistema @xpilot
5. **Submeta** PR com descrição clara

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes.

## 📜 Changelog

### v2.1.2 (2025-09-26)
- 🐛 **Fix**: README corrigido e documentação melhorada
- 📚 **Docs**: Estrutura de documentação reorganizada

### v2.1.1 (2025-09-26)  
- 📚 **Docs**: Documentação completa recriada do zero
- 🎯 **Standards**: Comandos padronizados com prefixo 'x'

### v2.1.0 (2025-09-26)
- ✨ **New**: Clean Architecture completa implementada
- 🤖 **New**: Sistema @xpilot de error handling inteligente
- 🔧 **Breaking**: Comandos padronizados (gst→xstatus, etc.)

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

## 🔗 Links Úteis

- [🐙 GitHub](https://github.com/user/xkit)
- [📱 Telegram Bot](https://t.me/xkit_bot)
- [🤖 IA Assistant](https://gemini.google.com/)

---

**XKit v2.1** - *Desenvolvimento Windows inteligente com arquitetura Python* 🚀