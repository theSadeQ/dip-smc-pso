# Example from: docs\testing\validation_methodology_guide.md
# Index: 4
# Runnable: True
# Hash: a3140306

# tests/validation/test_boundary_layer_properties.py

class TestBoundaryLayerContinuity:
    """Validate continuity of boundary layer switching functions."""

    def test_tanh_continuity_at_surface(self):
        """Test tanh switching function is continuous at σ = 0."""
        from src.controllers.smc.algorithms.classical.boundary_layer import BoundaryLayer

        boundary_layer = BoundaryLayer(thickness=0.1, method="tanh")

        epsilon = 1e-8
        switch_left = boundary_layer.compute(-epsilon)
        switch_center = boundary_layer.compute(0.0)
        switch_right = boundary_layer.compute(epsilon)

        # Values should be very close at the boundary
        assert abs(switch_left - switch_center) < 1e-6
        assert abs(switch_right - switch_center) < 1e-6
        assert abs(switch_center) < 1e-6  # tanh(0) = 0

    def test_linear_continuity_at_surface(self):
        """Test linear (saturation) switching function continuity."""
        boundary_layer = BoundaryLayer(thickness=0.1, method="linear")

        epsilon = 1e-8
        switch_left = boundary_layer.compute(-epsilon)
        switch_center = boundary_layer.compute(0.0)
        switch_right = boundary_layer.compute(epsilon)

        # Linear function is continuous
        assert abs(switch_left - switch_center) < 1e-10
        assert abs(switch_right - switch_center) < 1e-10