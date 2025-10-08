# Example from: docs\factory\factory_integration_user_guide.md
# Index: 13
# Runnable: True
# Hash: c34dd024

from src.controllers.factory import create_controller

def create_controller_ensemble(gains_dict, config):
    """Create multiple controllers for ensemble methods."""

    controllers = {}

    for controller_type, gains in gains_dict.items():
        try:
            controllers[controller_type] = create_controller(
                controller_type=controller_type,
                config=config,
                gains=gains
            )
            print(f"✓ Created {controller_type} successfully")
        except Exception as e:
            print(f"✗ Failed to create {controller_type}: {e}")

    return controllers

# Example usage
gains_ensemble = {
    'classical_smc': [20.0, 15.0, 12.0, 8.0, 35.0, 5.0],
    'adaptive_smc': [25.0, 18.0, 15.0, 10.0, 4.0],
    'sta_smc': [25.0, 15.0, 20.0, 12.0, 8.0, 6.0]
}

ensemble = create_controller_ensemble(gains_ensemble, config)