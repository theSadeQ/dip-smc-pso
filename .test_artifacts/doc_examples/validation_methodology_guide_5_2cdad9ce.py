# Example from: docs\testing\validation_methodology_guide.md
# Index: 5
# Runnable: False
# Hash: 2cdad9ce

# example-metadata:
# runnable: false

class TestBoundaryLayerMonotonicity:
    """Validate monotonicity of switching functions."""

    def test_tanh_monotonicity(self):
        """Test tanh switching function is strictly increasing."""
        boundary_layer = BoundaryLayer(thickness=0.1, method="tanh")

        s_values = np.linspace(-1, 1, 100)
        switch_values = [boundary_layer.compute(s) for s in s_values]

        # Verify strict monotonicity
        for i in range(len(switch_values) - 1):
            assert switch_values[i+1] >= switch_values[i], (
                f"Monotonicity violated at index {i}: "
                f"switch({s_values[i+1]}) = {switch_values[i+1]} < "
                f"switch({s_values[i]}) = {switch_values[i]}"
            )

    def test_saturation_monotonicity(self):
        """Test saturation function is monotonic."""
        boundary_layer = BoundaryLayer(thickness=0.1, method="linear")

        s_values = np.linspace(-2, 2, 200)
        switch_values = [boundary_layer.compute(s) for s in s_values]

        for i in range(len(switch_values) - 1):
            assert switch_values[i+1] >= switch_values[i]