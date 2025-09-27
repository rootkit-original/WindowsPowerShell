# 🚀 XKit AutoStart System

Sistema de inicialização automática do XKit v3.0 com notificações Telegram.

## ⚡ Instalação Rápida

```powershell
# 1. Execute o instalador
.\install-autostart.ps1

# 2. Teste (opcional)
.\xkit-startup.ps1
```

## 🎯 O que faz?

### 🌅 **Na inicialização do Windows:**
1. **Carrega automaticamente** o PowerShell com profile XKit
2. **Envia notificação** para Telegram com informações do sistema
3. **Registra logs** da execução
4. **Execução silenciosa** (sem janela visível)

### 📱 **Mensagem Telegram típica:**
```
🌅 Windows Iniciado com XKit
⏰ 26/09/2025 08:30:15
💻 MEU-PC | 👤 Usuario
🚀 XKit v3.0 | 🏗️ Hybrid MCP Architecture  
📊 Memória: 25.4MB
```

## 🔧 Métodos de Configuração

### 1. **Task Scheduler** (Recomendado)
- ✅ **Confiável** - Executa mesmo se usuário não logado
- ✅ **Configurável** - Horários, condições, etc.
- ✅ **Logs** - Windows mantém histórico de execução
- ✅ **Permissões** - Executa com privilégios do usuário

### 2. **Registry Run Key** (Backup)
- ✅ **Simples** - Executa no login do usuário
- ⚠️ **Limitado** - Só funciona com login interativo
- ✅ **Compatível** - Funciona em todas as versões do Windows

## 📂 Arquivos Criados

```
WindowsPowerShell/
├── install-autostart.ps1      # 🚀 Instalador principal
├── uninstall-autostart.ps1    # 🗑️ Desinstalador
├── xkit-startup.ps1           # 📜 Script executado na startup
├── xkit-autostart-config.ps1  # 🔧 Configurador avançado  
└── logs/
    └── startup.log            # 📋 Log das execuções
```

## 🎛️ Comandos Úteis

### **Verificar Status:**
```powershell
# Via Task Scheduler
Get-ScheduledTask -TaskName "XKit-PowerShell-AutoStart"

# Via Registry  
Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name "XKit-AutoStart"

# Logs
Get-Content "logs\startup.log" | Select-Object -Last 10
```

### **Testar Manualmente:**
```powershell
# Executar script de startup
.\xkit-startup.ps1

# Testar notificação
xkit-notify "Teste manual do XKit"
```

### **Gerenciar:**
```powershell
# Configurador avançado
.\xkit-autostart-config.ps1 -Status
.\xkit-autostart-config.ps1 -Install  
.\xkit-autostart-config.ps1 -Uninstall
```

## 🔧 Configuração Telegram

### **Variáveis Necessárias:**
No `Microsoft.PowerShell_profile.ps1`:
```powershell
$env:TELEGRAM_TOKEN = 'SEU_BOT_TOKEN'
$env:ADMIN_ID = 'SEU_CHAT_ID'
```

### **Como obter:**
1. **Bot Token:** Falar com @BotFather no Telegram
2. **Chat ID:** Falar com @userinfobot ou usar @RawDataBot

### **Testar Telegram:**
```powershell  
Send-XKitTelegramNotification "Teste do XKit!"
```

## 🛠️ Troubleshooting

### **❌ Não está executando na startup**
```powershell
# Verificar tarefa
Get-ScheduledTask -TaskName "XKit-PowerShell-AutoStart" | fl

# Verificar registry
Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name "XKit-AutoStart"

# Verificar logs
Get-Content "logs\startup.log"
```

### **📱 Telegram não funciona**
```powershell
# Testar variáveis
$env:TELEGRAM_TOKEN
$env:ADMIN_ID

# Testar função
Send-XKitTelegramNotification "Teste"

# Verificar conectividade
Test-NetConnection api.telegram.org -Port 443
```

### **🐌 Startup lento**
- Mover configuração para Task Scheduler com delay
- Usar `-WindowStyle Hidden` para execução silenciosa
- Verificar dependências do profile

### **🔒 Problemas de Permissão**
```powershell
# Executar como Administrador se necessário
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Verificar permissões da tarefa
Get-ScheduledTask -TaskName "XKit-PowerShell-AutoStart" | Get-ScheduledTaskInfo
```

## 📊 Monitoramento

### **Logs de Execução:**
```powershell
# Ver execuções recentes
Get-Content "logs\startup.log" | Select-Object -Last 20

# Contar execuções 
(Get-Content "logs\startup.log").Count

# Filtrar por data
Get-Content "logs\startup.log" | Where-Object { $_ -match "2025-09-26" }
```

### **Performance:**
```powershell
# Tempo de execução típico: ~2-3 segundos
# Memória: ~25-50MB
# CPU: Minimal impact após inicialização
```

## 🗑️ Remoção Completa

```powershell
# Executar desinstalador
.\uninstall-autostart.ps1

# Ou manualmente:
Unregister-ScheduledTask -TaskName "XKit-PowerShell-AutoStart" -Confirm:$false
Remove-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name "XKit-AutoStart"
```

## 🔄 Atualizações

O sistema é **automático** - se você atualizar o profile do PowerShell, as mudanças serão refletidas na próxima inicialização.

## 💡 Dicas Avançadas

### **Execução Condicional:**
Edite `xkit-startup.ps1` para adicionar condições:
```powershell
# Só executar em dias úteis
if ((Get-Date).DayOfWeek -in @('Saturday','Sunday')) { return }

# Só executar em determinados horários
if ((Get-Date).Hour -lt 6 -or (Get-Date).Hour -gt 22) { return }

# Só executar se conectado na rede
if (-not (Test-NetConnection google.com -InformationLevel Quiet)) { return }
```

### **Notificações Personalizadas:**
```powershell
# Adicionar informações do sistema
$SystemInfo = Get-ComputerInfo | Select-Object TotalPhysicalMemory, CsProcessors

# Adicionar clima (se tiver API)
$Weather = Invoke-RestMethod "https://api.weather.com/..."

# Adicionar status de rede
$NetworkStatus = Test-NetConnection -InformationLevel Detailed
```

---

**🎉 Com isso, seu XKit v3.0 será carregado automaticamente toda vez que o Windows iniciar, e você receberá uma notificação no Telegram!**