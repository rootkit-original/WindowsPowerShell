"""
Container repository implementation - integrates Podman/Docker functionality
"""
import subprocess
from pathlib import Path
from typing import Optional
from ..domain.interfaces import IContainerRepository
from ..domain.entities import ContainerInfo


class ContainerRepository(IContainerRepository):
    """Container operations implementation"""
    
    # Common container engine paths
    CONTAINER_ENGINES = {
        'podman': [
            Path("C:/Program Files/RedHat/Podman/podman.exe"),
            Path("C:/ProgramData/chocolatey/bin/podman.exe"),
            Path("/usr/bin/podman"),  # Linux/WSL
        ],
        'docker': [
            Path("C:/Program Files/Docker/Docker/resources/bin/docker.exe"),
            Path("C:/ProgramData/chocolatey/bin/docker.exe"),
            Path("/usr/bin/docker"),  # Linux/WSL
        ]
    }
    
    def _command_available(self, command: str) -> bool:
        """Verifica se um comando está disponível no PATH"""
        try:
            subprocess.run([command, '--version'], 
                          capture_output=True, timeout=5, check=True)
            return True
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def detect_container_engine(self) -> Optional[ContainerInfo]:
        """Detect available container engine (prioritize Podman)"""
        
        has_podman_compose = self._command_available('podman-compose')
        has_docker_compose = self._command_available('docker-compose') or self._command_available('docker')
        
        # Try Podman first (as per original configuration)
        for engine_path in self.CONTAINER_ENGINES['podman']:
            if self.is_engine_available(engine_path):
                return ContainerInfo(
                    engine_type='podman',
                    engine_path=engine_path,
                    is_available=True,
                    has_compose=has_podman_compose
                )
        
        # Fallback to Docker
        for engine_path in self.CONTAINER_ENGINES['docker']:
            if self.is_engine_available(engine_path):
                return ContainerInfo(
                    engine_type='docker',
                    engine_path=engine_path,
                    is_available=True,
                    has_compose=has_docker_compose
                )
        
        return None
    
    def is_engine_available(self, engine_path: Path) -> bool:
        """Check if container engine is available"""
        return engine_path.exists()
    
    def get_container_commands(self, container_info: ContainerInfo) -> dict:
        """Get available container commands based on detected engine"""
        if not container_info.is_available:
            return {}
            
        base_commands = {
            'build': f'Build images using {container_info.engine_type}',
            'run': f'Run containers using {container_info.engine_type}',
            'ps': f'List containers using {container_info.engine_type}',
            'images': f'List images using {container_info.engine_type}',
            'exec': f'Execute commands in containers using {container_info.engine_type}',
            'stop': f'Stop containers using {container_info.engine_type}',
            'rm': f'Remove containers using {container_info.engine_type}',
            'logs': f'View container logs using {container_info.engine_type}',
        }
        
        # Add compose commands if available
        if hasattr(container_info, 'has_compose') and container_info.has_compose:
            compose_cmd = 'podman-compose' if container_info.engine_type == 'podman' else 'docker compose'
            base_commands.update({
                'compose-up': f'Start services using {compose_cmd}',
                'compose-down': f'Stop services using {compose_cmd}',
                'compose-build': f'Build services using {compose_cmd}',
                'compose-ps': f'List services using {compose_cmd}',
                'compose-logs': f'View service logs using {compose_cmd}',
            })
        
        # Add Podman-specific commands if using Podman
        if container_info.engine_type == 'podman':
            base_commands.update({
                'machine-list': 'List Podman machines',
                'machine-start': 'Start Podman machine',
            })
        
        return base_commands