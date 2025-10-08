# Example from: docs\technical\controller_factory_integration.md
# Index: 13
# Runnable: False
# Hash: abe1e17f

def create_fallback_configuration(controller_type, gains):
    """Create minimal working configuration when full config fails."""

    fallback_params = {
        'gains': gains,
        'max_force': 150.0,  # Safe default
        'dt': 0.001,         # Standard timestep
    }

    # Add controller-specific required parameters
    if controller_type == 'classical_smc':
        fallback_params['boundary_layer'] = 0.02
    elif controller_type == 'sta_smc':
        fallback_params['K1'] = 4.0
        fallback_params['K2'] = 0.4

    return controller_info['config_class'](**fallback_params)