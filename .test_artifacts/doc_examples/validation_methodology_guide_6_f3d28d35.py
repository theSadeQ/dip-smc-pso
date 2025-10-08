# Example from: docs\testing\validation_methodology_guide.md
# Index: 6
# Runnable: False
# Hash: f3d28d35

# example-metadata:
# runnable: false

class TestBoundaryLayerAsymptoticBehavior:
    """Validate asymptotic limits of switching functions."""

    def test_tanh_asymptotic_limits(self):
        """Test tanh approaches ±1 for large |σ|."""
        boundary_layer = BoundaryLayer(thickness=0.1, method="tanh")

        # Large positive σ
        switch_pos = boundary_layer.compute(10.0)
        assert abs(switch_pos - 1.0) < 1e-3, (
            f"tanh should approach +1 for large positive σ, got {switch_pos}"
        )

        # Large negative σ
        switch_neg = boundary_layer.compute(-10.0)
        assert abs(switch_neg - (-1.0)) < 1e-3, (
            f"tanh should approach -1 for large negative σ, got {switch_neg}"
        )

    def test_saturation_bounds(self):
        """Test saturation function is bounded by ±1."""
        boundary_layer = BoundaryLayer(thickness=0.1, method="linear")

        # Test many values
        s_values = np.random.uniform(-100, 100, size=1000)
        for s in s_values:
            switch = boundary_layer.compute(s)
            assert -1.0 <= switch <= 1.0, (
                f"Saturation violated: switch({s}) = {switch} not in [-1, 1]"
            )