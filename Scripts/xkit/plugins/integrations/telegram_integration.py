"""
Integração entre Project Analyzer e Telegram Plugin
"""
from typing import Dict, Any, Optional
from ...events.events import PluginEvent


class ProjectAnalyzerTelegramIntegration:
    """Classe para integrar análise de projetos com notificações Telegram"""
    
    def __init__(self, project_analyzer_plugin, telegram_plugin=None):
        self.project_analyzer = project_analyzer_plugin
        self.telegram_plugin = telegram_plugin
        
    def set_telegram_plugin(self, telegram_plugin):
        """Define o plugin do Telegram"""
        self.telegram_plugin = telegram_plugin
    
    async def notify_analysis_completed(self, analysis_result: Dict[str, Any]) -> bool:
        """Notifica quando uma análise é completada"""
        if not self.telegram_plugin:
            return False
            
        # Cria evento de análise completada
        event_data = {
            "analysis": analysis_result,
            "project_path": analysis_result.get("path", ""),
            "timestamp": analysis_result.get("timestamp")
        }
        
        event = PluginEvent(
            plugin_name="project_analyzer",
            event_type="project_analyzed",
            data=event_data
        )
        
        # Envia evento para o plugin Telegram
        await self.telegram_plugin.handle_event(event)
        return True
    
    async def notify_anomalies_detected(self, anomalies: Dict[str, Any], project_name: str) -> bool:
        """Notifica quando anomalias são detectadas"""
        if not self.telegram_plugin:
            return False
            
        event_data = {
            "anomalies": anomalies,
            "project_name": project_name,
            "detection_time": "now"
        }
        
        event = PluginEvent(
            plugin_name="project_analyzer", 
            event_type="anomalies_detected",
            data=event_data
        )
        
        await self.telegram_plugin.handle_event(event)
        return True