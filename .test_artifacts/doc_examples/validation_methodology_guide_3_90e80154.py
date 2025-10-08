# Example from: docs\testing\validation_methodology_guide.md
# Index: 3
# Runnable: False
# Hash: 90e80154

# example-metadata:
# runnable: false

class TestSlidingSurfaceGainSensitivity:
    """Validate gain sensitivity of sliding surfaces."""

    def test_proportional_gain_scaling(self):
        """Test that doubling gains doubles sliding variable."""
        gains1 = [5.0, 3.0, 4.0, 2.0]
        gains2 = [10.0, 6.0, 8.0, 4.0]  # Doubled gains

        surface1 = LinearSlidingSurface(gains1)
        surface2 = LinearSlidingSurface(gains2)

        state = np.array([0.1, 0.1, 0.1, 0.05, 0.05, 0.05])

        s1 = surface1.compute(state)
        s2 = surface2.compute(state)

        # Surface value should double with doubled gains
        assert abs(s2 - 2 * s1) < 1e-10, (
            f"Gain sensitivity violated: s(2k) = {s2}, but 2·s(k) = {2*s1}"
        )

    def test_zero_gains_zero_surface(self):
        """Test that zero gains produce zero sliding variable."""
        gains = [0.0, 0.0, 0.0, 0.0]
        surface = LinearSlidingSurface(gains)

        state = np.random.uniform(-1, 1, size=6)
        s = surface.compute(state)

        assert abs(s) < 1e-15, f"Zero gains should produce zero surface, got {s}"