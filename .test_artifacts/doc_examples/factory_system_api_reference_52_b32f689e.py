# Example from: docs\api\factory_system_api_reference.md
# Index: 52
# Runnable: False
# Hash: b32f689e

# example-metadata:
# runnable: false

def _get_controller_info(controller_type: str) -> Dict[str, Any]:
    if controller_type not in CONTROLLER_REGISTRY:
        available = list(CONTROLLER_REGISTRY.keys())
        raise ValueError(
            f"Unknown controller type '{controller_type}'. "
            f"Available: {available}"
        )

    controller_info = CONTROLLER_REGISTRY[controller_type].copy()

    if controller_info['class'] is None:
        if controller_type == 'mpc_controller':
            raise ImportError("MPC controller missing optional dependency")
        else:
            raise ImportError(f"Controller class for {controller_type} is not available")

    return controller_info