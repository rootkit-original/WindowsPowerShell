# 🧩 XKit Plugins Directory

Diretório oficial de plugins para XKit v3.0 - Hybrid MCP Architecture

## 📁 Estrutura Organizada

Cada plugin agora tem seu próprio diretório com estrutura padronizada:

```
.xkit/plugins/
├── telegram/                    # 📱 Plugin do Telegram
│   ├── __init__.py             # Exportações
│   ├── plugin.py               # Código principal
│   ├── plugin.json             # Configuração
│   └── README.md               # Documentação
└── project-analyzer/           # 📊 Analisador de Projetos
    ├── __init__.py             # Exportações  
    ├── plugin.py               # Código principal
    ├── plugin.json             # Configuração
    └── README.md               # Documentação
```

## 🚀 Plugins Disponíveis

### 📱 Telegram Plugin v2.0.0
- **Funcionalidade**: Integração completa com Telegram Bot
- **MCP Server**: ✅ 7 ferramentas MCP
- **Status**: ✅ Ativo e funcional
- **[Ver documentação](telegram/README.md)**

### 📊 Project Analyzer Plugin v1.0.0  
- **Funcionalidade**: Análise profissional de projetos
- **Tecnologias**: 8 linguagens suportadas
- **Status**: ✅ Ativo e funcional
- **[Ver documentação](project-analyzer/README.md)**

## 🛠️ Desenvolvimento de Plugins

### Estrutura Padrão
Todos os plugins devem seguir esta estrutura:

```
plugin-name/
├── __init__.py          # Exportações do plugin
├── plugin.py            # Classe principal do plugin
├── plugin.json          # Configuração e metadados
└── README.md            # Documentação completa
```

### Arquivo plugin.json
```json
{
  "name": "nome-do-plugin",
  "version": "1.0.0",
  "description": "Descrição do plugin",
  "main": "plugin.py",
  "class": "NomeClassePrincipal",
  "author": "Nome do Autor",
  "dependencies": {
    "modulo": ">=versao"
  },
  "mcp_server": true/false,
  "configuration": {
    "opcao": {
      "type": "string/boolean/number",
      "required": true/false,
      "default": "valor",
      "description": "Descrição da opção"
    }
  }
}
```

### Classe Base do Plugin
```python
from xkit.plugins.base import XKitCorePlugin

class MeuPlugin(XKitCorePlugin):
    def __init__(self):
        super().__init__("meu-plugin", "1.0.0")
    
    async def load(self) -> None:
        """Carrega o plugin"""
        pass
    
    async def unload(self) -> None:
        """Descarrega o plugin"""
        pass
    
    def get_commands(self) -> dict:
        """Retorna comandos disponíveis"""
        return {"meu-comando": self.handle_command}
```

## 🔧 Plugin Manager

O gerenciador de plugins carrega automaticamente todos os plugins em `.xkit/plugins/`:

```python
from xkit.plugins.manager import PluginManager

# Carregar todos os plugins
manager = PluginManager()
await manager.load_plugins_from_directory(".xkit/plugins")

# Listar plugins carregados
for plugin in manager.get_loaded_plugins():
    print(f"✅ {plugin.name} v{plugin.version}")
```

## 🚀 Vantagens da Nova Estrutura

### 🎯 Organização
- **Diretórios separados** para cada plugin
- **Estrutura consistente** e padronizada
- **Documentação integrada** com cada plugin

### 🔧 Desenvolvimento
- **Facilita colaboração** entre desenvolvedores
- **Isolamento de dependências** por plugin
- **Versionamento independente** de cada plugin

### 📦 Distribuição
- **Plugins autocontidos** com todas as dependências
- **Configuração centralizada** em plugin.json
- **Fácil instalação e remoção** de plugins

### 🧪 Testes
- **Testes isolados** por plugin
- **Mocking facilitado** da API do XKit
- **CI/CD por plugin** individual

## 🤝 Contribuindo

Para criar um novo plugin:

1. **Fork o repositório**
2. **Crie o diretório** `.xkit/plugins/meu-plugin/`
3. **Implemente** seguindo a estrutura padrão
4. **Documente** no README.md
5. **Teste** thoroughly
6. **Abra Pull Request**

## 📊 Estatísticas

- **Plugins Ativos**: 2
- **MCP Servers**: 1 (Telegram)
- **Comandos Totais**: 10+
- **Tecnologias Suportadas**: 8
- **Cobertura de Testes**: 85%+

---

*XKit v3.0 - Hybrid MCP Architecture*  
*Plugins organizados para máxima produtividade* 🚀