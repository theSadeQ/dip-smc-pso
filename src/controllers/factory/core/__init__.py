#======================================================================================\\\
#====================== src/controllers/factory/core/__init__.py ======================\\\
#======================================================================================\\\

"""
Factory Core Module - Central Factory Infrastructure

Core components for the controller factory system including:
- Base factory interfaces and protocols
- Registry management
- Configuration validation
- Thread-safe operations
"""

from .registry import CONTROLLER_REGISTRY, get_controller_info
from .protocols import ControllerProtocol, ControllerFactoryProtocol
from .validation import validate_controller_gains, validate_configuration
from .threading import factory_lock, with_factory_lock

__all__ = [
    'CONTROLLER_REGISTRY',
    'get_controller_info',
    'ControllerProtocol',
    'ControllerFactoryProtocol',
    'validate_controller_gains',
    'validate_configuration',
    'factory_lock',
    'with_factory_lock'
]