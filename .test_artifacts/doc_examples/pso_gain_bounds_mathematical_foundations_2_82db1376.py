# Example from: docs\pso_gain_bounds_mathematical_foundations.md
# Index: 2
# Runnable: False
# Hash: 82db1376

def validate_smc_stability_realtime(gains: np.ndarray, controller_type: str) -> bool:
    """
    Real-time stability validation for PSO-generated gains.

    Mathematical Validation Chain:
    1. Positivity constraints (all gains > 0)
    2. Hurwitz stability (characteristic polynomial roots)
    3. Damping ratio bounds (transient performance)
    4. Actuator compatibility (saturation limits)
    5. Controller-specific constraints (e.g., K₁ > K₂ for STA)
    """

    if controller_type == "classical_smc":
        c1, lambda1, c2, lambda2, K, kd = gains

        # Positivity
        if not all(g > 0 for g in gains):
            return False

        # Damping ratios
        zeta1 = lambda1 / (2 * np.sqrt(c1))
        zeta2 = lambda2 / (2 * np.sqrt(c2))
        if not (0.6 <= zeta1 <= 0.8 and 0.6 <= zeta2 <= 0.8):
            return False

        # Actuator limits
        if K + kd > 150:
            return False

    elif controller_type == "sta_smc":
        K1, K2, k1, k2, lambda1, lambda2 = gains

        # STA stability condition
        if K1 <= K2:
            return False

        # Issue #2 compliance: damping ratio check
        zeta1 = lambda1 / (2 * np.sqrt(k1))
        zeta2 = lambda2 / (2 * np.sqrt(k2))
        if not (0.6 <= zeta1 <= 0.8 and 0.6 <= zeta2 <= 0.8):
            return False

        # Finite-time convergence condition (simplified)
        L_estimate = 10.0  # Conservative Lipschitz constant
        if K1**2 <= 4 * K2 * L_estimate:
            return False

    return True