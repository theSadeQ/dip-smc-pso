# Example from: docs\api\factory_methods_reference.md
# Index: 27
# Runnable: False
# Hash: 8c2c3a0f

CONTROLLER_REGISTRY = {
    'controller_type': {
        'class': ControllerClass,              # Implementation class
        'config_class': ConfigClass,           # Configuration class
        'default_gains': [float, ...],         # Default gain values
        'gain_count': int,                     # Expected number of gains
        'description': str,                    # Human-readable description
        'supports_dynamics': bool,             # Supports dynamics model
        'required_params': [str, ...]          # Required parameters
    }
}