# Example from: docs\technical\controller_factory_integration.md
# Index: 12
# Runnable: True
# Hash: 52196fbf

def validate_configuration(config_obj):
    """Validate configuration object after creation."""

    try:
        # Use config class validation
        config_obj._validate_gains()
        config_obj._validate_parameters()
    except ValidationError as e:
        logger.warning(f"Configuration validation failed: {e}")
        raise ConfigurationError(f"Invalid configuration: {e}")