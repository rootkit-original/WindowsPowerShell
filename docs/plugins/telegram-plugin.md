# 🤖 XKit Telegram Plugin

Plugin para integração com Telegram Bot que permite receber notificações automáticas sobre análises de projetos `.xkit` e outras atividades do framework.

## ✨ Funcionalidades

- 📊 **Notificações de Análise**: Receba relatórios automáticos quando projetos `.xkit` são analisados
- 🚨 **Alertas de Anomalias**: Seja notificado sobre anomalias detectadas em projetos
- 🚀 **Status de Inicialização**: Confirme quando o XKit e plugins são carregados
- 🧪 **Testes de Conectividade**: Verifique se o bot está funcionando

## 🛠️ Configuração

### 1. Criar Bot no Telegram

1. Converse com [@BotFather](https://t.me/BotFather) no Telegram
2. Use o comando `/newbot` 
3. Escolha um nome e username para seu bot
4. **Copie o token** fornecido (formato: `1234567890:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`)

### 2. Obter Chat ID

1. Envie uma mensagem qualquer para seu bot
2. Acesse: `https://api.telegram.org/bot<SEU_TOKEN>/getUpdates` 
3. Procure por `"from": {"id": 123456789}` 
4. **Copie o número ID**

### 3. Configurar XKit

Edite o arquivo `~/.xkit/config.json`:

```json
{
  "telegram": {
    "enabled": true,
    "token": "SEU_BOT_TOKEN_AQUI",
    "admin_id": "SEU_CHAT_ID_AQUI",
    "notifications": {
      "project_analysis": true,
      "anomalies": true, 
      "startup": true
    }
  }
}
```

### 4. Testar Configuração

```bash
# Verificar status
xkit telegram-status

# Enviar mensagem de teste  
xkit telegram-test

# Ver configuração atual
xkit telegram-config
```

## 📱 Tipos de Notificações

### 📊 Análise de Projeto
Enviado quando um projeto `.xkit` é analisado:

```
📊 Análise XKit Concluída

📁 Projeto: meu-projeto
🟢 Qualidade: 8.5/10

📈 Métricas:
• Arquivos: 45
• Documentação: ✅
• Git: ✅

🛠️ #python #docker #typescript
```

### 🚨 Alerta de Anomalias
Enviado quando anomalias são detectadas:

```
🚨 XKit Alert - 14:30:25
📁 Projeto: projeto-problematico

📝 Muitas mudanças não commitadas (15 files)
⚠️ Configuração docker modificada
❓ Dependências desatualizadas detectadas
```

### 🚀 Status de Inicialização
Enviado quando o plugin é carregado:

```
🚀 XKit Plugin Telegram Ativo

✅ Bot conectado e monitorando projetos .xkit
📊 Relatórios de análise serão enviados automaticamente
```

## 🧩 Integração com Outros Plugins

O plugin Telegram usa o sistema de eventos do XKit para receber notificações:

```python
# Exemplo: Enviar notificação customizada
from xkit.events.events import PluginEvent

event = PluginEvent(
    plugin_name="meu_plugin",
    event_type="custom_notification", 
    data={"message": "Algo importante aconteceu!"}
)

# Plugin Telegram automaticamente processa eventos conhecidos
```

## 🔧 Comandos Disponíveis

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `telegram-status` | Verifica conectividade | `xkit telegram-status` |
| `telegram-test` | Envia mensagem de teste | `xkit telegram-test` |  
| `telegram-config` | Mostra configuração atual | `xkit telegram-config` |

## 📋 Eventos Suportados

| Evento | Descrição | Dados |
|--------|-----------|-------|
| `project_analyzed` | Análise de projeto concluída | `analysis`, `project_path` |
| `anomalies_detected` | Anomalias encontradas | `anomalies`, `project_name` |
| `startup_completed` | XKit inicializado | `plugins_loaded`, `startup_time` |

## 🚫 Desabilitando Notificações

Para desabilitar temporariamente:

```json
{
  "telegram": {
    "enabled": false
  }
}
```

Para desabilitar tipos específicos:

```json
{
  "telegram": {
    "notifications": {
      "project_analysis": false,
      "anomalies": true,
      "startup": false
    }
  }
}
```

## 🐛 Resolução de Problemas

### Bot não responde
- ✅ Verifique se o token está correto
- ✅ Confirme que o bot não foi excluído no @BotFather
- ✅ Teste `xkit telegram-status`

### Não recebo notificações
- ✅ Verifique se `enabled: true` 
- ✅ Confirme o `admin_id` correto
- ✅ Veja se as notificações específicas estão habilitadas

### Erro de conectividade
- ✅ Verifique conexão com internet
- ✅ Teste `xkit telegram-test`
- ✅ Confirme que não há firewall bloqueando

## 🎯 Propaganda XKit

> 🚀 **XKit v3.0** - Framework PowerShell com Hybrid MCP Architecture  
> 🎨 Oh-my-zsh inspired para Windows  
> 🤖 AI-powered error handling  
> 🔌 MCP integration  
> 🧩 Plugin System com hot-reload  
> 📡 Event-Driven Architecture  
>
> ⭐ [GitHub](https://github.com/rootkit-original/WindowsPowerShell) | 📖 [Docs](./docs/) | 🛠️ [Contribuir](./CONTRIBUTING.md)

---

**Dica**: Configure notificações personalizadas criando seus próprios eventos e usando o sistema de plugins do XKit! 🎨