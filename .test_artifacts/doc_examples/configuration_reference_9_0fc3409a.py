# Example from: docs\factory\configuration_reference.md
# Index: 9
# Runnable: False
# Hash: 0fc3409a

# example-metadata:
# runnable: false

def validate_configuration(controller_type: str, config_params: Dict[str, Any]) -> None:
    """Comprehensive configuration validation."""

    # 1. Check required parameters
    controller_info = _get_controller_info(controller_type)
    required_params = controller_info['required_params']

    for param in required_params:
        if param not in config_params:
            raise ValueError(f"Missing required parameter: {param}")

    # 2. Validate gains
    gains = config_params.get('gains', [])
    _validate_controller_gains(gains, controller_info)

    # 3. Controller-specific validation
    if controller_type == 'classical_smc':
        if config_params.get('boundary_layer', 0) <= 0:
            raise ValueError("boundary_layer must be positive")

    # 4. Numerical validation
    for key, value in config_params.items():
        if key in ['max_force', 'dt', 'boundary_layer']:
            if not (isinstance(value, (int, float)) and value > 0):
                raise ValueError(f"{key} must be positive number")