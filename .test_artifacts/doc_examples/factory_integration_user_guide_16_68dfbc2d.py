# Example from: docs\factory\factory_integration_user_guide.md
# Index: 16
# Runnable: True
# Hash: 68dfbc2d

from src.controllers.factory import create_controller

def safe_controller_creation(controller_type, gains, config):
    """Validate parameters before creating controller."""

    # Pre-validation
    if not isinstance(gains, (list, tuple)):
        raise ValueError("Gains must be a list or tuple")

    if not all(isinstance(g, (int, float)) for g in gains):
        raise ValueError("All gains must be numeric")

    if any(g <= 0 for g in gains):
        raise ValueError("All gains must be positive")

    # Create controller after validation
    return create_controller(
        controller_type=controller_type,
        config=config,
        gains=gains
    )