# Example from: docs\controllers\factory_system_guide.md
# Index: 19
# Runnable: False
# Hash: db316252

# example-metadata:
# runnable: false

def _extract_controller_parameters(config, controller_type, controller_info):
    """Extract controller-specific parameters from configuration."""

    if hasattr(config, 'controllers') and controller_type in config.controllers:
        controller_config = config.controllers[controller_type]

        # Pydantic model
        if hasattr(controller_config, 'model_dump'):
            return controller_config.model_dump()

        # Dictionary
        elif isinstance(controller_config, dict):
            return controller_config.copy()

        # Object with attributes
        else:
            return {
                attr: getattr(controller_config, attr)
                for attr in dir(controller_config)
                if not attr.startswith('_') and not callable(getattr(controller_config, attr))
            }

    return {}