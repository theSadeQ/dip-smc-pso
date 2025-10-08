# Example from: docs\factory\configuration_reference.md
# Index: 10
# Runnable: False
# Hash: 9e90171f

# example-metadata:
# runnable: false

try:
    # Attempt full configuration
    controller_config = config_class(**config_params)
except Exception as e:
    logger.warning(f"Could not create full config, using minimal config: {e}")

    # Fallback to minimal configuration
    fallback_params = {
        'gains': controller_gains,
        'max_force': 150.0,
        'dt': 0.001
    }

    # Add controller-specific required parameters
    if controller_type == 'classical_smc':
        fallback_params['boundary_layer'] = 0.02

    controller_config = config_class(**fallback_params)