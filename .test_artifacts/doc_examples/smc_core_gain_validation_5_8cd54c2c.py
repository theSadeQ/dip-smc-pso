# Example from: docs\reference\controllers\smc_core_gain_validation.md
# Index: 5
# Runnable: True
# Hash: 8cd54c2c

from src.controllers.smc.core.gain_validation import validate_all_criteria

# Validation configuration
validation_config = {
    'u_max': 100.0,         # Actuator limit (N)
    'omega_s': 2*np.pi*100, # Sampling frequency (rad/s)
    'Delta_max': 20.0,      # Uncertainty bound (N)
    'u_eq_max': 80.0,       # Peak equivalent control (N)
}

# Run all validation checks
results = validate_all_criteria(gains, validation_config)

print("\nValidation Results:")
print("=" * 50)
for criterion, passed in results.items():
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"{criterion:30s}: {status}")

if all(results.values()):
    print("\n✓ All validation criteria passed")
else:
    print("\n✗ Some validation criteria failed")