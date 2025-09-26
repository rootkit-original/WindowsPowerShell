# 📖 Guia de Instalação - XKit v2.1

> **Instruções passo-a-passo para instalar o XKit v2.1 no Windows**

## 🚦 Pré-requisitos

- **Windows 10/11**
- **PowerShell 5.1+** (já incluído no Windows)
- **Python 3.8+** ([Download aqui](https://python.org))
- **Git** ([Download aqui](https://git-scm.com))

## 🚀 Instalação Rápida

```powershell
# 1. Clone o repositório
git clone https://github.com/user/xkit.git "$env:USERPROFILE\Documents\WindowsPowerShell"

# 2. Execute o setup
cd "$env:USERPROFILE\Documents\WindowsPowerShell"
python Scripts\xkit-setup.py

# 3. Reinicie o PowerShell
```

## ✅ Verificação

```powershell
# Teste se está funcionando
xkit-version
xkit-help
xstatus
```

## 🔧 Configurações Opcionais

### Integração Telegram + AI

```powershell
# Adicionar ao profile (opcional)
$env:GEMINI_API_KEY = "sua-chave-gemini"
$env:TELEGRAM_TOKEN = "seu-token-telegram"
$env:ADMIN_ID = "seu-telegram-id"
```

### Container Support

```powershell
# Podman (recomendado)
winget install -e --id RedHat.Podman

# Ou Docker
winget install -e --id Docker.DockerDesktop
```

## 🔍 Troubleshooting

### Execution Policy
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Python não encontrado
```powershell
python --version
```

### Profile não carrega
```powershell
. $PROFILE
xkit-reload
```

## 🔄 Atualização

```powershell
cd "$env:USERPROFILE\Documents\WindowsPowerShell"
git pull origin main
xkit-reload
```

---

**Pronto! Seu ambiente XKit está configurado! 🎉**