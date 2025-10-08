# Example from: docs\technical\controller_factory_integration.md
# Index: 18
# Runnable: False
# Hash: 269441f2

def get_gain_bounds_for_pso(smc_type: SMCType) -> Tuple[List[float], List[float]]:
    """Get PSO gain bounds based on control theory constraints."""

    bounds_map = {
        SMCType.CLASSICAL: {
            'lower': [0.1, 0.1, 0.1, 0.1, 1.0, 0.0],   # [c1, λ1, c2, λ2, K, kd]
            'upper': [50.0, 50.0, 50.0, 50.0, 200.0, 50.0]
        },
        SMCType.SUPER_TWISTING: {
            'lower': [1.0, 1.0, 0.1, 0.1, 0.1, 0.1],    # [K1, K2, c1, λ1, c2, λ2]
            'upper': [100.0, 100.0, 50.0, 50.0, 50.0, 50.0]
        }
    }

    return bounds_map.get(smc_type, default_bounds)