# Example from: docs\factory\parameter_interface_specification.md
# Index: 10
# Runnable: False
# Hash: 3dd2db87

class ParameterResolutionError(ValueError):
    """Raised when parameter resolution fails."""
    pass

class GainValidationError(ValueError):
    """Raised when gain validation fails."""
    pass

def create_controller_with_parameter_recovery(
    controller_type: str,
    config: Optional[Any] = None,
    gains: Optional[Union[list, np.ndarray]] = None
) -> Any:
    """Create controller with comprehensive parameter recovery."""

    try:
        # Primary creation attempt
        return create_controller(controller_type, config, gains)

    except GainValidationError as e:
        logger.warning(f"Gain validation failed: {e}")

        # Attempt recovery with default gains
        default_gains = get_default_gains(controller_type)
        logger.info(f"Falling back to default gains: {default_gains}")
        return create_controller(controller_type, config, default_gains)

    except ParameterResolutionError as e:
        logger.warning(f"Parameter resolution failed: {e}")

        # Attempt recovery with minimal configuration
        minimal_config = create_minimal_config(controller_type)
        return create_controller(controller_type, minimal_config, gains)

    except Exception as e:
        logger.error(f"Controller creation failed completely: {e}")
        raise