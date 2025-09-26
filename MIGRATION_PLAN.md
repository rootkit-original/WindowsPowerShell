# MIGRATION_PLAN.md

## 📋 Fases da Migração

### Fase 1: MCP Core (Semana 1)
- [ ] Implementar MCPClient base
- [ ] Criar adaptadores para servers existentes
- [ ] Migrar comandos atuais para usar MCP
- [ ] Testes de integração

### Fase 2: Plugin System (Semana 2)
- [ ] Converter módulos atuais em plugins
- [ ] Implementar PluginManager
- [ ] Sistema de descoberta automática
- [ ] Hot-reload de plugins

### Fase 3: Event System (Semana 3)
- [ ] Implementar EventBus central
- [ ] Migrar notificações para eventos
- [ ] Adicionar handlers assíncronos
- [ ] Sistema de replay de eventos

### Fase 4: Hexagonal Ports (Semana 4)
- [ ] Definir ports/adapters
- [ ] Migrar infraestrutura
- [ ] Implementar DI container
- [ ] Documentar contratos