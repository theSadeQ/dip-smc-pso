# Example from: docs\factory_integration_troubleshooting_guide.md
# Index: 7
# Runnable: True
# Hash: d2bee562

def validate_controller_parameters(controller_type, **params):
    """Validate parameters before controller creation."""

    from src.controllers.factory import CONTROLLER_REGISTRY

    controller_info = CONTROLLER_REGISTRY[controller_type]
    required_params = controller_info['required_params']

    # Check required parameters
    missing = set(required_params) - set(params.keys())
    if missing:
        print(f"Missing required parameters: {missing}")
        return False

    # Controller-specific validation
    if controller_type == 'classical_smc':
        if 'gains' in params and len(params['gains']) != 6:
            print("Classical SMC requires exactly 6 gains")
            return False

        if 'boundary_layer' in params and params['boundary_layer'] <= 0:
            print("Boundary layer must be positive")
            return False

    elif controller_type == 'mpc_controller':
        if 'horizon' in params and (not isinstance(params['horizon'], int) or params['horizon'] < 1):
            print("MPC horizon must be positive integer")
            return False

    return True

# Usage
params = {'gains': [20, 15, 12, 8, 35, 5], 'max_force': 150.0, 'boundary_layer': 0.02}
if validate_controller_parameters('classical_smc', **params):
    controller = create_controller('classical_smc', **params)