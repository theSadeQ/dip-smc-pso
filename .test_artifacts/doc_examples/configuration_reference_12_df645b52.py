# Example from: docs\factory\configuration_reference.md
# Index: 12
# Runnable: False
# Hash: df645b52

def create_controller_with_recovery(controller_type: str, config: Any, gains: Any) -> Any:
    """Create controller with automatic error recovery."""

    try:
        return create_controller(controller_type, config, gains)
    except Exception as primary_error:
        logger.warning(f"Primary creation failed: {primary_error}")

        # Attempt recovery with minimal configuration
        try:
            minimal_config = create_minimal_config(controller_type, gains)
            return create_controller(controller_type, minimal_config, None)
        except Exception as recovery_error:
            logger.error(f"Recovery failed: {recovery_error}")
            raise primary_error