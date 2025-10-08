# Example from: docs\api\factory_methods_reference.md
# Index: 45
# Runnable: False
# Hash: 0ad1afef

def create_best_available_controller(preferred_types: List[str]) -> Any:
    """Create first available controller from preference list."""
    available = list_available_controllers()

    for controller_type in preferred_types:
        if controller_type in available:
            try:
                return create_controller(controller_type)
            except Exception as e:
                logger.warning(f"Failed to create {controller_type}: {e}")
                continue

    # Fallback to any available controller
    if available:
        return create_controller(available[0])
    else:
        raise RuntimeError("No controllers available")