# Example from: docs\mathematical_foundations\test_validation_methodology.md
# Index: 8
# Runnable: False
# Hash: 353f3bfd

# example-metadata:
# runnable: false

def test_hurwitz_stability_check():
    """Test that gain combinations satisfy Hurwitz stability."""

    def check_stability(k1, k2, lam1, lam2):
        """Check if gains produce stable sliding dynamics."""
        # For each 2x2 subsystem: s² + λᵢs + cᵢ = 0
        # Stability requires λᵢ > 0 and cᵢ > 0
        return k1 > 0 and k2 > 0 and lam1 > 0 and lam2 > 0

    # Stable configuration
    stable_gains = [5.0, 3.0, 4.0, 2.0, 10.0, 1.0]
    config = ClassicalSMCConfig(gains=stable_gains, max_force=100, dt=0.01, boundary_layer=0.01)

    assert check_stability(config.k1, config.k2, config.lam1, config.lam2)

    # Check damping ratios
    zeta1 = config.lam1 / (2 * np.sqrt(config.k1))
    zeta2 = config.lam2 / (2 * np.sqrt(config.k2))

    # Both subsystems should have positive damping
    assert zeta1 > 0
    assert zeta2 > 0