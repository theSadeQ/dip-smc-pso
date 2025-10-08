# Example from: docs\factory\enhanced_factory_api_reference.md
# Index: 13
# Runnable: True
# Hash: 502dcf6d

def get_gain_bounds_for_pso(smc_type: SMCType) -> Tuple[List[float], List[float]]:
    """
    Returns (lower_bounds, upper_bounds) for PSO optimization.

    Based on control theory constraints and practical limits.
    """