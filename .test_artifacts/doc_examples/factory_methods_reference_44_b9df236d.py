# Example from: docs\api\factory_methods_reference.md
# Index: 44
# Runnable: False
# Hash: b9df236d

# example-metadata:
# runnable: false

def create_controller_safely(controller_type: str, **kwargs) -> Optional[Any]:
    """Create controller with comprehensive error handling."""
    try:
        return create_controller(controller_type, **kwargs)
    except ValueError as e:
        logger.error(f"Configuration error for {controller_type}: {e}")
        return None
    except ImportError as e:
        logger.warning(f"Import error for {controller_type}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error creating {controller_type}: {e}")
        return None