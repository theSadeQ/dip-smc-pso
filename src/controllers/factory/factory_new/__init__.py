#======================================================================================\\
#============================== src/controllers/factory/__init__.py ====================\\
#======================================================================================\\

"""
Controller factory - refactored modular architecture.

Refactored from monolithic factory.py (1,435 lines) into focused modules:
- core.py: Main factory logic and controller creation

Public API (backward compatible):
- create_controller()
- list_available_controllers()
- list_all_controllers()
- get_default_gains()
- SMCType, SMCConfig, SMCFactory
- Various support functions

All imports from this package are backward compatible with the legacy
single-file factory.py approach.
"""

# Re-export all public API from core module
from .core import (
    # Main factory functions
    create_controller,
    list_available_controllers,
    list_all_controllers,
    get_default_gains,

    # Enums and config classes
    SMCType,
    SMCConfig,
    SMCFactory,

    # Support functions
    create_smc_for_pso,
    create_pso_controller_factory,
    get_expected_gain_count,
    get_gain_bounds_for_pso,
    validate_smc_gains,

    # Backwards compatibility
    create_classical_smc_controller,
    create_sta_smc_controller,
    create_adaptive_smc_controller,
    create_controller_legacy,

    # Constants and registry
    CONTROLLER_REGISTRY,
    CONTROLLER_ALIASES,

    # Exceptions
    ConfigValueError,
    ControllerProtocol,
)

__all__ = [
    # Main functions
    "create_controller",
    "list_available_controllers",
    "list_all_controllers",
    "get_default_gains",

    # Enums and configs
    "SMCType",
    "SMCConfig",
    "SMCFactory",

    # Support functions
    "create_smc_for_pso",
    "create_pso_controller_factory",
    "get_expected_gain_count",
    "get_gain_bounds_for_pso",
    "validate_smc_gains",

    # Backwards compatibility
    "create_classical_smc_controller",
    "create_sta_smc_controller",
    "create_adaptive_smc_controller",
    "create_controller_legacy",

    # Constants
    "CONTROLLER_REGISTRY",
    "CONTROLLER_ALIASES",

    # Exceptions
    "ConfigValueError",
    "ControllerProtocol",
]
