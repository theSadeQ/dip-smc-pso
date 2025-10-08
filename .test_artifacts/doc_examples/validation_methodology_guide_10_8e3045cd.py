# Example from: docs\testing\validation_methodology_guide.md
# Index: 10
# Runnable: True
# Hash: 8e3045cd

class TestStabilityRequirements:
    """Validate stability requirements for controller gains."""

    def test_hurwitz_stability_condition(self):
        """Test gains satisfy Hurwitz stability criteria."""
        from src.controllers.smc.classic_smc import ClassicalSMC

        # Stable configuration
        stable_gains = [5.0, 3.0, 4.0, 2.0, 10.0, 1.0]
        controller = ClassicalSMC(gains=stable_gains, max_force=100.0)

        # Check Hurwitz conditions
        k1, k2, lam1, lam2 = controller.k1, controller.k2, controller.lam1, controller.lam2

        # For stable sliding dynamics: λᵢ > 0 and cᵢ (gains) > 0
        assert k1 > 0 and k2 > 0, "Position gains must be positive for stability"
        assert lam1 > 0 and lam2 > 0, "Velocity gains must be positive for stability"

    def test_damping_ratio_validation(self):
        """Test that damping ratios are positive."""
        from src.controllers.smc.classic_smc import ClassicalSMC

        stable_gains = [5.0, 3.0, 4.0, 2.0, 10.0, 1.0]
        controller = ClassicalSMC(gains=stable_gains, max_force=100.0)

        # Compute damping ratios: ζᵢ = λᵢ / (2√kᵢ)
        zeta1 = controller.lam1 / (2 * np.sqrt(controller.k1))
        zeta2 = controller.lam2 / (2 * np.sqrt(controller.k2))

        assert zeta1 > 0, f"Damping ratio ζ₁ must be positive, got {zeta1}"
        assert zeta2 > 0, f"Damping ratio ζ₂ must be positive, got {zeta2}"

        # Recommended: underdamped to critically damped (0 < ζ ≤ 1)
        assert 0 < zeta1 <= 2.0, f"ζ₁ = {zeta1} outside recommended range (0, 2]"
        assert 0 < zeta2 <= 2.0, f"ζ₂ = {zeta2} outside recommended range (0, 2]"