"""
XKit Adapters
Adapters for external systems following hexagonal architecture
"""

from .cli import PowerShellAdapter, CommandAdapter
from .external import EventServiceAdapter

__all__ = [
    'PowerShellAdapter',
    'CommandAdapter',
    'EventServiceAdapter'
]

__version__ = "1.0.0"