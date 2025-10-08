# Example from: docs\analysis\CONTROLLER_FACTORY_ANALYSIS.md
# Index: 11
# Runnable: False
# Hash: 1a222e08

# example-metadata:
# runnable: false

# File: src/controllers/factory.py
def list_available_controllers() -> list:
    """Get list of available controller types."""
    available_controllers = []
    for controller_type, controller_info in CONTROLLER_REGISTRY.items():
        # Only include controllers that have available classes AND are not placeholders
        if (controller_info['class'] is not None and
            controller_type != 'mpc_controller'):  # Exclude optional MPC
            available_controllers.append(controller_type)
    return available_controllers