# Example from: docs\api\factory_system_api_reference.md
# Index: 45
# Runnable: False
# Hash: b4b06e6b

# example-metadata:
# runnable: false

def _validate_mpc_parameters(config_params, controller_params):
    all_params = {**config_params, **controller_params}

    # Horizon validation
    if 'horizon' in all_params:
        horizon = all_params['horizon']
        if not isinstance(horizon, int):
            raise ConfigValueError("horizon must be an integer")
        if horizon < 1:
            raise ConfigValueError("horizon must be ≥ 1")

    # Weight parameters must be non-negative
    weight_params = ['q_x', 'q_theta', 'r_u']
    for param in weight_params:
        if param in all_params:
            value = all_params[param]
            if not isinstance(value, (int, float)) or value < 0:
                raise ConfigValueError(f"{param} must be ≥ 0")