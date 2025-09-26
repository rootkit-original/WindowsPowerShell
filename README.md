# XKit v2.1 - Kit de Desenvolvimento Windows Inteligente

[![PowerShell](https://img.shields.io/badge/PowerShell-5.1+-blue.svg)](https://docs.microsoft.com/en-us/powershell/)
[![Python](https://img.shields.io/badge/Python-3.11+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Sistema inteligente de desenvolvimento Windows com arquitetura Python-first e ponte PowerShell ultra-minimal**

## 🎯 Visão Geral

O XKit v2.1 é um framework de desenvolvimento com arquitetura Clean e ponte minimal PowerShell:

- **🐍 Python-First** - Toda lógica de negócio em Python com Clean Architecture
- **⚡ PowerShell Minimal** - Ponte ultra-simples chamando Python
- **🤖 Error Handling IA** - Sistema @xpilot para tratamento inteligente de erros
- **🏗️ Clean Architecture** - Domínio/Aplicação/Infraestrutura bem definidos
- **📱 Integrações IA** - Gemini AI + Telegram para notificações
- **🎨 Interface Rica** - Emojis e UX elaborada em Python

## 🚀 Interface em Ação

```bash
🚀 XKit - Ambiente de desenvolvimento ativo
==================================================
📁 Projeto: WindowsPowerShell
📜 XKit v2.1 - Kit de Desenvolvimento Windows Inteligente
💭 # XKit v2.1 - Kit de Desenvolvimento Windows Inteligente

[![PowerShell](https://img.shields.io/badge/PowerShell-5.1+-blue.svg)](https://docs.microsoft.com/en-us/powershell/)
[![Python](https://img.shields.io/badge/Python-3.11+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Sistema inteligente de desenvolvimento Windows com arquitetura Python-first e ponte PowerShell ultra-minimal**

## 🎯 Visão Geral

O XKit v2.1 é um framework de desenvolvimento com arquitetura Clean e ponte minimal PowerShell:

- **🐍 Python-First** - Toda lógica de negócio em Python com Clean Architecture
- **⚡ PowerShell Minimal** - Ponte ultra-simples chamando Python
- **🤖 Error Handling IA** - Sistema @xpilot para tratamento inteligente de erros
- **🏗️ Clean Architecture** - Domínio/Aplicação/Infraestrutura bem definidos
- **📱 Integrações IA** - Gemini AI + Telegram para notificações
- **🎨 Interface Rica** - Emojis e UX elaborada em Python

## 🚀 Interface em Ação

```text
🚀 XKit - Ambiente de desenvolvimento ativo
==================================================
📁 Projeto: WindowsPowerShell
📖 XKit v2.1 - Kit de Desenvolvimento Windows Inteligente
💭 > **Sistema inteligente de desenvolvimento Windows com AI e interface compacta estilo oh-my-zsh**
🛠️ Tecnologias: Python, PowerShell, Git
🌿 Branch: master (17 mudanças)
🐳 Container: Podman disponível

💡 Digite 'xkit-help' para ver comandos disponíveis
==================================================
🪟 📁WindowsPowerShell 🌿master ±17 📦podman 🐍💙📝
   ⚠️  2 anomalia(s) detectada(s)
   💡 xkit-help para comandos
```

## ⚡ Início Rápido

1. **Clone** este repositório para `$HOME\Documents\WindowsPowerShell`
2. **Configure** suas API keys em `xkit-minimal.ps1`
3. **Reinicie** o PowerShell
4. **Digite** `xkit-help` para começar

## 📦 Arquitetura Ultra-Minimal

```text
WindowsPowerShell/
├── Microsoft.PowerShell_profile.ps1  # Ultra-minimal profile loader
├── xkit-minimal.ps1                  # ⭐ Single PowerShell bridge
└── Scripts/
    ├── xkit_main.py                  # ⭐ Python entry point
    └── xkit/                         # 🏢 Clean Architecture
        ├── domain/                   # Business entities & interfaces
        ├── application/              # Use cases & orchestration
        └── infrastructure/           # External services & implementations
```

## 🔧 Comandos Principais

### Error Handling (@xpilot)

- `xtest-error` - Testar sistema de tratamento de erros
- `xerr` - Ver detalhes do último erro
- `xfix` - Tentar resolver último erro automaticamente

### Informações e Status

- `xkit-help` - Lista todos os comandos disponíveis
- `xkit-status` - Status detalhado do ambiente atual
- `xkit-version` - Ver versão do XKit

### Inteligência Artificial

- `question "pergunta"` - Fazer pergunta ao Gemini AI
- `tg "mensagem"` - Enviar mensagem via Telegram

## 🏢 Clean Architecture

### Domain Layer

- **Entities**: `DevelopmentContext`, `ProjectInfo`, `ErrorEntity`
- **Interfaces**: Contratos para repositórios e serviços
- **Business Rules**: Lógica de negócio pura

### Application Layer

- **Use Cases**: `HandleErrorUseCase`, `ShowWelcomeUseCase`
- **Orchestration**: Coordenação entre domínio e infraestrutura
- **Error Handling**: Sistema @xpilot integrado

### Infrastructure Layer

- **Services**: `GeminiAIService`, `TelegramService`
- **Repositories**: `FileSystemRepository`, `GitRepository`
- **Display**: `DisplayService` com suporte a emojis

## 🔧 Configuração

As configurações estão hard-coded em `xkit-minimal.ps1` para simplicidade:

```powershell
# API Keys (edit in xkit-minimal.ps1)
$env:GEMINI_API_KEY = 'your_api_key'
$env:TELEGRAM_TOKEN = 'your_bot_token'  
$env:ADMIN_ID = 'your_telegram_id'
```

## 🤖 Sistema @xpilot

### Fluxo de Error Handling

1. **Detecção**: PowerShell wrappers detectam erros
2. **Análise**: Python AI agent analisa padrões
3. **Git Integration**: Cria branch de erro automaticamente
4. **Resolução**: Fornece sugestões e auto-fixes
5. **Workflow**: Usuário pode aceitar fixes ou continuar

### Comandos de Error Handling

```powershell
xtest-error        # Simular erro para teste
xerr               # Ver detalhes do erro
xfix               # Tentar resolver automaticamente
```

## 📊 Performance

- **Startup Rápido** - PowerShell minimal, Python lazy-loaded
- **UTF-8 Nativo** - Emojis funcionam perfeitamente
- **Memória Baixa** - Arquitetura otimizada
- **Error Recovery** - Sistema robusto de recuperação

## 📁 Princípios de Desenvolvimento

1. **PowerShell É Ponte** - Mínimo lógica, apenas chamadas Python
2. **Python É Cérebro** - Toda lógica de negócio e UX rica
3. **Clean Architecture** - Separação clara de responsabilidades  
4. **Fail Fast** - Erros claros melhor que falhas silenciosas
5. **User-Centric** - Feedback rico e sugestões úteis

## 📋 Próximos Passos

Veja arquivos de documentação:

- **[INSTALL.md](INSTALL.md)** - Guia detalhado de instalação
- **[USAGE.md](USAGE.md)** - Manual completo de uso  
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Documentação técnica
- **[.github/copilot-instructions.md](.github/copilot-instructions.md)** - Instruções para GitHub Copilot

## 📄 Licença

Este projeto está sob a licença MIT. Veja [LICENSE](LICENSE) para detalhes.

---

**XKit v2.1** - PowerShell minimal, Python maximal 🚀
🔧 Tecnologias: Python, PowerShell, Git
🌿 Branch: master (17 mudanças)
🐳 Container: Podman disponível

💡 Digite 'xkit-help' para ver comandos disponíveis
==================================================
🪟 📁WindowsPowerShell 🌿master ±17 �podman 🐍💙📝
   ⚠️  2 anomalia(s) detectada(s)
   💡 xkit-help para comandos
```

## ⚡ Início Rápido

1. **Clone** este repositório para `$HOME\Documents\WindowsPowerShell`
2. **Configure** suas API keys em `xkit-minimal.ps1`
3. **Reinicie** o PowerShell
4. **Digite** `xkit-help` para começar

## 📦 Arquitetura Ultra-Minimal

```
WindowsPowerShell/
├── Microsoft.PowerShell_profile.ps1  # Ultra-minimal profile loader
├── xkit-minimal.ps1                  # ⭐ Single PowerShell bridge
└── Scripts/
    ├── xkit_main.py                  # ⭐ Python entry point
    └── xkit/                         # � Clean Architecture
        ├── domain/                   # Business entities & interfaces
        ├── application/              # Use cases & orchestration
        └── infrastructure/           # External services & implementations
```

## 🔧 Comandos Principais

### Error Handling (@xpilot)
- `xtest-error` - Testar sistema de tratamento de erros
- `xerr` - Ver detalhes do último erro
- `xfix` - Tentar resolver último erro automaticamente

### Informações e Status  
- `xkit-help` - Lista todos os comandos disponíveis
- `xkit-status` - Status detalhado do ambiente atual
- `xkit-version` - Ver versão do XKit

### Inteligência Artificial
- `question "pergunta"` - Fazer pergunta ao Gemini AI
- `tg "mensagem"` - Enviar mensagem via Telegram

## 🏢 Clean Architecture

### Domain Layer
- **Entities**: `DevelopmentContext`, `ProjectInfo`, `ErrorEntity`
- **Interfaces**: Contratos para repositórios e serviços
- **Business Rules**: Lógica de negócio pura

### Application Layer  
- **Use Cases**: `HandleErrorUseCase`, `ShowWelcomeUseCase`
- **Orchestration**: Coordenação entre domínio e infraestrutura
- **Error Handling**: Sistema @xpilot integrado

### Infrastructure Layer
- **Services**: `GeminiAIService`, `TelegramService`
- **Repositories**: `FileSystemRepository`, `GitRepository`
- **Display**: `DisplayService` com suporte a emojis

## 🔧 Configuração

As configurações estão hard-coded em `xkit-minimal.ps1` para simplicidade:

```powershell
# API Keys (edit in xkit-minimal.ps1)
$env:GEMINI_API_KEY = 'your_api_key'
$env:TELEGRAM_TOKEN = 'your_bot_token'  
$env:ADMIN_ID = 'your_telegram_id'
```

## 🤖 Sistema @xpilot

### Fluxo de Error Handling
1. **Detecção**: PowerShell wrappers detectam erros
2. **Análise**: Python AI agent analisa padrões
3. **Git Integration**: Cria branch de erro automaticamente
4. **Resolução**: Fornece sugestões e auto-fixes
5. **Workflow**: Usuário pode aceitar fixes ou continuar

### Comandos de Error Handling
```powershell
xtest-error        # Simular erro para teste
xerr               # Ver detalhes do erro
xfix               # Tentar resolver automaticamente
```

## 📊 Performance

- **Startup Rápido** - PowerShell minimal, Python lazy-loaded
- **UTF-8 Nativo** - Emojis funcionam perfeitamente
- **Memória Baixa** - Arquitetura otimizada
- **Error Recovery** - Sistema robusto de recuperação

## 📁 Princípios de Desenvolvimento

1. **PowerShell É Ponte** - Mínimo lógica, apenas chamadas Python
2. **Python É Cérebro** - Toda lógica de negócio e UX rica
3. **Clean Architecture** - Separação clara de responsabilidades  
4. **Fail Fast** - Erros claros melhor que falhas silenciosas
5. **User-Centric** - Feedback rico e sugestões úteis

## 📋 Próximos Passos

Veja arquivos de documentação:
- **[INSTALL.md](INSTALL.md)** - Guia detalhado de instalação
- **[USAGE.md](USAGE.md)** - Manual completo de uso  
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Documentação técnica
- **[.github/copilot-instructions.md](.github/copilot-instructions.md)** - Instruções para GitHub Copilot

## 📄 Licença

Este projeto está sob a licença MIT. Veja [LICENSE](LICENSE) para detalhes.

---

**XKit v2.1** - PowerShell minimal, Python maximal 🚀
- `xkit-ai` - Sugestões inteligentes baseadas no contexto
- `xkit-solve "problema"` - Resolução específica de problemas

### Gerenciamento de Containers
- `compose-up` / `compose-down` - Controle de serviços compose
- `container-status` - Status completo dos containers

## 📦 Estrutura do Projeto

```
WindowsPowerShell/
├── README.md                           # Este arquivo
├── INSTALL.md                          # Guia de instalação
├── USAGE.md                           # Manual de uso
├── ARCHITECTURE.md                    # Documentação técnica
├── CHANGELOG.md                       # Histórico de versões
├── Microsoft.PowerShell_profile.ps1   # Perfil otimizado
├── gh-copilot.ps1                     # GitHub Copilot integration
└── Scripts/
    ├── xkit_compact.py               # ⭐ Aplicação principal
    ├── xkit/                         # 🏗️ Clean Architecture
    │   ├── domain/                   # Entidades de negócio
    │   ├── application/              # Casos de uso
    │   └── infrastructure/           # Implementações
    └── tools/                        # 🔧 Utilitários
        ├── xkit-final-validator.py
        └── test-prompt.py
```

## 🔧 Configuração

### Variáveis de Ambiente Requeridas

Edite `Microsoft.PowerShell_profile.ps1`:

```powershell
# XKit v2.1 AI & Telegram Configuration
$env:GEMINI_API_KEY = 'sua_gemini_api_key'
$env:TELEGRAM_TOKEN = 'seu_telegram_bot_token'  
$env:ADMIN_ID = 'seu_telegram_user_id'
```

### Pré-requisitos

- **Windows 10/11**
- **PowerShell 5.1+**
- **Python 3.11+**
- **Git** (recomendado)
- **Podman ou Docker** (opcional)
- **podman-compose** (opcional)

## 🤖 Funcionalidades AI

### Gemini AI Integration
- Análise contextual inteligente do projeto atual
- Sugestões baseadas em tecnologias detectadas
- Resolução automática de problemas comuns
- Detecção de anomalias no ambiente

### Telegram Notifications
- Alertas automáticos de problemas
- Notificações de anomalias detectadas
- Logs de interações importantes

## 🐳 Container Management

### Detecção Automática
- **Podman** e **Docker** engines
- **podman-compose** v1.5.0+
- **Arquivos compose** no projeto
- **Containers em execução**

### Comandos Simplificados
```powershell
# Controle de serviços
compose-up          # Subir todos os serviços
compose-down        # Parar todos os serviços  
container-status    # Status completo

# Comandos diretos
podman ps           # Listar containers
podman images       # Listar imagens
```

## 🏗️ Arquitetura

O XKit segue **Clean Architecture** com separação clara de responsabilidades:

- **Domain Layer** - Regras de negócio e entidades
- **Application Layer** - Casos de uso e orquestração  
- **Infrastructure Layer** - Implementações concretas

## 📚 Documentação Completa

- **[INSTALL.md](INSTALL.md)** - Guia detalhado de instalação
- **[USAGE.md](USAGE.md)** - Manual completo de uso
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Documentação técnica
- **[CHANGELOG.md](CHANGELOG.md)** - Histórico e roadmap

## 🚀 Performance

- **Carregamento rápido** - Interface responsiva
- **Detecção otimizada** - Cache inteligente
- **Comandos eficientes** - Execução em segundo plano
- **Memoria baixa** - Footprint mínimo

## 🤝 Contribuição

1. **Fork** o repositório
2. **Crie** uma feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add AmazingFeature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)  
5. **Abra** um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

- 📖 **Documentação** - Veja os arquivos .md na raiz
- 🤖 **AI Help** - Use `xkit-ai "sua pergunta"`
- 💬 **Issues** - Abra uma issue no repositório
- 📱 **Telegram** - Configure para receber alertas

---

**XKit v2.1** - Desenvolvido com ❤️ para otimizar seu ambiente Windows de desenvolvimento