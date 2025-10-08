# Example from: docs\PATTERNS.md
# Index: 1
# Runnable: False
# Hash: a1a93fcd

# example-metadata:
# runnable: false

# src/controllers/factory.py (lines 507-543)

def create_controller(controller_type: str,
                     config: Optional[Any] = None,
                     gains: Optional[Union[list, np.ndarray]] = None) -> Any:
    """
    Create a controller instance of the specified type.

    This function is thread-safe and can be called concurrently.

    Supported types: 'classical_smc', 'sta_smc', 'adaptive_smc',
                     'hybrid_adaptive_sta_smc', 'mpc_controller'
    """
    # Normalize controller type (handles aliases)
    controller_type = _canonicalize_controller_type(controller_type)

    # Retrieve from registry
    controller_info = _get_controller_info(controller_type)
    controller_class = controller_info['class']

    # Resolve gains from config/defaults
    controller_gains = _resolve_controller_gains(gains, config, controller_type)

    # Validate gains with controller-specific rules
    _validate_controller_gains(controller_gains, controller_info)

    # Create and return configured instance
    return controller_class(controller_gains, **kwargs)