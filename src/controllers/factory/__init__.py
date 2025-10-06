#======================================================================================\\\
#======================== src/controllers/factory/__init__.py =========================\\\
#======================================================================================\\\

"""
Controller Factory Package

Provides clean, focused factory interfaces for creating controllers:
- SMC Factory: Type-safe, PSO-optimized interface for 4 core SMC controllers
- Legacy Factory: Backward-compatible factory for existing code

Recommended Usage:
    # Use the clean SMC factory for new code
    from controllers.factory import SMCFactory, SMCType, create_smc_for_pso

    # Use legacy factory only for backward compatibility
    from controllers.factory import create_controller_legacy
"""

# Standard library imports
from typing import Dict, List, Any

# Export the clean SMC factory as primary interface
from .smc_factory import (
    # Core types
    SMCType,
    SMCConfig,
    SMCGainSpec,
    SMCProtocol,
    SMCFactory,

    # PSO wrapper and convenience functions
    PSOControllerWrapper,
    create_smc_for_pso,
    get_gain_bounds_for_pso,
    validate_smc_gains,

    # Specifications
    SMC_GAIN_SPECS
)

# Export legacy factory for backward compatibility
from .legacy_factory import create_controller as create_controller_legacy
from .legacy_factory import create_controller  # Also export with original name
from .legacy_factory import build_controller as build_controller_legacy
from .legacy_factory import build_controller  # Also export with original name
from .legacy_factory import build_all as build_all_legacy
from .legacy_factory import _canonical  # For test compatibility
from .legacy_factory import FactoryConfigurationError, ConfigValueError, UnknownConfigKeyError  # Exception types

# Import the new factory functions from the factory.py module for compatibility
import sys
import os
import importlib.util

# Get the factory.py module path
factory_py_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'factory.py')

if os.path.exists(factory_py_path):
    spec = importlib.util.spec_from_file_location('factory_module', factory_py_path)
    factory_module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(factory_module)

        # Force reload if the module is already in sys.modules to ensure latest version
        if 'factory_module' in sys.modules:
            importlib.reload(factory_module)

        # Export the functions from factory.py module
        list_available_controllers = factory_module.list_available_controllers
        list_all_controllers = factory_module.list_all_controllers
        get_default_gains = factory_module.get_default_gains
        CONTROLLER_REGISTRY = factory_module.CONTROLLER_REGISTRY
        create_controller_new = factory_module.create_controller
        # Override the legacy create_controller with the new one
        create_controller = factory_module.create_controller
        # Export PSO-specific functions
        create_pso_controller_factory = factory_module.create_pso_controller_factory
        get_expected_gain_count = factory_module.get_expected_gain_count

    except Exception:
        # Fallback if the factory.py module can't be loaded
        def list_available_controllers() -> List[str]:
            """Fallback function when factory.py is not available."""
            return ['classical_smc', 'sta_smc', 'adaptive_smc', 'hybrid_adaptive_sta_smc']

        def get_default_gains(controller_type: str) -> List[float]:
            """Fallback function when factory.py is not available."""
            defaults: Dict[str, List[float]] = {
                'classical_smc': [5.0, 5.0, 5.0, 0.5, 0.5, 0.5],
                'sta_smc': [4.0, 4.0, 4.0, 0.4, 0.4, 0.4],
                'adaptive_smc': [10.0, 8.0, 5.0, 4.0, 1.0],
                'hybrid_adaptive_sta_smc': [5.0, 5.0, 5.0, 0.5]
            }
            return defaults.get(controller_type, [1.0, 1.0, 1.0, 1.0])

        CONTROLLER_REGISTRY = {}
        create_controller_new = create_controller

# Add missing deprecation mapping function for backward compatibility
def apply_deprecation_mapping(controller_type: str, params: dict = None, allow_unknown: bool = True) -> dict:
    """
    Apply deprecation mapping for controller parameters.

    This function handles mapping of deprecated parameter names
    to their current equivalents for backward compatibility.

    Args:
        controller_type: The controller type string to map
        params: Parameters dictionary to process (optional)
        allow_unknown: Whether to allow unknown parameters (ignored)

    Returns:
        Processed parameters dictionary with deprecation mappings applied
    """
    import warnings

    if params is None:
        params = {}

    # Make a copy to avoid modifying the original
    processed_params = params.copy()

    # Define parameter deprecation mappings by controller type
    deprecation_mappings = {
        'hybrid_adaptive_sta_smc': {
            'use_equivalent': 'enable_equivalent'
        },
        'classical_smc': {
            'boundary_thickness': 'boundary_layer',
            'force_saturation': 'max_force'
        },
        'sta_smc': {
            'twisting_gain1': 'K1',
            'twisting_gain2': 'K2'
        },
        'adaptive_smc': {
            'adaptation_rate': 'gamma',
            'leakage_rate': 'leak_rate'
        }
    }

    # Apply mappings for this controller type
    if controller_type in deprecation_mappings:
        controller_mappings = deprecation_mappings[controller_type]

        for old_param, new_param in controller_mappings.items():
            if old_param in processed_params:
                # Issue deprecation warning
                warnings.warn(
                    f"Parameter '{old_param}' for {controller_type} is deprecated. "
                    f"Use '{new_param}' instead.",
                    DeprecationWarning,
                    stacklevel=3
                )

                # Map the parameter if new one doesn't already exist
                if new_param not in processed_params:
                    processed_params[new_param] = processed_params[old_param]

                # Remove the old parameter
                del processed_params[old_param]

    return processed_params


def _as_dict(obj: Any) -> Dict[str, Any]:
    """
    Convert an object to dictionary representation.

    Handles objects with model_dump() method (like Pydantic models)
    and regular objects with __dict__.

    Args:
        obj: Object to convert to dictionary

    Returns:
        Dictionary representation of the object
    """
    if hasattr(obj, 'model_dump'):
        # Pydantic v2 style
        return obj.model_dump(exclude_unset=True)
    elif hasattr(obj, 'dict'):
        # Pydantic v1 style
        return obj.dict(exclude_unset=True)
    elif hasattr(obj, '__dict__'):
        # Regular object
        return obj.__dict__
    else:
        # Fallback to the object itself if it's already dict-like
        return dict(obj) if hasattr(obj, 'keys') else {}

# Clean public API - prioritize new SMC factory
__all__ = [
    # ========================================
    # PRIMARY INTERFACE - Clean SMC Factory
    # ========================================

    # Core types
    "SMCType",
    "SMCConfig",
    "SMCGainSpec",
    "SMCProtocol",
    "SMCFactory",

    # PSO integration
    "create_smc_for_pso",
    "get_gain_bounds_for_pso",
    "validate_smc_gains",
    "PSOControllerWrapper",

    # Specifications
    "SMC_GAIN_SPECS",

    # ========================================
    # LEGACY COMPATIBILITY
    # ========================================

    "create_controller",          # Original name for backward compatibility
    "create_controller_legacy",
    "build_controller",           # Original name for backward compatibility
    "build_controller_legacy",
    "build_all_legacy",
    "_canonical",                 # For test compatibility
    "apply_deprecation_mapping",  # Deprecation mapping function
    "_as_dict",                   # Object to dict conversion function

    # New factory.py functions for test compatibility
    "list_available_controllers",
    "list_all_controllers",
    "get_default_gains",
    "CONTROLLER_REGISTRY",
    "create_controller_new",
    "create_pso_controller_factory",
    "get_expected_gain_count",

    # Exception types
    "FactoryConfigurationError",
    "ConfigValueError",
    "UnknownConfigKeyError"
]