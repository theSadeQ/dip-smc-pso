# Example from: docs\factory_integration_troubleshooting_guide.md
# Index: 15
# Runnable: False
# Hash: b93a7f75

# example-metadata:
# runnable: false

def validate_and_clean_config(controller_type, config):
    """Validate and clean configuration object."""

    cleaned_config = {}
    warnings = []

    # Extract controller-specific configuration
    try:
        if hasattr(config, 'controllers') and controller_type in config.controllers:
            controller_config = config.controllers[controller_type]

            # Handle different config types
            if hasattr(controller_config, 'model_dump'):
                # Pydantic model
                cleaned_config = controller_config.model_dump()
            elif isinstance(controller_config, dict):
                # Dictionary
                cleaned_config = controller_config.copy()
            else:
                # Object with attributes
                cleaned_config = {
                    attr: getattr(controller_config, attr)
                    for attr in dir(controller_config)
                    if not attr.startswith('_') and not callable(getattr(controller_config, attr))
                }

    except Exception as e:
        warnings.append(f"Config extraction failed: {e}")

    # Validate parameters
    if 'gains' in cleaned_config:
        gains = cleaned_config['gains']
        if not isinstance(gains, (list, tuple)) or len(gains) == 0:
            warnings.append("Invalid gains format")
            del cleaned_config['gains']

    if 'max_force' in cleaned_config:
        if not isinstance(cleaned_config['max_force'], (int, float)) or cleaned_config['max_force'] <= 0:
            warnings.append("Invalid max_force value")
            cleaned_config['max_force'] = 150.0  # Default

    # Handle deprecated parameters
    deprecated_mappings = {
        'use_equivalent': 'enable_equivalent_control',
        'k_gain': 'switching_gain',
        'lambda_gains': 'surface_gains'
    }

    for old_param, new_param in deprecated_mappings.items():
        if old_param in cleaned_config:
            cleaned_config[new_param] = cleaned_config.pop(old_param)
            warnings.append(f"Deprecated parameter '{old_param}' migrated to '{new_param}'")

    if warnings:
        print("Configuration warnings:")
        for warning in warnings:
            print(f"  ⚠️  {warning}")

    return cleaned_config

# Usage
config = load_config("config.yaml")
cleaned = validate_and_clean_config('classical_smc', config)
controller = create_controller('classical_smc', **cleaned)