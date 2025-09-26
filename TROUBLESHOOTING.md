# 🚑 Troubleshooting - XKit v2.1

## 🔍 Problemas Comuns

### Comandos não funcionam

**Problema**: `xstatus: CommandNotFoundException`

**Solução**:
```powershell
# Recarregar profile
. $PROFILE
xkit-reload
```

### Python não encontrado

**Problema**: `python: O termo não é reconhecido`

**Solução**:
```powershell
# Verificar instalação
python --version
py --version

# Adicionar ao PATH se necessário
```

### Execution Policy

**Problema**: `Execution Policy` bloqueando scripts

**Solução**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Emojis não aparecem

**Problema**: Caracteres estranhos ao invés de emojis

**Solução**:
```powershell
# O XKit já configura UTF-8, mas se não funcionar:
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001
```

### Profile não carrega

**Problema**: XKit não aparece ao abrir PowerShell

**Solução**:
```powershell
# Verificar se profile existe
Test-Path $PROFILE

# Ver conteúdo
Get-Content $PROFILE

# Recriar se necessário
```

## 🎆 Suporte

1. 📝 Consulte a documentação completa
2. 🐛 Abra issue no GitHub
3. 💬 Use GitHub Discussions
4. 🤖 Teste com `xtest-error`