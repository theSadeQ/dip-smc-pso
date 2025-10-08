# Example from: docs\api\factory_system_api_reference.md
# Index: 57
# Runnable: True
# Hash: fd0f3b26

from src.controllers.factory import get_gain_bounds_for_pso, SMCType
import numpy as np

def validate_pso_particle(gains, smc_type):
    """Validate PSO particle before fitness evaluation."""
    # Get bounds for controller type
    lower_bounds, upper_bounds = get_gain_bounds_for_pso(smc_type)

    # Check bounds
    gains = np.array(gains)
    if np.any(gains < lower_bounds) or np.any(gains > upper_bounds):
        return False

    # Check controller-specific constraints
    if smc_type == SMCType.SUPER_TWISTING:
        if gains[0] <= gains[1]:  # K1 must be > K2
            return False

    return True