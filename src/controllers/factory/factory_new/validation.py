#======================================================================================\
#================ src/controllers/factory/factory_new/validation.py ===================\
#======================================================================================\

"""
Validation functions for controller factory.

This module provides validation logic for controller gains, parameters,
and configuration.

Extracted from monolithic core.py (1,435 lines) during Phase 2 refactor.
"""

# Standard library imports
import logging
from typing import Any, Dict, List, Optional, Union

# Third-party imports
import numpy as np

# Local imports - Type definitions
from .types import ConfigValueError, SMCType

# =============================================================================
# MODULE-LEVEL LOGGER
# =============================================================================

logger = logging.getLogger(__name__)

# =============================================================================
# GAIN RESOLUTION AND VALIDATION
# =============================================================================

def _resolve_controller_gains(
    gains: Optional[Union[List[float], np.ndarray]],
    config: Optional[Any],
    controller_type: str,
    controller_info: Dict[str, Any]
) -> List[float]:
    """Resolve controller gains from multiple sources.

    Args:
        gains: Explicitly provided gains
        config: Configuration object
        controller_type: Controller type name
        controller_info: Controller registry information

    Returns:
        Resolved gains list
    """
    if gains is not None:
        if isinstance(gains, np.ndarray):
            gains = gains.tolist()
        return gains

    # Try to extract gains from config
    if config is not None:
        try:
            # Try different config structures
            if hasattr(config, 'controller_defaults'):
                defaults = config.controller_defaults
                if isinstance(defaults, dict) and controller_type in defaults:
                    config_gains = defaults[controller_type].get('gains')
                    if config_gains is not None:
                        return config_gains
                elif hasattr(defaults, controller_type):
                    controller_config = getattr(defaults, controller_type)
                    if hasattr(controller_config, 'gains'):
                        return controller_config.gains

            elif hasattr(config, 'controllers'):
                controllers = config.controllers
                if isinstance(controllers, dict) and controller_type in controllers:
                    config_gains = controllers[controller_type].get('gains')
                    if config_gains is not None:
                        return config_gains
                elif hasattr(controllers, controller_type):
                    controller_config = getattr(controllers, controller_type)
                    if hasattr(controller_config, 'gains'):
                        return controller_config.gains
        except Exception as e:
            # OK: Config loading optional - fall back to default gains
            logger.debug(f"Could not load config gains for {controller_type}, using defaults: {e}")

    return controller_info['default_gains']

def _validate_controller_gains(
    gains: List[float],
    controller_info: Dict[str, Any],
    controller_type: str
) -> None:
    """Validate controller gains with controller-specific rules.

    Args:
        gains: Controller gains to validate
        controller_info: Controller registry information
        controller_type: Type of controller for specific validation

    Raises:
        ValueError: If gains are invalid
    """
    expected_count = controller_info['gain_count']
    if len(gains) != expected_count:
        raise ValueError(
            f"Controller '{controller_info.get('description', 'unknown')}' "
            f"requires {expected_count} gains, got {len(gains)}"
        )

    if not all(isinstance(g, (int, float)) and np.isfinite(g) for g in gains):
        raise ValueError("All gains must be finite numbers")

    if any(g <= 0 for g in gains):
        raise ValueError("All gains must be positive")

    # Controller-specific validation rules
    if controller_type == 'sta_smc' and len(gains) >= 2:
        K1, K2 = gains[0], gains[1]
        if K1 <= K2:
            raise ValueError("Super-Twisting stability requires K1 > K2 > 0")

    elif controller_type == 'adaptive_smc' and len(gains) != 5:
        raise ValueError("Adaptive SMC requires exactly 5 gains: [k1, k2, lam1, lam2, gamma]")

def validate_smc_gains(smc_type: SMCType, gains: Union[list, np.ndarray]) -> bool:
    """Validate gains for a controller type.

    Args:
        smc_type: SMC controller type
        gains: Gains to validate

    Returns:
        True if gains are valid, False otherwise
    """
    expected_lengths = {
        SMCType.CLASSICAL: 6,
        SMCType.ADAPTIVE: 5,
        SMCType.SUPER_TWISTING: 6,
        SMCType.HYBRID: 4,
    }
    expected_len = expected_lengths.get(smc_type, 6)
    return len(gains) == expected_len and all(isinstance(g, (int, float)) and g > 0 for g in gains)

# =============================================================================
# PARAMETER EXTRACTION AND VALIDATION
# =============================================================================

def _extract_controller_parameters(
    config: Optional[Any],
    controller_type: str,
    controller_info: Dict[str, Any]
) -> Dict[str, Any]:
    """Extract controller-specific parameters from configuration.

    Args:
        config: Configuration object
        controller_type: Controller type name
        controller_info: Controller registry information

    Returns:
        Dictionary of controller parameters
    """
    if config is None:
        return {}

    controller_params = {}

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
        # OK: Config introspection optional - return empty params
        logger.debug(f"Could not extract controller params from config: {e}")

    return controller_params

def _validate_mpc_parameters(config_params: Dict[str, Any], controller_params: Dict[str, Any]) -> None:
    """Validate MPC controller parameters.

    Args:
        config_params: Main configuration parameters
        controller_params: Controller-specific parameters

    Raises:
        ConfigValueError: If any parameter is invalid
    """
    # Merge parameters from both sources
    all_params = {**config_params, **controller_params}

    # Validate horizon parameter
    if 'horizon' in all_params:
        horizon = all_params['horizon']
        if not isinstance(horizon, int):
            raise ConfigValueError("horizon must be an integer")
        if horizon < 1:
            raise ConfigValueError("horizon must be ≥ 1")

    # Validate geometric constraints
    if 'max_cart_pos' in all_params:
        max_cart_pos = all_params['max_cart_pos']
        if not isinstance(max_cart_pos, (int, float)) or max_cart_pos <= 0:
            raise ConfigValueError("max_cart_pos must be > 0")
