# Example from: docs\reports\GITHUB_ISSUE_HYBRID_SMC_RESOLUTION_REPORT.md
# Index: 10
# Runnable: False
# Hash: 6c6ce954

# example-metadata:
# runnable: false

def create_controller_with_validation(controller_type: str, **kwargs):
    """Create controller with enhanced output validation."""
    controller = _create_controller_impl(controller_type, **kwargs)

    # Wrap compute_control with validation
    original_method = controller.compute_control

    def validated_compute_control(*args, **kwargs):
        result = original_method(*args, **kwargs)

        if result is None:
            raise TypeError(f"{controller_type}: compute_control returned None")

        if not hasattr(result, 'control'):
            raise TypeError(f"{controller_type}: Missing control attribute")

        return result

    controller.compute_control = validated_compute_control
    return controller