# Example from: docs\api\factory_system_api_reference.md
# Index: 56
# Runnable: True
# Hash: e2efccc1

from src.controllers.factory import create_controller, list_available_controllers

def create_controller_safely(controller_type, config=None, gains=None):
    """Create controller with comprehensive error handling."""
    try:
        # Check availability first
        if controller_type not in list_available_controllers():
            print(f"Warning: {controller_type} not available")
            return None

        # Attempt creation
        controller = create_controller(controller_type, config, gains)
        return controller

    except ValueError as e:
        print(f"Validation error: {e}")
        return None

    except ImportError as e:
        print(f"Dependency error: {e}")
        return None

    except Exception as e:
        print(f"Unexpected error: {e}")
        return None