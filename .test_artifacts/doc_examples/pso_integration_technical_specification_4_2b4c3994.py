# Example from: docs\pso_integration_technical_specification.md
# Index: 4
# Runnable: False
# Hash: 2b4c3994

# example-metadata:
# runnable: false

def validate_gain_bounds(controller_type: str, gains: np.ndarray) -> tuple[bool, str]:
    """
    Comprehensive gain bounds validation with mathematical reasoning.

    Implements controller-specific stability and performance constraints
    derived from Lyapunov stability theory and sliding mode control theory.

    Returns
    -------
    tuple[bool, str]
        (is_valid, error_message) with detailed mathematical justification
    """
    bounds_spec = CONTROLLER_REGISTRY[controller_type]['gain_bounds']
    stability_req = CONTROLLER_REGISTRY[controller_type]['stability_requirements']

    # Basic bounds validation
    for i, (gain, (min_val, max_val)) in enumerate(zip(gains, bounds_spec)):
        if not (min_val <= gain <= max_val):
            return False, f"Gain {i} = {gain:.3f} outside bounds [{min_val}, {max_val}]"

    # Controller-specific mathematical constraints
    if controller_type == 'sta_smc':
        K1, K2 = gains[0], gains[1]
        if K1 <= K2:
            return False, f"STA stability requires K₁ > K₂, got K₁={K1:.3f}, K₂={K2:.3f}"

        lambda1, lambda2 = gains[4], gains[5]
        damping = lambda2 / (2 * np.sqrt(lambda1))
        if not (0.6 <= damping <= 0.8):
            return False, f"Damping ratio ζ={damping:.3f} outside optimal range [0.6, 0.8]"

    return True, "All constraints satisfied"