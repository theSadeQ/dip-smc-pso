#======================================================================================\
#================ src/controllers/factory/factory_new/registration.py =================\
#======================================================================================\

"""
Controller registry and type canonicalization for the controller factory.

This module provides the controller registry, type aliasing, and controller
information retrieval functions.

Extracted from monolithic core.py (1,435 lines) during Phase 2 refactor.
"""

# Standard library imports
from typing import Any, Dict, List, Optional

# Local imports - Type definitions
from .types import ConfigValueError

# Local imports - Controller implementations
from src.controllers.smc.classic_smc import ClassicalSMC
from src.controllers.smc.sta_smc import SuperTwistingSMC
from src.controllers.smc.adaptive_smc import AdaptiveSMC
from src.controllers.smc.algorithms.hybrid.controller import ModularHybridSMC

# Local imports - Configuration classes with fallback handling
try:
    from src.controllers.smc.algorithms.classical.config import ClassicalSMCConfig
    from src.controllers.smc.algorithms.super_twisting.config import (
        SuperTwistingSMCConfig as STASMCConfig
    )
    from src.controllers.smc.algorithms.adaptive.config import AdaptiveSMCConfig
    from src.controllers.smc.algorithms.hybrid.config import (
        HybridSMCConfig as HybridAdaptiveSTASMCConfig
    )
    CONFIG_CLASSES_AVAILABLE = True
except ImportError:
    CONFIG_CLASSES_AVAILABLE = False
    # Fallback minimal config classes for graceful degradation
    from src.controllers.factory.fallback_configs import (
        ClassicalSMCConfig,
        STASMCConfig,
        AdaptiveSMCConfig,
        HybridAdaptiveSTASMCConfig
    )

# Optional MPC controller import
try:
    from src.controllers.mpc.mpc_controller import MPCController
    MPC_AVAILABLE = True
except ImportError:
    MPCController = None
    MPC_AVAILABLE = False

# =============================================================================
# CONTROLLER TYPE ALIASING
# =============================================================================

# Controller type aliases for backwards compatibility and normalization
CONTROLLER_ALIASES = {
    'classic_smc': 'classical_smc',
    'smc_classical': 'classical_smc',
    'smc_v1': 'classical_smc',
    'super_twisting': 'sta_smc',
    'sta': 'sta_smc',
    'adaptive': 'adaptive_smc',
    'hybrid': 'hybrid_adaptive_sta_smc',
    'hybrid_sta': 'hybrid_adaptive_sta_smc',
}

def _canonicalize_controller_type(name: str) -> str:
    """Normalize and alias controller type names.

    Args:
        name: Controller type name to normalize

    Returns:
        Canonical controller type name

    Raises:
        ValueError: If name is not a string or is empty
    """
    if not isinstance(name, str):
        raise ValueError(f"Controller type must be string, got {type(name)}")

    if not name.strip():
        raise ValueError("Controller type cannot be empty")

    key = name.strip().lower().replace('-', '_').replace(' ', '_')
    return CONTROLLER_ALIASES.get(key, key)

# =============================================================================
# CONTROLLER REGISTRY
# =============================================================================

# Controller registry with organized structure and comprehensive metadata
CONTROLLER_REGISTRY = {
    'classical_smc': {
        'class': ClassicalSMC,
        'config_class': ClassicalSMCConfig,
        'default_gains': [20.0, 15.0, 12.0, 8.0, 35.0, 5.0],  # [k1, k2, λ1, λ2, K, kd] - Optimized for DIP
        'gain_count': 6,
        'description': 'Classical sliding mode controller with boundary layer',
        'supports_dynamics': True,
        'required_params': ['gains', 'max_force', 'boundary_layer']
    },
    'sta_smc': {
        'class': SuperTwistingSMC,
        'config_class': STASMCConfig,
        'default_gains': [25.0, 15.0, 20.0, 12.0, 8.0, 6.0],  # [K1, K2, k1, k2, λ1, λ2] - Enhanced for DIP
        'gain_count': 6,
        'description': 'Super-twisting sliding mode controller',
        'supports_dynamics': True,
        'required_params': ['gains', 'max_force', 'dt']
    },
    'adaptive_smc': {
        'class': AdaptiveSMC,
        'config_class': AdaptiveSMCConfig,
        'default_gains': [25.0, 18.0, 15.0, 10.0, 4.0],  # [k1, k2, λ1, λ2, γ] - Aggressive for DIP
        'gain_count': 5,
        'description': 'Adaptive sliding mode controller with parameter estimation',
        'supports_dynamics': True,
        'required_params': ['gains', 'max_force', 'dt']
    },
    'hybrid_adaptive_sta_smc': {
        'class': ModularHybridSMC,
        'config_class': HybridAdaptiveSTASMCConfig,
        'default_gains': [18.0, 12.0, 10.0, 8.0],  # [k1, k2, λ1, λ2] - Enhanced for DIP
        'gain_count': 4,
        'description': 'Hybrid adaptive super-twisting sliding mode controller',
        'supports_dynamics': False,  # Uses sub-controllers
        'required_params': ['classical_config', 'adaptive_config', 'hybrid_mode']
    }
}

# Add MPC controller to registry if available
if MPC_AVAILABLE:
    # Create a minimal config class for MPC
    class MPCConfig:
        def __init__(self, horizon: int = 10, q_x: float = 1.0, q_theta: float = 1.0, r_u: float = 0.1, **kwargs: Any) -> None:
            self.horizon = horizon
            self.q_x = q_x
            self.q_theta = q_theta
            self.r_u = r_u
            for key, value in kwargs.items():
                setattr(self, key, value)

    CONTROLLER_REGISTRY['mpc_controller'] = {
        'class': MPCController,
        'config_class': MPCConfig,
        'default_gains': [],  # MPC doesn't use traditional gains
        'gain_count': 0,
        'description': 'Model predictive controller',
        'supports_dynamics': True,
        'required_params': ['horizon', 'q_x', 'q_theta', 'r_u']
    }
else:
    # Add placeholder entry when MPC is not available for proper error handling
    class UnavailableMPCConfig:
        def __init__(self, **kwargs: Any) -> None:
            pass

    CONTROLLER_REGISTRY['mpc_controller'] = {
        'class': None,
        'config_class': UnavailableMPCConfig,
        'default_gains': [],
        'gain_count': 0,
        'description': 'Model predictive controller (unavailable)',
        'supports_dynamics': True,
        'required_params': ['horizon', 'q_x', 'q_theta', 'r_u']
    }

# =============================================================================
# REGISTRY ACCESS FUNCTIONS
# =============================================================================

def _get_controller_info(controller_type: str) -> Dict[str, Any]:
    """Get controller information from registry with validation.

    Args:
        controller_type: Canonical controller type name

    Returns:
        Controller registry information

    Raises:
        ValueError: If controller type is not recognized
        ImportError: If controller type is recognized but unavailable due to missing dependencies
    """
    if controller_type not in CONTROLLER_REGISTRY:
        available = list(CONTROLLER_REGISTRY.keys())
        raise ValueError(
            f"Unknown controller type '{controller_type}'. "
            f"Available: {available}"
        )

    controller_info = CONTROLLER_REGISTRY[controller_type].copy()

    # For MPC controller, check if it's been dynamically made available (e.g., via monkeypatch)
    if controller_type == 'mpc_controller' and controller_info['class'] is None:
        # Check if MPCController is now available (handles monkeypatch scenarios)
        try:
            # Check parent package first (where monkeypatch usually applies)
            import sys
            parent_package = 'src.controllers.factory'
            if parent_package in sys.modules:
                parent_module = sys.modules[parent_package]
                if hasattr(parent_module, 'MPCController') and getattr(parent_module, 'MPCController') is not None:
                    controller_info['class'] = getattr(parent_module, 'MPCController')

            # If still None, raise helpful error
            if controller_info['class'] is None:
                raise ImportError(
                    "MPC controller is not available. Install required dependencies: "
                    "pip install cvxpy control"
                )
        except ImportError as e:
            raise ImportError(
                f"MPC controller requires optional dependencies: {e}"
            ) from e

    return controller_info

def list_available_controllers() -> List[str]:
    """Get list of currently available controller types that can be instantiated.

    This function queries the controller registry and returns only those controller types
    for which all required dependencies are available. Controllers that require missing
    optional dependencies (e.g., MPC without cvxpy) are excluded from the list.

    Returns:
        List[str]: Sorted list of controller type names that can be created via
            create_controller(). Each name is a canonical controller type identifier:
            ['adaptive_smc', 'classical_smc', 'hybrid_adaptive_sta_smc', 'sta_smc']
            (if MPC dependencies are missing, 'mpc_controller' is excluded)

    Examples:
        >>> from src.controllers.factory import list_available_controllers, create_controller
        >>>
        >>> # Query available controllers before creation
        >>> available = list_available_controllers()
        >>> print(available)
        ['adaptive_smc', 'classical_smc', 'hybrid_adaptive_sta_smc', 'sta_smc']
        >>>
        >>> # Dynamically create all available controllers for benchmarking
        >>> controllers = {}
        >>> for controller_type in list_available_controllers():
        ...     controllers[controller_type] = create_controller(controller_type)
        >>>
        >>> # Check if specific controller is available
        >>> if 'mpc_controller' in list_available_controllers():
        ...     mpc = create_controller('mpc_controller')

    See Also:
        - list_all_controllers(): Returns all registered types including unavailable ones
        - CONTROLLER_REGISTRY: Complete registry with availability metadata
        - create_controller(): Primary factory function for controller instantiation

    Notes:
        - This function performs live availability checks of controller classes
        - The returned list may change if optional dependencies are installed/uninstalled
        - Use this function to avoid ImportError exceptions from create_controller()
        - The list is sorted alphabetically for consistent iteration order
    """
    available_controllers = []
    for controller_type, controller_info in CONTROLLER_REGISTRY.items():
        # Only include controllers that have available classes
        if controller_info['class'] is not None:
            available_controllers.append(controller_type)
    return available_controllers

def list_all_controllers() -> List[str]:
    """Get list of all registered controller types, including unavailable ones.

    Returns:
        List of all controller type names in the registry
    """
    return list(CONTROLLER_REGISTRY.keys())

def get_default_gains(controller_type: str) -> List[float]:
    """Get default gain vector for a specific controller type from the registry.

    This function retrieves the registry-defined default gains for a controller type,
    which serve as baseline values when gains are not explicitly provided to
    create_controller() or not found in the configuration file.

    The default gains are carefully tuned for the double-inverted pendulum (DIP)
    system and provide reasonable baseline performance. For optimal performance,
    use PSO optimization to tune gains for specific plant configurations.

    Args:
        controller_type: Controller type identifier (must be canonical name, not alias).
            Valid types: 'classical_smc', 'sta_smc', 'adaptive_smc',
            'hybrid_adaptive_sta_smc', 'mpc_controller'

    Returns:
        List[float]: Copy of the default gain vector for the controller type:
            - Classical SMC: [20.0, 15.0, 12.0, 8.0, 35.0, 5.0]
            - STA SMC: [25.0, 15.0, 20.0, 12.0, 8.0, 6.0]
            - Adaptive SMC: [25.0, 18.0, 15.0, 10.0, 4.0]
            - Hybrid SMC: [18.0, 12.0, 10.0, 8.0]
            - MPC: [] (MPC uses cost matrices instead of gains)

    Raises:
        ValueError: If controller_type is not in the registry. Error message includes
            list of all registered controller types.

    Examples:
        >>> from src.controllers.factory import get_default_gains, create_controller
        >>>
        >>> # Example 1: Query default gains before optimization
        >>> default_gains = get_default_gains('classical_smc')
        >>> print(f"Default gains: {default_gains}")
        Default gains: [20.0, 15.0, 12.0, 8.0, 35.0, 5.0]
        >>>
        >>> # Example 2: Use defaults as PSO initialization
        >>> from src.optimization.integration.pso_factory_bridge import create_optimized_controller_factory
        >>> initial_guess = get_default_gains('sta_smc')
        >>> # PSO optimization starts from initial_guess...
        >>>
        >>> # Example 3: Compare controller with defaults vs. optimized gains
        >>> controller_default = create_controller('classical_smc')  # Uses defaults
        >>> controller_tuned = create_controller('classical_smc', gains=[25.0, 18.0, 14.0, 10.0, 42.0, 6.0])
        >>> print(f"Default cost: {evaluate(controller_default)}")
        >>> print(f"Tuned cost: {evaluate(controller_tuned)}")

    See Also:
        - CONTROLLER_REGISTRY: Complete registry with default gains and metadata
        - create_controller(): Uses these defaults when gains are not provided
        - src.optimization.algorithms.pso_optimizer: PSO-based gain optimization
        - config.yaml: Override defaults via configuration file

    Notes:
        - Returns a copy of the gains list to prevent accidental modification of registry
        - Default gains are optimized for nominal DIP parameters in config.yaml
        - For plant variations or uncertainty, use PSO optimization or robust tuning
        - Gains are ordered according to controller-specific conventions (see controller docs)
        - MPC controller returns empty list as it uses horizon/cost matrices instead
    """
    if controller_type not in CONTROLLER_REGISTRY:
        available = list(CONTROLLER_REGISTRY.keys())
        raise ValueError(f"Unknown controller type '{controller_type}'. Available: {available}")

    return CONTROLLER_REGISTRY[controller_type]['default_gains'].copy()
