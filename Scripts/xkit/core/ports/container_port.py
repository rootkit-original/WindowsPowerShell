"""
Container Service Port
Interface for container operations (Docker/Podman)
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class ContainerStatus(Enum):
    """Container status"""
    RUNNING = "running"
    STOPPED = "stopped"
    PAUSED = "paused"
    RESTARTING = "restarting"
    REMOVING = "removing"
    EXITED = "exited"
    DEAD = "dead"


@dataclass
class ContainerInfo:
    """Container information"""
    id: str
    name: str
    image: str
    status: ContainerStatus
    ports: Dict[str, str]
    created: str
    started: Optional[str] = None


class IContainerService(ABC):
    """Port for container operations"""
    
    @abstractmethod
    async def list_containers(self, all_containers: bool = False) -> List[ContainerInfo]:
        """List containers"""
        pass
    
    @abstractmethod
    async def start_container(self, container_id: str) -> bool:
        """Start a container"""
        pass
    
    @abstractmethod
    async def stop_container(self, container_id: str) -> bool:
        """Stop a container"""
        pass
    
    @abstractmethod
    async def restart_container(self, container_id: str) -> bool:
        """Restart a container"""
        pass
    
    @abstractmethod
    async def get_container_logs(self, container_id: str, tail: int = 100) -> str:
        """Get container logs"""
        pass
    
    @abstractmethod
    async def execute_in_container(self, container_id: str, 
                                 command: str) -> Dict[str, Any]:
        """Execute command in container"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if container service is available"""
        pass