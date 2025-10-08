# Example from: docs\factory\configuration_reference.md
# Index: 18
# Runnable: True
# Hash: 7c49353b

def list_available_controllers() -> List[str]:
    """Get list of available controller types."""
    return list(CONTROLLER_REGISTRY.keys())

def get_default_gains(controller_type: str) -> List[float]:
    """Get default gains for a controller type."""
    return CONTROLLER_REGISTRY[controller_type]['default_gains'].copy()