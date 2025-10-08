# Example from: docs\mathematical_foundations\validation_framework_guide.md
# Index: 10
# Runnable: True
# Hash: 2ce682ce

from src.controllers.smc.core.gain_validation import SMCGainValidator, validate_smc_gains

validator = SMCGainValidator()

# Classical SMC gains
classical_gains = [10.0, 5.0, 8.0, 3.0, 15.0, 2.0]
result = validator.validate_gains(classical_gains, "classical")

if result['valid']:
    print("✅ Gains valid for Classical SMC")
else:
    print(f"❌ Validation failed:")
    for violation in result['violations']:
        print(f"  - {violation['name']}: {violation['value']} not in {violation['bounds']}")

# Quick validation
is_valid = validate_smc_gains(classical_gains, "classical")  # Returns: True