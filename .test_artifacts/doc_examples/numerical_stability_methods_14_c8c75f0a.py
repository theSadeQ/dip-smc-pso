# Example from: docs\theory\numerical_stability_methods.md
# Index: 14
# Runnable: True
# Hash: c8c75f0a

from src.optimization.validation.pso_bounds_validator import PSOBoundsValidator
validator = PSOBoundsValidator(config)
result = validator.validate_bounds('classical_smc', bounds_min, bounds_max)
if not result.is_valid:
    print("Warnings:", result.warnings)
    print("Recommended bounds:", result.adjusted_bounds)