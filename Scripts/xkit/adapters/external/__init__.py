"""
XKit External Adapters
Adapters for external systems and APIs
"""

from .event_adapter import EventServiceAdapter
from .legacy_adapter import LegacyInfrastructureAdapter

__all__ = [
    'EventServiceAdapter',
    'LegacyInfrastructureAdapter'
]