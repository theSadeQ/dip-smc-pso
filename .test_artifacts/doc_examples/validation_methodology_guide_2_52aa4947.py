# Example from: docs\testing\validation_methodology_guide.md
# Index: 2
# Runnable: False
# Hash: 52aa4947

class TestSlidingSurfaceHomogeneity:
    """Validate homogeneity property of sliding surfaces."""

    def test_homogeneity_property(self):
        """Test σ(α·x) = α·σ(x) for linear surfaces."""
        gains = [5.0, 3.0, 4.0, 2.0]
        surface = LinearSlidingSurface(gains)

        x = np.array([0.1, 0.1, 0.1, 0.05, 0.05, 0.05])
        alpha = 2.5

        s_original = surface.compute(x)
        s_scaled = surface.compute(alpha * x)

        # Verify homogeneity: s(α·x) = α·s(x)
        expected = alpha * s_original
        assert abs(s_scaled - expected) < 1e-10, (
            f"Homogeneity violated: s({alpha}·x) = {s_scaled}, "
            f"but {alpha}·s(x) = {expected}"
        )

    def test_homogeneity_negative_scaling(self):
        """Test homogeneity with negative scalar."""
        gains = [5.0, 3.0, 4.0, 2.0]
        surface = LinearSlidingSurface(gains)

        x = np.array([0.1, 0.1, 0.1, 0.05, 0.05, 0.05])
        alpha = -1.5

        s_original = surface.compute(x)
        s_scaled = surface.compute(alpha * x)

        assert abs(s_scaled - alpha * s_original) < 1e-10