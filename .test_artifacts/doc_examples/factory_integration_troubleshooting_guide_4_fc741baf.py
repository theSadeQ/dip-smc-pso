# Example from: docs\factory_integration_troubleshooting_guide.md
# Index: 4
# Runnable: False
# Hash: fc741baf

# example-metadata:
# runnable: false

def safe_create_controller(preferred_types, **kwargs):
    """Create controller with fallback options."""
    available = list_available_controllers()

    for controller_type in preferred_types:
        if controller_type in available:
            try:
                return create_controller(controller_type, **kwargs)
            except Exception as e:
                print(f"Failed to create {controller_type}: {e}")
                continue

    raise RuntimeError(f"None of {preferred_types} could be created. Available: {available}")

# Usage with fallbacks
controller = safe_create_controller(['classical_smc', 'adaptive_smc'])