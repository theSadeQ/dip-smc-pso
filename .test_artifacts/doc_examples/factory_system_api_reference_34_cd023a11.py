# Example from: docs\api\factory_system_api_reference.md
# Index: 34
# Runnable: False
# Hash: cd023a11

# example-metadata:
# runnable: false

def get_gain_bounds_for_pso(smc_type: SMCType) -> Tuple[List[float], List[float]]:
    """Get PSO gain bounds for a controller type.

    Returns:
        Tuple of (lower_bounds, upper_bounds) lists
    """
    bounds_map = {
        SMCType.CLASSICAL: {
            'lower': [1.0, 1.0, 1.0, 1.0, 5.0, 0.1],
            'upper': [30.0, 30.0, 20.0, 20.0, 50.0, 10.0]
        },
        SMCType.ADAPTIVE: {
            'lower': [2.0, 2.0, 1.0, 1.0, 0.5],
            'upper': [40.0, 40.0, 25.0, 25.0, 10.0]
        },
        SMCType.SUPER_TWISTING: {
            # K1 > K2 constraint: K1 in [2.0, 50.0], K2 in [1.0, 49.0]
            'lower': [2.0, 1.0, 2.0, 2.0, 0.5, 0.5],
            'upper': [50.0, 49.0, 30.0, 30.0, 20.0, 20.0]
        },
        SMCType.HYBRID: {
            'lower': [2.0, 2.0, 1.0, 1.0],
            'upper': [30.0, 30.0, 20.0, 20.0]
        }
    }
    return (bounds_map[smc_type]['lower'], bounds_map[smc_type]['upper'])