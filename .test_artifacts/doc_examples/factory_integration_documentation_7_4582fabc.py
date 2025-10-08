# Example from: docs\factory_integration_documentation.md
# Index: 7
# Runnable: False
# Hash: 4582fabc

# example-metadata:
# runnable: false

def get_gain_bounds_for_pso(smc_type: SMCType) -> Tuple[List[float], List[float]]:
    """Get PSO gain bounds for a controller type."""
    bounds_map = {
        SMCType.CLASSICAL: {
            'lower': [1.0, 1.0, 1.0, 1.0, 5.0, 0.1],   # [k1, k2, lam1, lam2, K, kd]
            'upper': [30.0, 30.0, 20.0, 20.0, 50.0, 10.0]
        },
        SMCType.ADAPTIVE: {
            'lower': [2.0, 2.0, 1.0, 1.0, 0.5],        # [k1, k2, lam1, lam2, gamma]
            'upper': [40.0, 40.0, 25.0, 25.0, 10.0]
        },
        # ... additional controller types
    }
    return (bounds_map[smc_type]['lower'], bounds_map[smc_type]['upper'])