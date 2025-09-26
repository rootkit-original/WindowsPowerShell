# 🤝 Como Contribuir - XKit v2.1

## 📜 Diretrizes

### 🌿 Branches
- `main` - produção estável
- `develop` - desenvolvimento
- `feature/*` - novas funcionalidades

### 📝 Commits
Use convenções do Conventional Commits:
```
feat: adicionar novo comando xdeploy
fix: corrigir error handling no xstatus
docs: atualizar README com novos comandos
```

### 🏧 Arquitetura
- **PowerShell**: Apenas ponte minimal
- **Python**: Toda lógica de negócio
- **Clean Architecture**: Domain/Application/Infrastructure

### ✅ Pull Requests
1. Fork o repositório
2. Crie branch feature
3. Implemente com testes
4. Abra PR com descrição clara

### 🐛 Issues
Reporte bugs com:
- Versão do XKit
- Sistema operacional
- Passos para reproduzir
- Saída esperada vs atual