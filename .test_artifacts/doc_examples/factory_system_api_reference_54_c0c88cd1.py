# Example from: docs\api\factory_system_api_reference.md
# Index: 54
# Runnable: False
# Hash: c0c88cd1

# example-metadata:
# runnable: false

try:
    controller_config = config_class(**config_params)
except Exception as e:
    # Log failure and use fallback configuration
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(f"Could not create full config, using minimal config: {e}")

    # Fallback to minimal configuration with all required defaults
    fallback_params = {
        'gains': controller_gains,
        'max_force': 150.0,
        'dt': 0.001
    }

    # Add controller-specific required parameters
    if controller_type == 'classical_smc':
        fallback_params['boundary_layer'] = 0.02

    controller_config = config_class(**fallback_params)