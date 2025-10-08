# Example from: docs\factory_integration_documentation.md
# Index: 11
# Runnable: False
# Hash: e890712a

def create_controller(controller_type: str, config: Optional[Any] = None,
                     gains: Optional[Union[list, np.ndarray]] = None) -> Any:
    """Create controller with graceful degradation."""

    try:
        # Attempt full configuration creation
        controller_config = create_full_config(controller_type, config, gains)
        return controller_class(controller_config)

    except Exception as e:
        logger.warning(f"Full config creation failed: {e}. Using minimal config.")

        # Fallback to minimal configuration
        minimal_config = create_minimal_config(controller_type, gains)
        return controller_class(minimal_config)