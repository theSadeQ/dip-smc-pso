# Example from: docs\factory\parameter_interface_specification.md
# Index: 11
# Runnable: False
# Hash: 7b8b1dc9

# example-metadata:
# runnable: false

def create_minimal_config(controller_type: str) -> Dict[str, Any]:
    """Create minimal viable configuration for controller type."""

    base_config = {
        'max_force': 150.0,
        'dt': 0.001
    }

    # Add controller-specific minimal parameters
    if controller_type == 'classical_smc':
        base_config['boundary_layer'] = 0.02

    elif controller_type == 'adaptive_smc':
        base_config.update({
            'leak_rate': 0.01,
            'adapt_rate_limit': 10.0,
            'K_min': 0.1,
            'K_max': 100.0,
            'K_init': 10.0,
            'alpha': 0.5
        })

    elif controller_type == 'sta_smc':
        base_config.update({
            'power_exponent': 0.5,
            'regularization': 1e-6,
            'switch_method': 'tanh'
        })

    return base_config