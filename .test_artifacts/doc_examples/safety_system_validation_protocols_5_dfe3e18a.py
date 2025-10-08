# Example from: docs\safety_system_validation_protocols.md
# Index: 5
# Runnable: False
# Hash: dfe3e18a

# example-metadata:
# runnable: false

def verify_safety_branch_coverage():
    """Verify all safety-critical branches are tested."""
    safety_modules = [
        'src.utils.control.saturation',
        'src.utils.safety.emergency_stop',
        'src.utils.validation.parameter_validator'
    ]

    for module in safety_modules:
        coverage = get_branch_coverage(module)
        assert coverage == 100.0, f"Safety module {module} coverage: {coverage}%"