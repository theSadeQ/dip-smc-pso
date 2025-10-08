# Example from: docs\factory\factory_api_reference.md
# Index: 33
# Runnable: True
# Hash: 559c16a0

from src.controllers.factory import create_controller, get_default_gains

def robust_controller_creation(controller_type, gains=None):
    """Robust controller creation with error recovery."""

    try:
        return create_controller(controller_type, gains=gains)

    except ValueError as e:
        if "gains" in str(e):
            # Use default gains on validation error
            default_gains = get_default_gains(controller_type)
            return create_controller(controller_type, gains=default_gains)
        else:
            raise

    except ImportError:
        # Fallback to basic controller type
        return create_controller('classical_smc', gains=gains)