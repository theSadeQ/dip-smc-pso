# Example from: docs\technical\factory_usage_examples.md
# Index: 18
# Runnable: True
# Hash: 1b9bddf0

from src.controllers.factory import create_controller

# Controllers with dynamics models are created only when needed
def create_controller_lazily(controller_type, gains):
    """Create controller with lazy dynamics loading."""

    # Dynamics model is only created when the controller needs it
    controller = create_controller(
        controller_type=controller_type,
        gains=gains
        # No explicit dynamics model - created automatically when needed
    )

    return controller

# Fast creation - dynamics loaded on first use
controller = create_controller_lazily('classical_smc', [8.0, 6.0, 4.0, 3.0, 15.0, 2.0])