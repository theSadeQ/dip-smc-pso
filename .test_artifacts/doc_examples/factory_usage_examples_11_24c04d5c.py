# Example from: docs\technical\factory_usage_examples.md
# Index: 11
# Runnable: True
# Hash: 24c04d5c

from src.controllers.factory import get_gain_bounds_for_pso, SMCType, validate_smc_gains

# Get controller-specific bounds
bounds = get_gain_bounds_for_pso(SMCType.CLASSICAL)
lower_bounds, upper_bounds = bounds

print(f"Classical SMC bounds:")
print(f"  Lower: {lower_bounds}")
print(f"  Upper: {upper_bounds}")

# Validate gains before optimization
test_gains = [15.0, 12.0, 8.0, 6.0, 25.0, 4.0]
is_valid = validate_smc_gains(SMCType.CLASSICAL, test_gains)

if is_valid:
    print("Gains are valid for Classical SMC")
    # Use gains in optimization or controller creation
else:
    print("Invalid gains - adjustment needed")