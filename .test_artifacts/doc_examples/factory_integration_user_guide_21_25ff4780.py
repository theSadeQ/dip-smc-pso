# Example from: docs\factory\factory_integration_user_guide.md
# Index: 21
# Runnable: True
# Hash: 25ff4780

from src.controllers.factory.core.validation import validate_controller_parameters

# Detailed parameter validation
validation_result = validate_controller_parameters(
    controller_type='classical_smc',
    gains=[20.0, 15.0, 12.0, 8.0, 35.0, 5.0],
    max_force=150.0
)

if not validation_result.is_valid:
    print("Validation issues:")
    for issue in validation_result.issues:
        print(f"  - {issue}")