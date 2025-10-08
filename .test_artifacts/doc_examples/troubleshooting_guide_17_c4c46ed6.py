# Example from: docs\factory\troubleshooting_guide.md
# Index: 17
# Runnable: True
# Hash: c4c46ed6

def validate_before_creation(controller_type, gains, config=None):
    """Comprehensive pre-creation validation."""

    from src.controllers.factory import (
        list_available_controllers,
        CONTROLLER_REGISTRY,
        validate_smc_gains,
        SMCType
    )

    errors = []
    warnings = []

    # Controller type validation
    if controller_type not in list_available_controllers():
        errors.append(f"Unknown controller type: {controller_type}")

    # Gains validation
    if gains is not None:
        if controller_type in CONTROLLER_REGISTRY:
            expected_count = CONTROLLER_REGISTRY[controller_type]['gain_count']
            if len(gains) != expected_count:
                errors.append(f"Expected {expected_count} gains, got {len(gains)}")

            if not all(isinstance(g, (int, float)) for g in gains):
                errors.append("All gains must be numeric")

            if any(g <= 0 for g in gains):
                errors.append("All gains must be positive")

    # Configuration validation
    if config is not None:
        # Add configuration-specific validation
        pass

    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings
    }

# Example usage
validation = validate_before_creation('classical_smc', [10, 5, 8, 3, 15, 2])
if not validation['valid']:
    print("Validation errors:")
    for error in validation['errors']:
        print(f"  - {error}")