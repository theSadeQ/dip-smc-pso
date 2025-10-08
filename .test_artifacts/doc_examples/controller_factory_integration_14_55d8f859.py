# Example from: docs\technical\controller_factory_integration.md
# Index: 14
# Runnable: False
# Hash: 55d8f859

# example-metadata:
# runnable: false

def safe_controller_creation(controller_class, config):
    """Create controller with error recovery."""

    try:
        return controller_class(config)
    except Exception as e:
        logger.error(f"Controller instantiation failed: {e}")

        # Try with minimal configuration
        minimal_config = create_minimal_config(config)
        try:
            return controller_class(minimal_config)
        except Exception as e2:
            logger.error(f"Minimal controller creation failed: {e2}")
            raise FactoryError(f"Cannot create controller: {e}, {e2}")