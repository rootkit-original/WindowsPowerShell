# XKit Tests Directory

Este diretório contém todos os testes para validar as funcionalidades do XKit v3.0.

## 📋 Testes Disponíveis

### 🤖 AI Integration Tests
- **`test_gemini_fixed.py`** - Testa integração com API do Google Gemini
  - Valida chaves de API
  - Testa diferentes modelos (gemini-pro, gemini-1.5-flash, etc.)
  - Verifica diferentes versões da API (v1, v1beta)

### 📱 Telegram Integration Tests  
- **`test_telegram.py`** - Teste básico do Telegram Bot
  - Verifica configuração do bot
  - Testa envio de mensagens simples
  - Validação de token e chat_id

- **`test_telegram_mcp.py`** - Teste completo do MCP Telegram Server
  - Testa integração MCP-Telegram
  - Validação de todas as ferramentas MCP
  - Teste de comandos remotos (/analyze, /status, /git)
  - Relatórios de projetos via MCP

## 🚀 Como Executar os Testes

### Pré-requisitos
1. **XKit v3.0** instalado e configurado
2. **Configuração completa** em `~/.xkit/config.json`:
   ```json
   {
     "ai": {
       "gemini": {
         "api_key": "SUA_CHAVE_GEMINI"
       }
     },
     "telegram": {
       "enabled": true,
       "token": "SEU_BOT_TOKEN",
       "admin_id": "SEU_CHAT_ID"
     }
   }
   ```

### Executando Testes Individuais

#### Teste do Gemini AI
```powershell
cd tests
python test_gemini_fixed.py
```

#### Teste Básico do Telegram
```powershell
cd tests  
python test_telegram.py
```

#### Teste Completo do MCP Telegram
```powershell
cd tests
python test_telegram_mcp.py
```

## 📊 Estrutura dos Testes

### test_gemini_fixed.py
- ✅ Validação de chave de API
- ✅ Teste de diferentes modelos
- ✅ Verificação de versões da API
- ✅ Teste de geração de conteúdo
- ✅ Relatório detalhado de compatibilidade

### test_telegram.py
- ✅ Verificação de configuração
- ✅ Teste de conectividade
- ✅ Validação de bot token
- ✅ Teste de envio de mensagem
- ✅ Verificação de permissões

### test_telegram_mcp.py
- ✅ Disponibilidade do MCP Server
- ✅ Listagem de ferramentas MCP
- ✅ Informações do bot
- ✅ Envio de mensagens via MCP
- ✅ Relatórios de projeto
- ✅ Status do sistema
- ✅ Status Git
- ✅ Processamento de comandos

## 🔧 Configuração de Desenvolvimento

### Para Desenvolvedores
1. **Clone o repositório**
2. **Configure as variáveis de ambiente**:
   ```powershell
   $env:XKIT_CONFIG_PATH = "~/.xkit/config.json"
   $env:PYTHONPATH = "$PWD/Scripts"
   ```
3. **Execute os testes** para validar o ambiente

### Adicionando Novos Testes
1. Crie arquivos seguindo o padrão `test_*.py`
2. Use a estrutura de classes para organizar testes
3. Implemente métodos `async` para testes assíncronos
4. Adicione logging detalhado para debugging
5. Inclua validação de configuração

## 📈 Resultados Esperados

### ✅ Teste Bem-Sucedido
- Todos os testes passam
- Conexões estabelecidas com sucesso
- Mensagens enviadas corretamente
- APIs respondem adequadamente

### ⚠️ Teste com Avisos
- Configuração parcial (algumas funcionalidades desabilitadas)
- APIs com limitações temporárias
- Testes pulados por falta de credenciais

### ❌ Teste Falhando
- Configuração incorreta
- Credenciais inválidas  
- Problemas de conectividade
- Erros de código

## 🐛 Debugging

### Logs Detalhados
Os testes geram logs detalhados para facilitar debugging:
```
🚀 Iniciando testes do MCP Telegram Server...
📡 Teste 1: Disponibilidade do Servidor
✅ Servidor 'telegram-bot' encontrado
🛠️ Teste 2: Listagem de Ferramentas  
✅ 7 ferramentas encontradas
```

### Arquivos de Configuração
Verifique sempre:
- `~/.xkit/config.json` - Configuração principal
- `Scripts/xkit/mcp/config.json` - Configuração MCP
- `Scripts/xkit/config/config.example.json` - Exemplo de configuração

## 📚 Documentação Relacionada

- [API Documentation](../docs/api/) - Documentação completa das APIs
- [MCP Protocol](../docs/api/mcp-protocol.md) - Protocolo MCP detalhado
- [Plugin Development](../docs/development/plugin-development.md) - Desenvolvimento de plugins
- [Telegram Plugin](../docs/plugins/telegram-plugin.md) - Plugin Telegram

## 🎯 Objetivos dos Testes

1. **Validação de Integração** - Verificar se todas as integrações funcionam
2. **Qualidade de Código** - Garantir que o código funciona conforme esperado
3. **Debugging Facilitated** - Fornecer informações para solução de problemas
4. **Documentação Viva** - Exemplos práticos de como usar as APIs
5. **Regression Testing** - Evitar quebras em funcionalidades existentes

---

**XKit v3.0** - Hybrid MCP Architecture  
🚀 Desenvolvido com ❤️ para desenvolvedores