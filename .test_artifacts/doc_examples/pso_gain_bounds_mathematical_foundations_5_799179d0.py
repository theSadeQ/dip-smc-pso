# Example from: docs\pso_gain_bounds_mathematical_foundations.md
# Index: 5
# Runnable: False
# Hash: 799179d0

# example-metadata:
# runnable: false

def compute_constraint_penalty(gains: np.ndarray, controller_type: str) -> float:
    """
    Compute penalty for constraint violations in PSO fitness function.

    Penalty Structure:
    P = w₁ × bounds_violation + w₂ × stability_violation + w₃ × safety_violation
    """
    penalty = 0.0

    # Bounds violation penalty
    bounds = get_controller_bounds(controller_type)
    for i, (gain, (min_val, max_val)) in enumerate(zip(gains, bounds)):
        if gain < min_val:
            penalty += 1000 * (min_val - gain)**2
        elif gain > max_val:
            penalty += 1000 * (gain - max_val)**2

    # Stability constraint penalties
    if controller_type == "sta_smc":
        K1, K2 = gains[0], gains[1]
        if K1 <= K2:
            penalty += 10000  # Large penalty for stability violation

        # Issue #2 damping penalty
        lambda1, lambda2 = gains[4], gains[5]
        damping = lambda2 / (2 * np.sqrt(lambda1))
        if damping < 0.6 or damping > 0.8:
            penalty += 5000 * abs(damping - 0.7)**2

    return penalty