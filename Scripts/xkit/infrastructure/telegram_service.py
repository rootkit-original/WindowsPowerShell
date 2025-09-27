"""
Telegram Service - Notificações de anomalias via Telegram
"""
import os
import json
import requests
from typing import Optional, Dict, Any, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from ..domain.entities import DevelopmentContext


class TelegramService:
    """Serviço de notificações via Telegram"""
    
    def __init__(self, token: Optional[str] = None, admin_id: Optional[str] = None):
        self.token = token or os.getenv('TELEGRAM_TOKEN')
        self.admin_id = admin_id or os.getenv('ADMIN_ID')
        self.base_url = f"https://api.telegram.org/bot{self.token}" if self.token else None
        
    def is_available(self) -> bool:
        """Verifica se o serviço está disponível"""
        return bool(self.token and self.admin_id)
    
    def send_anomaly_alert(self, anomalies: Dict[str, Any], project_name: str) -> bool:
        """Envia alerta de anomalias"""
        if not self.is_available() or not anomalies:
            return False
            
        message = self._format_anomaly_message(anomalies, project_name)
        return self._send_message(message)
    
    def send_project_summary(self, context: 'DevelopmentContext') -> bool:
        """Envia resumo do projeto"""
        if not self.is_available():
            return False
            
        message = self._format_project_summary(context)
        return self._send_message(message)
    
    def _format_anomaly_message(self, anomalies: Dict[str, Any], project_name: str) -> str:
        """Formata mensagem de anomalias"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        message = f"🚨 *XKit Alert* - {timestamp}\n"
        message += f"📁 Projeto: `{project_name}`\n\n"
        
        for key, description in anomalies.items():
            if 'many_changes' in key:
                message += f"📝 {description}\n"
            elif 'config' in key:
                message += f"⚠️ {description}\n"
            else:
                message += f"❓ {description}\n"
        
        return message
    
    def _format_project_summary(self, context: 'DevelopmentContext') -> str:
        """Formata resumo do projeto"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        message = f"📊 *XKit Status* - {timestamp}\n"
        message += f"📁 `{context.project.name}`\n"
        
        if context.project.technologies:
            tech_icons = {
                'Python': '🐍', 'Node.js': '📦', 'Docker': '🐳',
                'React': '⚛️', 'TypeScript': '📘', 'Java': '☕'
            }
            
            tech_line = ""
            for tech in context.project.technologies[:3]:  # Max 3 tecnologias
                icon = tech_icons.get(tech, '🛠️')
                tech_line += f"{icon}{tech} "
            
            if tech_line:
                message += f"🛠️ {tech_line.strip()}\n"
        
        if context.is_git_project:
            status = "🟢" if context.git.is_clean else "🟡"
            message += f"🌿 {status} `{context.git.current_branch}`"
            if not context.git.is_clean:
                message += f" ({context.git.changes_count} changes)"
            message += "\n"
        
        if context.has_containers:
            message += f"🐳 {context.container.engine_type.title()}\n"
        
        return message
    
    def _send_message(self, message: str) -> bool:
        """Envia mensagem via Telegram"""
        try:
            if not self.base_url:
                return False
                
            data = {
                'chat_id': self.admin_id,
                'text': message,
                'parse_mode': 'Markdown'
            }
            
            response = requests.post(
                f"{self.base_url}/sendMessage",
                data=data,
                timeout=5
            )
            
            return response.status_code == 200
            
        except Exception:
            return False
    
    def get_bot_info(self) -> Optional[Dict[str, Any]]:
        """Obtém informações do bot"""
        try:
            if not self.base_url:
                return None
                
            response = requests.get(
                f"{self.base_url}/getMe",
                timeout=5
            )
            
            if response.status_code == 200:
                return response.json().get('result', {})
            return None
            
        except Exception:
            return None