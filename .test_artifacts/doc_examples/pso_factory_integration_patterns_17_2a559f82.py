# Example from: docs\pso_factory_integration_patterns.md
# Index: 17
# Runnable: False
# Hash: 2a559f82

# ✅ Good: Centralized PSO configuration
PSO_CONFIGS = {
    SMCType.CLASSICAL: {
        'n_particles': 30,
        'max_iter': 100,
        'w': 0.9,
        'c1': 2.0,
        'c2': 2.0,
        'early_stopping': True
    },
    SMCType.ADAPTIVE: {
        'n_particles': 40,
        'max_iter': 150,
        'w': 0.8,
        'c1': 2.2,
        'c2': 1.8,
        'early_stopping': True
    }
}

def get_pso_config(controller_type: SMCType) -> Dict[str, Any]:
    """Get optimized PSO configuration for controller type."""
    return PSO_CONFIGS.get(controller_type, PSO_CONFIGS[SMCType.CLASSICAL])