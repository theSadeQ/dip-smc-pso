#==========================================================================================\\\
#============================== src/controllers/factory.py =============================\\\
#==========================================================================================\\\
"""
Controller factory for creating control system instances.

This module provides a factory pattern for instantiating different types
of controllers with proper configuration and parameter management.
"""

from typing import Any, Callable, Dict, List, Optional, Tuple, Union
import numpy as np
import logging

# Import the dynamics models from the compatibility layer
try:
    from ..core.dynamics import DIPDynamics as DoubleInvertedPendulum
except ImportError:
    try:
        from src.core.dynamics import DIPDynamics as DoubleInvertedPendulum
    except ImportError:
        # Fallback for legacy import paths
        try:
            from src.plant.models.simplified.dynamics import (
                SimplifiedDIPDynamics as DoubleInvertedPendulum
            )
        except ImportError:
            raise ImportError(
                "Could not import DoubleInvertedPendulum from any expected location"
            )

# Import controller implementations
from src.controllers.smc.algorithms.classical.controller import (
    ModularClassicalSMC
)
from src.controllers.smc.algorithms.super_twisting.controller import (
    ModularSuperTwistingSMC
)
from src.controllers.smc.algorithms.adaptive.controller import (
    ModularAdaptiveSMC
)
from src.controllers.smc.algorithms.hybrid.controller import (
    ModularHybridSMC
)

# Import enums needed for configuration
from src.controllers.smc.algorithms.hybrid.config import HybridMode

# Import configuration classes
try:
    from src.controllers.smc.algorithms.classical.config import (
        ClassicalSMCConfig
    )
    from src.controllers.smc.algorithms.super_twisting.config import (
        SuperTwistingSMCConfig as STASMCConfig
    )
    from src.controllers.smc.algorithms.adaptive.config import (
        AdaptiveSMCConfig
    )
    from src.controllers.smc.algorithms.hybrid.config import (
        HybridSMCConfig as HybridAdaptiveSTASMCConfig
    )
except ImportError:
    # Create minimal config classes if the full ones don't exist
    from dataclasses import dataclass

    @dataclass
    class ClassicalSMCConfig:
        gains: list
        max_force: float = 150.0
        boundary_layer: float = 0.02
        boundary_layer_slope: float = 1.0
        switch_method: str = "tanh"
        regularization: float = 1e-6
        dynamics_model: Any = None

        def get_surface_gains(self) -> List[float]:
            return self.gains[:4] if len(self.gains) >= 4 else self.gains

        def get_effective_controllability_threshold(self) -> float:
            return self.regularization

    @dataclass
    class STASMCConfig:
        gains: list
        max_force: float = 150.0
        damping_gain: float = 0.0
        dt: float = 0.001
        switch_method: str = "tanh"
        dynamics_model: Any = None
        K1: float = 4.0
        K2: float = 0.4
        power_exponent: float = 0.5
        regularization: float = 1e-6

        def get_surface_gains(self) -> List[float]:
            return self.gains[:4] if len(self.gains) >= 4 else self.gains

        def get_effective_anti_windup_gain(self) -> float:
            return self.damping_gain

    @dataclass
    class AdaptiveSMCConfig:
        gains: list
        max_force: float = 150.0
        leak_rate: float = 0.01
        dead_zone: float = 0.05
        adapt_rate_limit: float = 10.0
        K_min: float = 0.1
        K_max: float = 100.0
        dt: float = 0.001
        smooth_switch: bool = True
        boundary_layer: float = 0.1
        gamma: float = 2.0
        dynamics_model: Any = None

        def get_surface_gains(self):
            return self.gains[:4] if len(self.gains) >= 4 else self.gains

        def get_adaptation_bounds(self):
            return (self.K_min, self.K_max)

    @dataclass
    class HybridAdaptiveSTASMCConfig:
        gains: list
        max_force: float = 150.0
        dt: float = 0.001
        k1_init: float = 4.0
        k2_init: float = 0.4
        gamma1: float = 2.0
        gamma2: float = 0.5
        dead_zone: float = 0.05
        dynamics_model: Any = None

        def get_surface_gains(self):
            return self.gains[:4] if len(self.gains) >= 4 else self.gains


# Map controller names to their implementations and configs
# Alias mapping for backwards compatibility and normalization
ALIAS_MAP = {
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

    - Lowercases and replaces dashes/spaces with underscores
    - Applies common aliases (e.g., classic_smc -> classical_smc)
    """
    if not isinstance(name, str):
        return name
    key = name.strip().lower().replace('-', '_').replace(' ', '_')
    return ALIAS_MAP.get(key, key)
CONTROLLER_REGISTRY = {
    'classical_smc': {
        'class': ModularClassicalSMC,
        'config_class': ClassicalSMCConfig,
        'default_gains': [8.0, 6.0, 4.0, 3.0, 15.0, 2.0]  # Tuned for stability
    },
    'sta_smc': {
        'class': ModularSuperTwistingSMC,
        'config_class': STASMCConfig,
        'default_gains': [10.0, 5.0, 8.0, 6.0, 2.0, 1.5]  # Balanced gains
    },
    'adaptive_smc': {
        'class': ModularAdaptiveSMC,
        'config_class': AdaptiveSMCConfig,
        'default_gains': [12.0, 10.0, 6.0, 5.0, 2.5]  # Improved convergence
    },
    'hybrid_adaptive_sta_smc': {
        'class': ModularHybridSMC,
        'config_class': HybridAdaptiveSTASMCConfig,
        'default_gains': [8.0, 6.0, 4.0, 3.0]  # Stable surface gains
    }
}


def create_controller(controller_type: str,
                     config: Optional[Any] = None,
                     gains: Optional[Union[list, np.ndarray]] = None) -> Any:
    """
    Create a controller instance of the specified type.

    Args:
        controller_type: Type of controller ('classical_smc', 'sta_smc', etc.)
        config: Configuration object (optional)
        gains: Controller gains array (optional)

    Returns:
        Configured controller instance

    Raises:
        ValueError: If controller_type is not recognized
        ImportError: If required dependencies are missing
    """
    logger = logging.getLogger(__name__)

    # Normalize/alias controller type
    controller_type = _canonicalize_controller_type(controller_type)

    # Validate controller type
    if controller_type not in CONTROLLER_REGISTRY:
        available = list(CONTROLLER_REGISTRY.keys())
        raise ValueError(f"Unknown controller type '{controller_type}'. Available: {available}")

    controller_info = CONTROLLER_REGISTRY[controller_type]
    controller_class = controller_info['class']
    config_class = controller_info['config_class']

    # Determine gains to use
    if gains is not None:
        if isinstance(gains, np.ndarray):
            gains = gains.tolist()
        controller_gains = gains
    else:
        # Try to get gains from config
        if config is not None:
            try:
                # Try different ways to extract gains from config
                if hasattr(config, 'controller_defaults'):
                    controller_gains = getattr(config.controller_defaults.get(controller_type, {}), 'gains', None)
                    if controller_gains is None and isinstance(config.controller_defaults, dict):
                        controller_gains = config.controller_defaults.get(controller_type, {}).get('gains')
                elif hasattr(config, 'controllers'):
                    controller_gains = getattr(config.controllers.get(controller_type, {}), 'gains', None)
                else:
                    controller_gains = None

                if controller_gains is None:
                    controller_gains = controller_info['default_gains']
            except Exception:
                controller_gains = controller_info['default_gains']
        else:
            controller_gains = controller_info['default_gains']

    # Create dynamics model if needed
    dynamics_model = None
    if config is not None:
        try:
            # Try to get existing dynamics model
            if hasattr(config, 'dynamics_model'):
                dynamics_model = config.dynamics_model
            elif hasattr(config, 'physics'):
                dynamics_model = DoubleInvertedPendulum(config.physics)
            elif hasattr(config, 'dip_params'):
                dynamics_model = DoubleInvertedPendulum(config.dip_params)
        except Exception as e:
            logger.warning(f"Could not create dynamics model: {e}")

    # Extract controller-specific parameters from config
    controller_params = {}
    if config is not None:
        try:
            if hasattr(config, 'controllers') and controller_type in config.controllers:
                controller_config = config.controllers[controller_type]
                if hasattr(controller_config, 'model_dump'):
                    controller_params = controller_config.model_dump()
                elif isinstance(controller_config, dict):
                    controller_params = controller_config.copy()
                else:
                    # Extract attributes from config object
                    controller_params = {
                        attr: getattr(controller_config, attr)
                        for attr in dir(controller_config)
                        if not attr.startswith('_') and not callable(getattr(controller_config, attr))
                    }
        except Exception as e:
            logger.warning(f"Could not extract controller parameters: {e}")

    # Create configuration object
    try:
        # Build config parameters based on controller type
        if controller_type == 'hybrid_adaptive_sta_smc':
            # Hybrid controllers require special handling - need sub-configs
            # Import the config classes
            from src.controllers.smc.algorithms.classical.config import ClassicalSMCConfig
            from src.controllers.smc.algorithms.adaptive.config import AdaptiveSMCConfig

            # Create proper sub-configs with all required parameters
            classical_config = ClassicalSMCConfig(
                gains=[8.0, 6.0, 4.0, 3.0, 15.0, 2.0],
                max_force=150.0,
                dt=0.001,
                boundary_layer=0.02
            )
            adaptive_config = AdaptiveSMCConfig(
                gains=[12.0, 10.0, 6.0, 5.0, 2.5],
                max_force=150.0,
                dt=0.001
            )

            config_params = {
                'hybrid_mode': HybridMode.CLASSICAL_ADAPTIVE,  # Default hybrid mode enum
                'dt': 0.001,
                'max_force': 150.0,
                'classical_config': classical_config,
                'adaptive_config': adaptive_config,
                'dynamics_model': dynamics_model,
                **controller_params
            }
        else:
            # Standard controllers use gains - ensure required parameters are provided
            config_params = {
                'gains': controller_gains,
                'max_force': 150.0,  # Required by all controllers
                'dt': 0.001,  # Safe default for all
                **controller_params
            }

            # Add controller-specific required parameters
            if controller_type == 'classical_smc':
                config_params.setdefault('boundary_layer', 0.02)  # Required parameter
            elif controller_type == 'sta_smc':
                # Ensure STA-specific parameters are present
                config_params.setdefault('K1', 4.0)
                config_params.setdefault('K2', 0.4)
                config_params.setdefault('power_exponent', 0.5)
                config_params.setdefault('regularization', 1e-6)
            elif controller_type == 'adaptive_smc':
                # Ensure Adaptive-specific parameters are present
                config_params.setdefault('leak_rate', 0.01)
                config_params.setdefault('dead_zone', 0.05)
                config_params.setdefault('adapt_rate_limit', 10.0)
                config_params.setdefault('K_min', 0.1)
                config_params.setdefault('K_max', 100.0)
                config_params.setdefault('boundary_layer', 0.1)
                config_params.setdefault('gamma', 2.0)
                config_params.setdefault('smooth_switch', True)

            # Only add dynamics_model for controllers that support it
            if dynamics_model is not None and controller_type in ['classical_smc', 'sta_smc', 'adaptive_smc']:
                config_params['dynamics_model'] = dynamics_model

        # Remove None values and filter to only valid parameters
        config_params = {k: v for k, v in config_params.items() if v is not None}

        controller_config = config_class(**config_params)
    except Exception as e:
        logger.warning(f"Could not create full config, using minimal config: {e}")
        # Fallback to minimal configuration with ALL required defaults
        if controller_type == 'hybrid_adaptive_sta_smc':
            # Hybrid controller has completely different structure
            # Import the config classes
            from src.controllers.smc.algorithms.classical.config import ClassicalSMCConfig
            from src.controllers.smc.algorithms.adaptive.config import AdaptiveSMCConfig

            # Create minimal sub-configs with ALL required parameters
            classical_config = ClassicalSMCConfig(
                gains=[8.0, 6.0, 4.0, 3.0, 15.0, 2.0],
                max_force=150.0,
                dt=0.001,
                boundary_layer=0.02
            )
            adaptive_config = AdaptiveSMCConfig(
                gains=[12.0, 10.0, 6.0, 5.0, 2.5],
                max_force=150.0,
                dt=0.001
            )

            fallback_params = {
                'hybrid_mode': HybridMode.CLASSICAL_ADAPTIVE,  # Default hybrid mode enum
                'dt': 0.001,
                'max_force': 150.0,
                'classical_config': classical_config,
                'adaptive_config': adaptive_config
            }
        else:
            # Standard controllers use gains - ensure ALL required parameters are included
            fallback_params = {
                'gains': controller_gains,
                'max_force': 150.0,  # Always required
                'dt': 0.001  # Always add dt for safety
            }

            # Add controller-specific required parameters
            if controller_type == 'classical_smc':
                fallback_params['boundary_layer'] = 0.02  # Required parameter
            elif controller_type == 'sta_smc':
                # STA SMC may have specific requirements - check config
                fallback_params.update({
                    'K1': 4.0,
                    'K2': 0.4,
                    'power_exponent': 0.5,
                    'regularization': 1e-6
                })
            elif controller_type == 'adaptive_smc':
                # Adaptive SMC specific defaults
                fallback_params.update({
                    'leak_rate': 0.01,
                    'dead_zone': 0.05,
                    'adapt_rate_limit': 10.0,
                    'K_min': 0.1,
                    'K_max': 100.0,
                    'boundary_layer': 0.1,
                    'gamma': 2.0,
                    'smooth_switch': True
                })

            # Only add dynamics_model if not None and controller supports it
            if dynamics_model is not None and controller_type in ['classical_smc', 'sta_smc', 'adaptive_smc']:
                fallback_params['dynamics_model'] = dynamics_model

        controller_config = config_class(**fallback_params)

    # Create and return controller instance
    try:
        controller = controller_class(controller_config)
        logger.info(f"Created {controller_type} controller with gains: {controller_gains}")
        return controller
    except Exception as e:
        logger.error(f"Failed to create {controller_type} controller: {e}")
        raise


def list_available_controllers() -> list:
    """
    Get list of available controller types.

    Returns:
        List of controller type names
    """
    return list(CONTROLLER_REGISTRY.keys())


def get_default_gains(controller_type: str) -> list:
    """
    Get default gains for a controller type.

    Args:
        controller_type: Type of controller

    Returns:
        Default gains list

    Raises:
        ValueError: If controller_type is not recognized
    """
    if controller_type not in CONTROLLER_REGISTRY:
        available = list(CONTROLLER_REGISTRY.keys())
        raise ValueError(f"Unknown controller type '{controller_type}'. Available: {available}")

    return CONTROLLER_REGISTRY[controller_type]['default_gains'].copy()


# Backwards compatibility aliases
def create_classical_smc_controller(config: Optional[Any] = None, gains: Optional[Union[list, np.ndarray]] = None) -> Any:
    """Create classical SMC controller (backwards compatibility)."""
    return create_controller('classical_smc', config, gains)


def create_sta_smc_controller(config: Optional[Any] = None, gains: Optional[Union[list, np.ndarray]] = None) -> Any:
    """Create super-twisting SMC controller (backwards compatibility)."""
    return create_controller('sta_smc', config, gains)


def create_adaptive_smc_controller(config: Optional[Any] = None, gains: Optional[Union[list, np.ndarray]] = None) -> Any:
    """Create adaptive SMC controller (backwards compatibility)."""
    return create_controller('adaptive_smc', config, gains)


# Additional backwards compatibility for the existing __init__.py
def create_controller_legacy(controller_type: str, config: Optional[Any] = None, gains: Optional[Union[list, np.ndarray]] = None) -> Any:
    """Legacy factory function (backwards compatibility)."""
    return create_controller(controller_type, config, gains)


# Placeholder classes and functions for the existing __init__.py structure
from enum import Enum

class SMCType(Enum):
    """SMC Controller types enumeration."""
    CLASSICAL = "classical_smc"
    ADAPTIVE = "adaptive_smc"
    SUPER_TWISTING = "sta_smc"
    HYBRID = "hybrid_adaptive_sta_smc"


class SMCConfig:
    """Configuration class for SMC controllers."""
    def __init__(self, gains, max_force=150.0, dt=0.001, **kwargs):
        self.gains = gains
        self.max_force = max_force
        self.dt = dt
        for key, value in kwargs.items():
            setattr(self, key, value)


class SMCFactory:
    """Factory class for creating SMC controllers."""

    @staticmethod
    def create_controller(smc_type: SMCType, config: SMCConfig) -> Any:
        """Create controller using SMCType enum."""
        return create_controller(smc_type.value, config, config.gains)


class PSOControllerWrapper:
    """Wrapper for SMC controllers to provide PSO-compatible interface."""

    def __init__(self, controller, n_gains: int, controller_type: str):
        self.controller = controller
        self.n_gains = n_gains
        self.controller_type = controller_type
        self.max_force = getattr(controller, 'max_force', 150.0)

    def compute_control(self, state: np.ndarray) -> np.ndarray:
        """PSO-compatible control computation interface."""
        try:
            # Validate input state
            if len(state) != 6:
                raise ValueError(f"Expected state vector of length 6, got {len(state)}")

            # Call the underlying controller with the full interface
            result = self.controller.compute_control(state, (), {})

            # Extract control value and return as numpy array
            if hasattr(result, 'u'):
                u = result.u
            elif isinstance(result, dict) and 'u' in result:
                u = result['u']
            else:
                u = result

            # Apply saturation at wrapper level for extra safety
            if isinstance(u, (int, float)):
                u_saturated = np.clip(u, -self.max_force, self.max_force)
                return np.array([u_saturated])
            elif isinstance(u, np.ndarray):
                if u.shape == ():
                    u_saturated = np.clip(float(u), -self.max_force, self.max_force)
                    return np.array([u_saturated])
                elif u.shape == (1,):
                    u_saturated = np.clip(u[0], -self.max_force, self.max_force)
                    return np.array([u_saturated])
                else:
                    u_saturated = np.clip(u.flatten()[0], -self.max_force, self.max_force)
                    return np.array([u_saturated])
            else:
                u_saturated = np.clip(float(u), -self.max_force, self.max_force)
                return np.array([u_saturated])

        except Exception as e:
            # Safe fallback control
            return np.array([0.0])


def create_smc_for_pso(smc_type: SMCType, gains: Union[list, np.ndarray], plant_config_or_model: Optional[Any] = None, **kwargs: Any) -> Any:
    """Create SMC controller optimized for PSO usage."""
    # Handle different calling patterns for backward compatibility
    dynamics_model = kwargs.get('dynamics_model', plant_config_or_model)
    max_force = kwargs.get('max_force', 150.0)
    dt = kwargs.get('dt', 0.001)

    config = SMCConfig(gains=gains, max_force=max_force, dt=dt, **kwargs)
    controller = SMCFactory.create_controller(smc_type, config)

    # Wrap the controller with PSO-compatible interface
    wrapper = PSOControllerWrapper(controller, len(gains), smc_type.value)
    return wrapper


def create_pso_controller_factory(smc_type: SMCType, plant_config: Optional[Any] = None, **kwargs: Any) -> Callable:
    """Create a PSO-optimized controller factory function with required attributes."""

    def controller_factory(gains: Union[list, np.ndarray]) -> Any:
        """Controller factory function optimized for PSO."""
        return create_smc_for_pso(smc_type, gains, plant_config, **kwargs)

    # Add PSO-required attributes to the factory function
    # Use expected gain counts that match what the controllers actually need
    controller_factory.n_gains = get_expected_gain_count(smc_type)
    controller_factory.controller_type = smc_type.value

    return controller_factory


def get_expected_gain_count(smc_type: SMCType) -> int:
    """Get expected number of gains for a controller type."""
    expected_counts = {
        SMCType.CLASSICAL: 6,
        SMCType.ADAPTIVE: 5,
        SMCType.SUPER_TWISTING: 6,
        SMCType.HYBRID: 4,
    }
    return expected_counts.get(smc_type, 6)


def get_gain_bounds_for_pso(smc_type: SMCType) -> Tuple[List[float], List[float]]:
    """Get PSO gain bounds for a controller type.

    Returns:
        Tuple of (lower_bounds, upper_bounds) lists
    """
    # Use controller-specific bounds based on control theory
    bounds_map = {
        SMCType.CLASSICAL: {
            'lower': [1.0, 1.0, 1.0, 1.0, 5.0, 0.1],   # [k1, k2, lam1, lam2, K, kd]
            'upper': [30.0, 30.0, 20.0, 20.0, 50.0, 10.0]
        },
        SMCType.ADAPTIVE: {
            'lower': [2.0, 2.0, 1.0, 1.0, 0.5],        # [k1, k2, lam1, lam2, gamma]
            'upper': [40.0, 40.0, 25.0, 25.0, 10.0]
        },
        SMCType.SUPER_TWISTING: {
            'lower': [3.0, 2.0, 2.0, 2.0, 0.5, 0.5],    # [K1, K2, k1, k2, lam1, lam2]
            'upper': [50.0, 30.0, 30.0, 30.0, 20.0, 20.0]
        },
        SMCType.HYBRID: {
            'lower': [2.0, 2.0, 1.0, 1.0],              # [k1, k2, lam1, lam2]
            'upper': [30.0, 30.0, 20.0, 20.0]
        }
    }

    if smc_type in bounds_map:
        return (bounds_map[smc_type]['lower'], bounds_map[smc_type]['upper'])
    else:
        # Fallback to default 6-gain bounds
        n_gains = 6
        lower_bounds = [0.1] * n_gains
        upper_bounds = [50.0] * n_gains
        return (lower_bounds, upper_bounds)


def validate_smc_gains(smc_type: SMCType, gains: Union[list, np.ndarray]) -> bool:
    """Validate gains for a controller type."""
    expected_lengths = {
        SMCType.CLASSICAL: 6,
        SMCType.ADAPTIVE: 5,
        SMCType.SUPER_TWISTING: 6,
        SMCType.HYBRID: 4,
    }
    expected_len = expected_lengths.get(smc_type, 6)
    return len(gains) == expected_len and all(isinstance(g, (int, float)) and g > 0 for g in gains)


# SMC Gain specifications - create spec objects with the expected interface
class SMCGainSpec:
    """SMC gain specification with expected interface."""
    def __init__(self, gain_names: List[str], gain_bounds: List[Tuple[float, float]], controller_type: str, n_gains: int):
        self.gain_names = gain_names
        self.gain_bounds = gain_bounds
        self.controller_type = controller_type
        self.n_gains = n_gains

SMC_GAIN_SPECS = {
    SMCType.CLASSICAL: SMCGainSpec(
        gain_names=['k1', 'k2', 'lambda1', 'lambda2', 'K', 'kd'],
        gain_bounds=[(1.0, 30.0), (1.0, 30.0), (1.0, 20.0), (1.0, 20.0), (5.0, 50.0), (0.1, 10.0)],
        controller_type='classical_smc',
        n_gains=6
    ),
    SMCType.ADAPTIVE: SMCGainSpec(
        gain_names=['k1', 'k2', 'lambda1', 'lambda2', 'gamma'],
        gain_bounds=[(2.0, 40.0), (2.0, 40.0), (1.0, 25.0), (1.0, 25.0), (0.5, 10.0)],
        controller_type='adaptive_smc',
        n_gains=5
    ),
    SMCType.SUPER_TWISTING: SMCGainSpec(
        gain_names=['K1', 'K2', 'k1', 'k2', 'lambda1', 'lambda2'],
        gain_bounds=[(3.0, 50.0), (2.0, 30.0), (2.0, 30.0), (2.0, 30.0), (0.5, 20.0), (0.5, 20.0)],
        controller_type='sta_smc',
        n_gains=6
    ),
    SMCType.HYBRID: SMCGainSpec(
        gain_names=['k1', 'k2', 'lambda1', 'lambda2'],
        gain_bounds=[(2.0, 30.0), (2.0, 30.0), (1.0, 20.0), (1.0, 20.0)],
        controller_type='hybrid_adaptive_sta_smc',
        n_gains=4
    )
}
