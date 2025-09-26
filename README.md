# XKit v2.1 - Kit de Desenvolvimento Windows Inteligente

[![PowerShell](https://img.shields.io/badge/PowerShell-5.1+-blue.svg)](https://docs.microsoft.com/en-us/powershell/)
[![Python](https://img.shields.io/badge/Python-3.11+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Sistema inteligente de desenvolvimento Windows com AI e interface compacta estilo oh-my-zsh**

## 🎯 Visão Geral

O XKit v2.1 é um sistema completo para otimização do ambiente de desenvolvimento Windows, oferecendo:

- **🎨 Interface compacta** estilo oh-my-zsh com informações contextuais
- **🤖 Integração com Gemini AI** para decisões inteligentes e resolução de problemas  
- **📱 Notificações Telegram** para detecção de anomalias
- **🐳 Suporte completo** a Podman/Docker e podman-compose
- **⚡ Prompt personalizado** estilo bash/zsh
- **🏗️ Clean Architecture** mantendo código organizado e escalável

## 🚀 Interface em Ação

### Prompt Personalizado
```bash
Usuario@DESKTOP-II8D8DC [main] ~/Documents/WindowsPowerShell
$ 
```

### Interface Ultra-Compacta
```bash
🪟 📁WindowsPowerShell 🌿main ✓ 🐳podman 🐍💙
📦 compose: podman-compose v1.5.0  
🤖 AI suggestions • 📱 Telegram alerts
💡 xkit-help para comandos
```

## ⚡ Início Rápido

1. **Clone** este repositório para `$HOME\Documents\WindowsPowerShell`
2. **Configure** suas API keys no perfil PowerShell
3. **Reinicie** o PowerShell
4. **Digite** `xkit-help` para começar

## 🎯 Comandos Principais

### Interface e Informações
- `xkit-help` - Lista todos os comandos disponíveis
- `xkit-status` - Status detalhado do ambiente
- `xkit-info` - Informações do projeto atual

### Inteligência Artificial
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