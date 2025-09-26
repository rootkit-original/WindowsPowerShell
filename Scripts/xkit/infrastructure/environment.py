"""
Environment detector - Detecção de ambientes (WSL, Container, etc.)
"""
import os
import platform
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class EnvironmentInfo:
    """Informações do ambiente atual"""
    type: str  # 'windows', 'wsl', 'container', 'linux'
    distro: Optional[str] = None
    container_type: Optional[str] = None  # 'alpine', 'ubuntu', 'debian'
    is_elevated: bool = False
    shell: str = 'unknown'
    
    @property
    def icon(self) -> str:
        """Ícone representativo do ambiente"""
        icons = {
            'windows': '🪟',
            'wsl': '🐧',
            'container': '🐳',
            'linux': '🐧',
            'alpine': '🏔️',
            'ubuntu': '🟠',
            'debian': '🌀'
        }
        
        if self.container_type:
            return icons.get(self.container_type, icons.get('container', '🐳'))
        
        return icons.get(self.type, '💻')
    
    @property
    def display_name(self) -> str:
        """Nome amigável do ambiente"""
        if self.container_type:
            return f"{self.container_type.title()} Container"
        
        names = {
            'windows': 'Windows',
            'wsl': 'WSL',
            'linux': 'Linux'
        }
        
        return names.get(self.type, self.type.title())


class EnvironmentDetector:
    """Detector de ambiente de execução"""
    
    def detect(self) -> EnvironmentInfo:
        """Detecta o ambiente atual"""
        env_type = self._detect_environment_type()
        distro = self._detect_distro()
        container_type = self._detect_container_type()
        is_elevated = self._is_elevated()
        shell = self._detect_shell()
        
        return EnvironmentInfo(
            type=env_type,
            distro=distro,
            container_type=container_type,
            is_elevated=is_elevated,
            shell=shell
        )
    
    def _detect_environment_type(self) -> str:
        """Detecta o tipo básico de ambiente"""
        system = platform.system().lower()
        
        # Verifica se está em container
        if self._is_in_container():
            return 'container'
        
        # Verifica WSL
        if self._is_wsl():
            return 'wsl'
        
        # Sistema base
        if system == 'windows':
            return 'windows'
        elif system == 'linux':
            return 'linux'
        elif system == 'darwin':
            return 'macos'
        
        return system
    
    def _detect_distro(self) -> Optional[str]:
        """Detecta a distribuição Linux"""
        try:
            # Tenta ler /etc/os-release
            if Path('/etc/os-release').exists():
                with open('/etc/os-release', 'r') as f:
                    for line in f:
                        if line.startswith('ID='):
                            return line.split('=')[1].strip().strip('"')
            
            # Fallback para outros métodos
            if Path('/etc/alpine-release').exists():
                return 'alpine'
            elif Path('/etc/debian_version').exists():
                return 'debian'
            
        except Exception:
            pass
        
        return None
    
    def _detect_container_type(self) -> Optional[str]:
        """Detecta se está rodando em container e qual tipo"""
        try:
            # Verifica Alpine container
            if Path('/etc/alpine-release').exists():
                return 'alpine'
            
            # Verifica outros indicadores de container
            container_indicators = [
                '/.dockerenv',
                '/run/.containerenv'
            ]
            
            for indicator in container_indicators:
                if Path(indicator).exists():
                    # Tenta determinar a distribuição base
                    distro = self._detect_distro()
                    if distro:
                        return distro
                    return 'unknown'
        
        except Exception:
            pass
        
        return None
    
    def _is_in_container(self) -> bool:
        """Verifica se está executando dentro de um container"""
        container_indicators = [
            '/.dockerenv',
            '/run/.containerenv'
        ]
        
        return any(Path(indicator).exists() for indicator in container_indicators)
    
    def _is_wsl(self) -> bool:
        """Verifica se está rodando no WSL"""
        try:
            # Verifica variável de ambiente WSL
            if os.getenv('WSL_DISTRO_NAME'):
                return True
            
            # Verifica /proc/version para WSL
            if Path('/proc/version').exists():
                with open('/proc/version', 'r') as f:
                    version_info = f.read().lower()
                    if 'microsoft' in version_info or 'wsl' in version_info:
                        return True
            
        except Exception:
            pass
        
        return False
    
    def _is_elevated(self) -> bool:
        """Verifica se está executando com privilégios elevados"""
        try:
            if platform.system().lower() == 'windows':
                import ctypes
                return bool(ctypes.windll.shell32.IsUserAnAdmin())
            else:
                return os.geteuid() == 0
        except Exception:
            return False
    
    def _detect_shell(self) -> str:
        """Detecta o shell atual"""
        try:
            shell = os.getenv('SHELL', '')
            if shell:
                return Path(shell).name
            
            # Fallback para Windows
            if platform.system().lower() == 'windows':
                return 'powershell'
            
        except Exception:
            pass
        
        return 'unknown'