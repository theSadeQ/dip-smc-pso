# Example from: docs\factory_integration_troubleshooting_guide.md
# Index: 12
# Runnable: True
# Hash: 4d66136d

def fix_common_gain_issues(gains, smc_type):
    """Fix common gain validation issues."""

    import numpy as np

    # Convert to list if numpy array
    if isinstance(gains, np.ndarray):
        gains = gains.tolist()

    # Ensure all gains are float
    gains = [float(g) for g in gains]

    # Clamp to valid range
    for i, gain in enumerate(gains):
        if not np.isfinite(gain):
            gains[i] = 1.0  # Default for invalid values
        elif gain <= 0:
            gains[i] = 0.1  # Minimum positive value
        elif gain > 1000:
            gains[i] = 100.0  # Maximum reasonable value

    # Ensure correct count
    expected_count = get_expected_gain_count(smc_type)
    if len(gains) < expected_count:
        # Pad with defaults
        default_gains = get_default_gains(smc_type.value)
        gains.extend(default_gains[len(gains):])
    elif len(gains) > expected_count:
        # Truncate
        gains = gains[:expected_count]

    return gains

# Usage in PSO fitness function
def robust_fitness_function(gains):
    """PSO fitness function with gain fixing."""

    # Fix common issues
    fixed_gains = fix_common_gain_issues(gains, SMCType.CLASSICAL)

    # Validate
    if not validate_smc_gains(SMCType.CLASSICAL, fixed_gains):
        return float('inf')

    # Create controller
    factory = create_pso_controller_factory(SMCType.CLASSICAL)
    controller = factory(fixed_gains)

    # Evaluate performance
    return evaluate_controller_performance(controller)