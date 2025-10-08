# Example from: docs\factory_integration_troubleshooting_guide.md
# Index: 11
# Runnable: True
# Hash: c6d2acb7

from src.controllers.factory import validate_smc_gains, get_gain_bounds_for_pso, SMCType
import numpy as np

def debug_gain_validation(smc_type, gains):
    """Debug gain validation step by step."""

    print(f"Validating gains for {smc_type.value}: {gains}")

    # Step 1: Check gain count
    from src.controllers.factory import get_expected_gain_count
    expected_count = get_expected_gain_count(smc_type)
    actual_count = len(gains)

    print(f"Gain count: expected {expected_count}, got {actual_count}")
    if actual_count != expected_count:
        print(f"❌ Wrong gain count")
        return False

    # Step 2: Check gain types
    for i, gain in enumerate(gains):
        if not isinstance(gain, (int, float)):
            print(f"❌ Gain {i} has wrong type: {type(gain)}")
            return False

        if not np.isfinite(gain):
            print(f"❌ Gain {i} is not finite: {gain}")
            return False

        if gain <= 0:
            print(f"❌ Gain {i} is not positive: {gain}")
            return False

    print("✅ All validation checks passed")

    # Step 3: Check against bounds
    lower_bounds, upper_bounds = get_gain_bounds_for_pso(smc_type)
    for i, (gain, lower, upper) in enumerate(zip(gains, lower_bounds, upper_bounds)):
        if not (lower <= gain <= upper):
            print(f"⚠️  Gain {i} outside recommended bounds: {gain} not in [{lower}, {upper}]")

    return True

# Test validation
test_gains = [20.0, 15.0, 12.0, 8.0, 35.0, 5.0]
debug_gain_validation(SMCType.CLASSICAL, test_gains)