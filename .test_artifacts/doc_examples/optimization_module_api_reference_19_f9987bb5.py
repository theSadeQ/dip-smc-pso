# Example from: docs\api\optimization_module_api_reference.md
# Index: 19
# Runnable: True
# Hash: f9987bb5

from src.optimization.validation.pso_bounds_validator import PSOBoundsValidator
from src.config import load_config

config = load_config("config.yaml")
validator = PSOBoundsValidator(config)

# Validate bounds for Classical SMC
result = validator.validate_bounds(
    controller_type='classical_smc',
    lower_bounds=[1.0, 1.0, 0.5, 0.5, 1.0, 0.1],
    upper_bounds=[100.0, 100.0, 50.0, 50.0, 200.0, 20.0]
)

if result.is_valid:
    print("Bounds are valid!")
else:
    print("Validation warnings:")
    for warning in result.warnings:
        print(f"  - {warning}")

    print("\nRecommendations:")
    for rec in result.recommendations:
        print(f"  - {rec}")

    if result.adjusted_bounds:
        print("\nAdjusted bounds:")
        print(f"  Lower: {result.adjusted_bounds['lower']}")
        print(f"  Upper: {result.adjusted_bounds['upper']}")