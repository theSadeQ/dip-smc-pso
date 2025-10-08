# Example from: docs\controllers\factory_system_guide.md
# Index: 28
# Runnable: False
# Hash: 8dbd5cfa

# example-metadata:
# runnable: false

# If config creation fails, use fallback with ALL required parameters
try:
    controller_config = config_class(**config_params)
except Exception as e:
    if controller_type == 'classical_smc':
        fallback_params = {
            'gains': controller_gains,
            'max_force': 150.0,
            'dt': 0.001,
            'boundary_layer': 0.02,  # Required
            'regularization_alpha': 1e-4,
            'min_regularization': 1e-10,
            'max_condition_number': 1e14,
            'use_adaptive_regularization': True
        }

    controller_config = config_class(**fallback_params)