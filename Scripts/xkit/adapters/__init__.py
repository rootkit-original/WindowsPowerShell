"""
XKit Adapters
Adapters for external systems following hexagonal architecture
"""

from .cli import PowerShellAdapter, CommandAdapter
from .external import EventServiceAdapter, LegacyInfrastructureAdapter

__all__ = [
    'PowerShellAdapter',
    'CommandAdapter',
    'EventServiceAdapter', 
    'LegacyInfrastructureAdapter'
]

__version__ = "1.0.0"