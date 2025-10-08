# Example from: docs\pso_gain_bounds_mathematical_foundations.md
# Index: 7
# Runnable: False
# Hash: 371f4358

def issue2_compliant_constraints(gains: np.ndarray) -> bool:
    """
    Issue #2 specific constraints for STA-SMC optimization.
    """
    K1, K2, k1, k2, lambda1, lambda2 = gains

    # Original STA constraints
    if K1 <= K2:
        return False

    # Issue #2 specific: damping ratio constraint
    zeta1 = lambda1 / (2 * np.sqrt(k1))
    zeta2 = lambda2 / (2 * np.sqrt(k2))

    # Target damping for <5% overshoot
    if not (0.69 <= zeta1 <= 0.8 and 0.69 <= zeta2 <= 0.8):
        return False

    return True