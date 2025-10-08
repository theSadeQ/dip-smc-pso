# Example from: docs\factory\troubleshooting_guide.md
# Index: 8
# Runnable: True
# Hash: 598b0370

from src.controllers.factory import get_gain_bounds_for_pso, validate_smc_gains

def diagnose_pso_bounds_error(smc_type, particle_gains):
    print(f"Diagnosing PSO bounds for {smc_type}")

    # Get expected bounds
    lower_bounds, upper_bounds = get_gain_bounds_for_pso(smc_type)
    print(f"Expected bounds:")
    print(f"  Lower: {lower_bounds}")
    print(f"  Upper: {upper_bounds}")

    print(f"Particle gains: {particle_gains}")

    # Check each gain
    for i, (gain, lower, upper) in enumerate(zip(particle_gains, lower_bounds, upper_bounds)):
        if gain < lower:
            print(f"✗ Gain {i}: {gain} < {lower} (too low)")
        elif gain > upper:
            print(f"✗ Gain {i}: {gain} > {upper} (too high)")
        else:
            print(f"✓ Gain {i}: {gain} within bounds [{lower}, {upper}]")

    # Overall validation
    is_valid = validate_smc_gains(smc_type, particle_gains)
    print(f"Overall validation: {'PASS' if is_valid else 'FAIL'}")

# Example usage
diagnose_pso_bounds_error(SMCType.CLASSICAL, [100, 50, 30, 25, 200, 15])  # Out of bounds