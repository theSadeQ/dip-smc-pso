# Example from: docs\troubleshooting\hybrid_smc_runtime_fix.md
# Index: 16
# Runnable: False
# Hash: 99a26068

# Enhanced factory with type checking
def create_controller(controller_type: str, **kwargs):
    """Create controller with enhanced validation."""

    controller = _create_controller_impl(controller_type, **kwargs)

    # Validation wrapper
    original_compute_control = controller.compute_control

    def validated_compute_control(*args, **kwargs):
        result = original_compute_control(*args, **kwargs)

        # Type validation
        if result is None:
            raise TypeError(f"{controller_type} compute_control returned None")

        if not hasattr(result, 'control'):
            raise TypeError(f"{controller_type} result missing 'control' attribute")

        return result

    controller.compute_control = validated_compute_control
    return controller