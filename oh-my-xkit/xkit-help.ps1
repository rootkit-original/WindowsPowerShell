# XKit Help System
# Comprehensive help for Oh My XKit

function xkit-help {
    param([string]$Topic)
    
    if (-not $Topic) {
        Show-XKitMainHelp
        return
    }
    
    switch ($Topic.ToLower()) {
        "themes" { Show-XKitThemeHelp }
        "plugins" { Show-XKitPluginHelp }
        "git" { Show-GitPluginHelp }
        "docker" { Show-DockerPluginHelp }
        "ai" { Show-AIPluginHelp }
        "telegram" { Show-TelegramPluginHelp }
        "commands" { Show-XKitCommands }
        default {
            Write-Host "❌ Unknown help topic: $Topic" -ForegroundColor Red
            Write-Host "Available topics: themes, plugins, git, docker, ai, telegram, commands" -ForegroundColor Yellow
        }
    }
}

function Show-XKitMainHelp {
    Write-Host ""
    Write-Host "🎨 " -NoNewline -ForegroundColor Blue
    Write-Host "Oh My XKit" -NoNewline -ForegroundColor Green
    Write-Host " - PowerShell Framework" -ForegroundColor Cyan
    Write-Host "======================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📖 Quick Start:" -ForegroundColor Yellow
    Write-Host "  xkit-themes          - List available themes" -ForegroundColor White
    Write-Host "  xkit-plugins         - List available plugins" -ForegroundColor White  
    Write-Host "  xkit-version         - Show version info" -ForegroundColor White
    Write-Host "  xkit-reload          - Reload configuration" -ForegroundColor White
    Write-Host ""
    Write-Host "🎭 Themes:" -ForegroundColor Yellow
    Write-Host "  powerlevel10k-xkit   - Advanced prompt with segments" -ForegroundColor White
    Write-Host "  classic-xkit         - Traditional shell prompt" -ForegroundColor White
    Write-Host "  minimal-xkit         - Clean minimal prompt" -ForegroundColor White
    Write-Host ""
    Write-Host "🔌 Plugins:" -ForegroundColor Yellow
    Write-Host "  git                  - Enhanced git functionality" -ForegroundColor White
    Write-Host "  docker               - Container management" -ForegroundColor White
    Write-Host "  ai-assistant         - AI-powered help" -ForegroundColor White
    Write-Host "  telegram-notifier    - Development notifications" -ForegroundColor White
    Write-Host ""
    Write-Host "📚 Detailed Help:" -ForegroundColor Yellow
    Write-Host "  xkit-help themes     - Theme system help" -ForegroundColor White
    Write-Host "  xkit-help plugins    - Plugin system help" -ForegroundColor White
    Write-Host "  xkit-help git        - Git plugin commands" -ForegroundColor White
    Write-Host "  xkit-help docker     - Docker plugin commands" -ForegroundColor White
    Write-Host "  xkit-help ai         - AI assistant commands" -ForegroundColor White
    Write-Host "  xkit-help telegram   - Telegram notifier commands" -ForegroundColor White
    Write-Host ""
}

function Show-XKitThemeHelp {
    Write-Host "🎭 XKit Theme System" -ForegroundColor Cyan
    Write-Host "====================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📋 Available Themes:" -ForegroundColor Yellow
    Write-Host "  powerlevel10k-xkit   - Advanced multi-segment prompt" -ForegroundColor White
    Write-Host "                       - Shows user, git, containers, python" -ForegroundColor Gray
    Write-Host "  classic-xkit         - Traditional user@host:path format" -ForegroundColor White
    Write-Host "  minimal-xkit         - Ultra-clean directory-focused prompt" -ForegroundColor White
    Write-Host ""
    Write-Host "⚙️  Theme Commands:" -ForegroundColor Yellow
    Write-Host "  xkit-themes          - List all themes with status" -ForegroundColor White
    Write-Host "  Set-XKitTheme name   - Switch to theme" -ForegroundColor White
    Write-Host "  xkit-reload          - Apply theme changes" -ForegroundColor White
    Write-Host ""
    Write-Host "🎨 Creating Custom Themes:" -ForegroundColor Yellow
    Write-Host "  1. Create file: oh-my-xkit/themes/mytheme.ps1" -ForegroundColor White
    Write-Host "  2. Define global:prompt function" -ForegroundColor White
    Write-Host "  3. Set theme metadata variables" -ForegroundColor White
    Write-Host "  4. Use: Set-XKitTheme mytheme" -ForegroundColor White
    Write-Host ""
}

function Show-XKitPluginHelp {
    Write-Host "🔌 XKit Plugin System" -ForegroundColor Cyan
    Write-Host "=====================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📦 Available Plugins:" -ForegroundColor Yellow
    Write-Host "  git                  - Git aliases and enhanced commands" -ForegroundColor White
    Write-Host "  docker               - Docker/Podman container management" -ForegroundColor White
    Write-Host "  ai-assistant         - AI-powered development assistance" -ForegroundColor White
    Write-Host "  telegram-notifier    - Telegram notifications for events" -ForegroundColor White
    Write-Host ""
    Write-Host "⚙️  Plugin Management:" -ForegroundColor Yellow
    Write-Host "  xkit-plugins         - List plugins with status" -ForegroundColor White
    Write-Host "  Edit XKIT_PLUGINS in profile to enable/disable" -ForegroundColor White
    Write-Host ""
    Write-Host "🛠️  Creating Plugins:" -ForegroundColor Yellow
    Write-Host "  1. Create directory: oh-my-xkit/plugins/myplugin/" -ForegroundColor White
    Write-Host "  2. Create file: myplugin.plugin.ps1" -ForegroundColor White
    Write-Host "  3. Add to XKIT_PLUGINS array in profile" -ForegroundColor White
    Write-Host "  4. Reload with: xkit-reload" -ForegroundColor White
    Write-Host ""
}

function Show-GitPluginHelp {
    Write-Host "🌿 Git Plugin Commands" -ForegroundColor Cyan
    Write-Host "======================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📝 Basic Aliases:" -ForegroundColor Yellow
    Write-Host "  gst                  - git status" -ForegroundColor White
    Write-Host "  ga <files>           - git add" -ForegroundColor White
    Write-Host "  gaa                  - git add --all" -ForegroundColor White
    Write-Host "  gcmsg 'message'      - git commit -m" -ForegroundColor White
    Write-Host "  gp                   - git push" -ForegroundColor White
    Write-Host "  gl                   - git pull" -ForegroundColor White
    Write-Host "  gb                   - git branch" -ForegroundColor White
    Write-Host "  gco <branch>         - git checkout" -ForegroundColor White
    Write-Host "  gcb <branch>         - git checkout -b" -ForegroundColor White
    Write-Host "  gd                   - git diff" -ForegroundColor White
    Write-Host "  gds                  - git diff --staged" -ForegroundColor White
    Write-Host "  glog                 - git log --oneline --graph" -ForegroundColor White
    Write-Host ""
    Write-Host "⚡ Advanced Commands:" -ForegroundColor Yellow
    Write-Host "  gqc 'message'        - Quick commit (add all + commit)" -ForegroundColor White
    Write-Host "  gbc                  - Clean merged branches" -ForegroundColor White
    Write-Host "  ginfo                - Repository information" -ForegroundColor White
    Write-Host ""
}

function Show-DockerPluginHelp {
    Write-Host "🐳 Docker Plugin Commands" -ForegroundColor Cyan
    Write-Host "==========================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🚢 Docker Aliases:" -ForegroundColor Yellow
    Write-Host "  d                    - docker" -ForegroundColor White
    Write-Host "  dc                   - docker-compose" -ForegroundColor White
    Write-Host "  dps                  - docker ps" -ForegroundColor White
    Write-Host "  dpsa                 - docker ps -a" -ForegroundColor White
    Write-Host "  di                   - docker images" -ForegroundColor White
    Write-Host "  drun                 - docker run" -ForegroundColor White
    Write-Host "  dexec                - docker exec" -ForegroundColor White
    Write-Host "  dlogs                - docker logs" -ForegroundColor White
    Write-Host ""
    Write-Host "🎣 Podman Aliases:" -ForegroundColor Yellow
    Write-Host "  p                    - podman" -ForegroundColor White
    Write-Host "  pc                   - podman-compose" -ForegroundColor White
    Write-Host "  pps, ppsa, pi, etc   - podman equivalents" -ForegroundColor White
    Write-Host ""
    Write-Host "🧹 Management:" -ForegroundColor Yellow
    Write-Host "  dclean               - Docker cleanup (containers, images, volumes)" -ForegroundColor White
    Write-Host "  pclean               - Podman cleanup" -ForegroundColor White
    Write-Host "  cinfo                - Container environment info" -ForegroundColor White
    Write-Host "  dqr image            - Quick run container" -ForegroundColor White
    Write-Host ""
}

function Show-AIPluginHelp {
    Write-Host "🤖 AI Assistant Commands" -ForegroundColor Cyan
    Write-Host "=========================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "💬 Basic Commands:" -ForegroundColor Yellow
    Write-Host "  ai 'question'        - Ask AI a question" -ForegroundColor White
    Write-Host "  ai-help 'question'   - Same as ai" -ForegroundColor White
    Write-Host "  ai-status            - Check AI service status" -ForegroundColor White
    Write-Host ""
    Write-Host "🔍 Code Analysis:" -ForegroundColor Yellow
    Write-Host "  aicode file.py       - Analyze code file" -ForegroundColor White
    Write-Host "  ai-analyze-code file - Same as aicode" -ForegroundColor White
    Write-Host ""
    Write-Host "🐛 Error Help:" -ForegroundColor Yellow
    Write-Host "  aierror 'message'    - Explain error and suggest fixes" -ForegroundColor White
    Write-Host "  aierror              - Use last PowerShell error" -ForegroundColor White
    Write-Host ""
    Write-Host "💡 Command Suggestions:" -ForegroundColor Yellow
    Write-Host "  aicmd 'task'         - Get command suggestions" -ForegroundColor White
    Write-Host "  ai-suggest-command   - Same as aicmd" -ForegroundColor White
    Write-Host ""
    Write-Host "📝 Examples:" -ForegroundColor Yellow
    Write-Host "  ai 'how to merge git branches'" -ForegroundColor Gray
    Write-Host "  aicode script.ps1" -ForegroundColor Gray
    Write-Host "  aierror 'permission denied'" -ForegroundColor Gray
    Write-Host "  aicmd 'list all python processes'" -ForegroundColor Gray
    Write-Host ""
}

function Show-TelegramPluginHelp {
    Write-Host "📱 Telegram Notifier Commands" -ForegroundColor Cyan
    Write-Host "==============================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📢 Basic Notifications:" -ForegroundColor Yellow
    Write-Host "  tg 'message'         - Send custom notification" -ForegroundColor White
    Write-Host "  telegram-notify      - Same as tg" -ForegroundColor White
    Write-Host "  telegram-status      - Check service status" -ForegroundColor White
    Write-Host ""
    Write-Host "🏗️  Build Notifications:" -ForegroundColor Yellow
    Write-Host "  tgbuild success      - Build successful" -ForegroundColor White
    Write-Host "  tgbuild failure      - Build failed" -ForegroundColor White
    Write-Host "  tgbuild started      - Build started" -ForegroundColor White
    Write-Host ""
    Write-Host "🚀 Deployment Notifications:" -ForegroundColor Yellow
    Write-Host "  tgdeploy success     - Deployment successful" -ForegroundColor White
    Write-Host "  tgdeploy failure     - Deployment failed" -ForegroundColor White
    Write-Host "  tgdeploy started     - Deployment started" -ForegroundColor White
    Write-Host ""
    Write-Host "🚨 Error Alerts:" -ForegroundColor Yellow
    Write-Host "  tgerror 'message'    - Send error alert" -ForegroundColor White
    Write-Host "  telegram-error-alert - Same as tgerror" -ForegroundColor White
    Write-Host ""
    Write-Host "🌿 Git Integration:" -ForegroundColor Yellow
    Write-Host "  telegram-git-push    - Notify git push (auto)" -ForegroundColor White
    Write-Host "  Enable-AutoNotifications - Auto-notify on git push" -ForegroundColor White
    Write-Host ""
}

function Show-XKitCommands {
    Write-Host "⚡ All XKit Commands" -ForegroundColor Cyan
    Write-Host "===================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🔧 Core Commands:" -ForegroundColor Yellow
    Write-Host "  xkit-version         - Show version" -ForegroundColor White
    Write-Host "  xkit-reload          - Reload configuration" -ForegroundColor White
    Write-Host "  xkit-help [topic]    - Show help" -ForegroundColor White
    Write-Host "  xkit-themes          - List themes" -ForegroundColor White
    Write-Host "  xkit-plugins         - List plugins" -ForegroundColor White
    Write-Host "  Set-XKitTheme name   - Change theme" -ForegroundColor White
    Write-Host ""
    Write-Host "🌿 Git (when plugin enabled):" -ForegroundColor Yellow
    Write-Host "  gst, ga, gaa, gp, gl, gb, gco, gcb, gd, gds, glog" -ForegroundColor White
    Write-Host "  gqc, gbc, ginfo" -ForegroundColor White
    Write-Host ""
    Write-Host "🐳 Docker (when plugin enabled):" -ForegroundColor Yellow
    Write-Host "  d, dc, dps, dpsa, di, drun, dexec, dlogs" -ForegroundColor White
    Write-Host "  p, pc, pps, ppsa, pi, prun, pexec, plogs" -ForegroundColor White
    Write-Host "  dclean, pclean, cinfo, dqr" -ForegroundColor White
    Write-Host ""
    Write-Host "🤖 AI (when plugin enabled):" -ForegroundColor Yellow
    Write-Host "  ai, aicode, aierror, aicmd, ai-status" -ForegroundColor White
    Write-Host ""
    Write-Host "📱 Telegram (when plugin enabled):" -ForegroundColor Yellow
    Write-Host "  tg, tgbuild, tgdeploy, tgerror, telegram-status" -ForegroundColor White
    Write-Host ""
}

# Export the help function
New-Alias -Name "xkit-help" -Value "xkit-help" -Force -Scope Global

Write-Verbose "✅ Loaded XKit help system"