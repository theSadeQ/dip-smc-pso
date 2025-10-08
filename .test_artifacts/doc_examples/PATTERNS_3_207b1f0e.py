# Example from: docs\PATTERNS.md
# Index: 3
# Runnable: False
# Hash: 207b1f0e

# example-metadata:
# runnable: false

# Controller registry with comprehensive metadata (lines 181-218)
CONTROLLER_REGISTRY = {
    'classical_smc': {
        'class': ClassicalSMC,
        'config_class': ClassicalSMCConfig,
        'default_gains': [20.0, 15.0, 12.0, 8.0, 35.0, 5.0],
        'gain_count': 6,
        'description': 'Classical sliding mode controller with boundary layer',
        'supports_dynamics': True,
        'required_params': ['gains', 'max_force', 'boundary_layer']
    },
    'sta_smc': { ... },
    'adaptive_smc': { ... },
    'hybrid_adaptive_sta_smc': { ... }
}