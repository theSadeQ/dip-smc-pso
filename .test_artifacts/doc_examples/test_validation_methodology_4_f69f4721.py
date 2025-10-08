# Example from: docs\mathematical_foundations\test_validation_methodology.md
# Index: 4
# Runnable: False
# Hash: f69f4721

# example-metadata:
# runnable: false

   def test_boundary_layer_continuity():
       """Test that boundary layer provides continuous switching."""
       boundary_layer = BoundaryLayer(thickness=0.1, switch_method="tanh")

       # Test continuity at surface (s=0)
       epsilon = 1e-8
       switch_left = boundary_layer.compute_switching_function(-epsilon)
       switch_right = boundary_layer.compute_switching_function(epsilon)
       switch_center = boundary_layer.compute_switching_function(0.0)

       # Values should be very close at the boundary
       assert abs(switch_left - switch_center) < 1e-6
       assert abs(switch_right - switch_center) < 1e-6