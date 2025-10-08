# Example from: docs\architecture\controller_system_architecture.md
# Index: 2
# Runnable: False
# Hash: 59ce141a

def create_controller(
    controller_type: str,
    config: Optional[Dict[str, Any]] = None,
    gains: Optional[List[float]] = None,
    **kwargs
) -> ControllerInterface:
    """
    Universal controller factory with comprehensive validation.

    This factory method serves as the single entry point for all controller
    instantiation, providing type safety, configuration validation, and
    standardized error handling across all SMC variants.
    """

    # Step 1: Validate controller type
    if controller_type not in SUPPORTED_CONTROLLERS:
        raise ValueError(f"Unsupported controller: {controller_type}")

    # Step 2: Load and validate configuration
    controller_config = _prepare_controller_config(controller_type, config, **kwargs)

    # Step 3: Validate and apply gains
    if gains is not None:
        _validate_gains(controller_type, gains)
        controller_config = _apply_gains_to_config(controller_type, controller_config, gains)

    # Step 4: Instantiate controller with error handling
    try:
        controller_class = ControllerRegistry.get_controller_class(controller_type)
        controller = controller_class(**controller_config)

        # Step 5: Post-instantiation validation
        _validate_controller_interface(controller, controller_type)

        return controller

    except Exception as e:
        raise ControllerCreationError(
            f"Failed to create {controller_type} controller: {str(e)}"
        ) from e