# Example from: docs\guides\api\optimization.md
# Index: 15
# Runnable: True
# Hash: acba2f81

from src.controllers import validate_smc_gains

# Check if gains are within valid range
candidate_gains = [10, 8, 15, 12, 50, 5]
is_valid = validate_smc_gains(SMCType.CLASSICAL, candidate_gains)

if not is_valid:
    print("Invalid gains detected!")

# Validate bounds themselves
def validate_bounds(bounds, controller_type):
    """Ensure bounds are physically meaningful."""
    n_expected = {
        SMCType.CLASSICAL: 6,
        SMCType.ADAPTIVE: 5,
        SMCType.SUPER_TWISTING: 6,
        SMCType.HYBRID: 4
    }

    if len(bounds) != n_expected[controller_type]:
        raise ValueError(f"Expected {n_expected[controller_type]} bounds")

    for i, (low, high) in enumerate(bounds):
        if low >= high:
            raise ValueError(f"Bound {i}: low ({low}) >= high ({high})")
        if low <= 0:
            raise ValueError(f"Bound {i}: non-positive lower bound")

    return True