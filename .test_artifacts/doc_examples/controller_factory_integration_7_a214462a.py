# Example from: docs\technical\controller_factory_integration.md
# Index: 7
# Runnable: False
# Hash: a214462a

# example-metadata:
# runnable: false

def resolve_configuration(controller_type, config, gains):
    """Resolve configuration with fallback mechanisms."""

    # 1. Resolve gains
    if gains is not None:
        controller_gains = gains
    elif config and hasattr(config, 'controllers'):
        controller_gains = extract_gains_from_config(config, controller_type)
    else:
        controller_gains = get_default_gains(controller_type)

    # 2. Create configuration object
    try:
        return create_validated_config(controller_type, controller_gains, config)
    except ValidationError:
        return create_fallback_config(controller_type, controller_gains)