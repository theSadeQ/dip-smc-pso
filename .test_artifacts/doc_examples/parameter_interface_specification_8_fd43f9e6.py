# Example from: docs\factory\parameter_interface_specification.md
# Index: 8
# Runnable: False
# Hash: fd43f9e6

# example-metadata:
# runnable: false

def _extract_controller_parameters(
    config: Optional[Any],
    controller_type: str,
    controller_info: Dict[str, Any]
) -> Dict[str, Any]:
    """Extract controller-specific parameters from diverse configuration formats."""

    if config is None:
        return {}

    controller_params = {}

    try:
        # Method 1: Direct controller configuration
        if hasattr(config, 'controllers') and controller_type in config.controllers:
            controller_config = config.controllers[controller_type]

            # Pydantic model with model_dump()
            if hasattr(controller_config, 'model_dump'):
                controller_params = controller_config.model_dump()

            # Dictionary configuration
            elif isinstance(controller_config, dict):
                controller_params = controller_config.copy()

            # Object with attributes
            else:
                controller_params = {
                    attr: getattr(controller_config, attr)
                    for attr in dir(controller_config)
                    if not attr.startswith('_') and not callable(getattr(controller_config, attr))
                }

        # Method 2: Legacy controller_defaults structure
        elif hasattr(config, 'controller_defaults'):
            defaults = config.controller_defaults
            if isinstance(defaults, dict) and controller_type in defaults:
                controller_params = defaults[controller_type].copy()

    except Exception as e:
        logger.warning(f"Parameter extraction failed for {controller_type}: {e}")
        return {}

    return controller_params