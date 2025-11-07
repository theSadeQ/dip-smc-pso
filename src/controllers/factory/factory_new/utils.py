#======================================================================================\
#=================== src/controllers/factory/factory_new/utils.py =====================\
#======================================================================================\

"""
Utility functions for controller factory.

This module provides utility functions for dynamics model creation,
gain counting, and PSO bounds generation.

Extracted from monolithic core.py (1,435 lines) during Phase 2 refactor.
"""

# Standard library imports
from typing import Any, List, Optional, Tuple

# Local imports - Core dynamics
from src.core.dynamics import DIPDynamics

# Local imports - Type definitions
from .types import SMCType

# =============================================================================
# DYNAMICS MODEL UTILITIES
# =============================================================================

def _create_dynamics_model(config: Any) -> Optional[Any]:
    """Create dynamics model from configuration.

    Args:
        config: Configuration object

    Returns:
        Dynamics model instance or None
    """
    # Try to get existing dynamics model
    if hasattr(config, 'dynamics_model'):
        return config.dynamics_model
    elif hasattr(config, 'physics'):
        return DIPDynamics(config.physics)
    elif hasattr(config, 'dip_params'):
        return DIPDynamics(config.dip_params)
    return None

# =============================================================================
# GAIN UTILITIES
# =============================================================================

def get_expected_gain_count(smc_type: SMCType) -> int:
    """Get expected number of gains for a controller type.

    Args:
        smc_type: SMC controller type

    Returns:
        Expected number of gains
    """
    expected_counts = {
        SMCType.CLASSICAL: 6,
        SMCType.ADAPTIVE: 5,
        SMCType.SUPER_TWISTING: 6,
        SMCType.HYBRID: 4,
    }
    return expected_counts.get(smc_type, 6)

def get_gain_bounds_for_pso(smc_type: SMCType) -> Tuple[List[float], List[float]]:
    """Get PSO gain bounds for a controller type.

    Args:
        smc_type: SMC controller type

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
            # K1 > K2 constraint: K1 in [2.0, 50.0], K2 in [1.0, 49.0] ensures K1 > K2
            'lower': [2.0, 1.0, 2.0, 2.0, 0.5, 0.5],    # [K1, K2, k1, k2, lam1, lam2]
            'upper': [50.0, 49.0, 30.0, 30.0, 20.0, 20.0]
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
