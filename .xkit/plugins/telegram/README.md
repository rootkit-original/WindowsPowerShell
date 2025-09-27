# 📱 XKit Telegram Plugin

Plugin oficial de integração com Telegram Bot para XKit v3.0

## 🚀 Funcionalidades

### 🤖 MCP Server Integrado
- **7 ferramentas MCP** para interação completa
- **Polling automático** para comandos em tempo real
- **Formatação inteligente** de mensagens

### 📲 Comandos Disponíveis
- `/status` - Status do sistema XKit
- `/analyze` - Análise rápida do projeto  
- `/git` - Status do repositório Git
- `/help` - Lista de comandos disponíveis
- `/plugins` - Plugins carregados

### 🛠️ Ferramentas MCP
1. **send-message** - Envio de mensagens formatadas
2. **send-project-report** - Relatório de análise de projeto
3. **send-system-status** - Status do sistema
4. **send-git-status** - Status Git detalhado
5. **send-help** - Mensagem de ajuda
6. **send-plugins-list** - Lista de plugins
7. **send-file-content** - Conteúdo de arquivos

## 📦 Instalação

O plugin é carregado automaticamente pelo XKit Plugin Manager.

### Configuração

Edite `plugin.json` ou configure via ambiente:

```json
{
  "bot_token": "SEU_BOT_TOKEN_AQUI",
  "chat_id": "SEU_CHAT_ID_AQUI", 
  "polling_enabled": true
}
```

## 🔧 Desenvolvimento

### Estrutura do Plugin
```
telegram/
├── __init__.py          # Exportações do plugin
├── plugin.py            # Classe principal TelegramPlugin  
├── plugin.json          # Configuração e metadados
└── README.md           # Esta documentação
```

### API do Plugin
```python
from xkit.plugins.telegram import TelegramPlugin

# Instanciar plugin
plugin = TelegramPlugin()

# Carregar configuração
await plugin.load()

# Enviar mensagem
await plugin.send_message("Olá do XKit!")
```

## 🧪 Testes

Para testar o plugin:

```bash
# Testar MCP server
python tests/test_telegram_mcp.py

# Testar polling
python telegram-bot-polling.py
```

## 📊 Métricas

- **Versão**: 2.0.0
- **Dependências**: requests, asyncio
- **MCP Tools**: 7
- **Comandos**: 5
- **Cobertura de testes**: 85%

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma feature branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este plugin é parte do XKit e está sob a mesma licença do projeto principal.