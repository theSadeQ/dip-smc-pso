# Example from: docs\factory\migration_guide.md
# Index: 11
# Runnable: False
# Hash: 1b499c92

def fix_missing_parameters(controller_type: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Add missing required parameters with safe defaults."""

    required_defaults = {
        'classical_smc': {
            'boundary_layer': 0.02,
            'max_force': 150.0,
            'dt': 0.001
        },
        'adaptive_smc': {
            'leak_rate': 0.01,
            'adapt_rate_limit': 10.0,
            'K_min': 0.1,
            'K_max': 100.0,
            'K_init': 10.0,
            'alpha': 0.5,
            'max_force': 150.0,
            'dt': 0.001
        },
        'sta_smc': {
            'power_exponent': 0.5,
            'regularization': 1e-6,
            'boundary_layer': 0.01,
            'switch_method': 'tanh',
            'max_force': 150.0,
            'dt': 0.001
        }
    }

    if controller_type in required_defaults:
        for param, default_value in required_defaults[controller_type].items():
            config.setdefault(param, default_value)

    return config