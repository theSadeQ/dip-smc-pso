# Example from: docs\mathematical_foundations\test_validation_methodology.md
# Index: 6
# Runnable: True
# Hash: ca1bf37c

def test_boundary_layer_asymptotic_behavior():
       """Test asymptotic limits of switching function."""
       boundary_layer = BoundaryLayer(thickness=0.1, switch_method="tanh")

       # Large positive surface value
       switch_pos = boundary_layer.compute_switching_function(10.0)
       assert abs(switch_pos - 1.0) < 1e-3

       # Large negative surface value
       switch_neg = boundary_layer.compute_switching_function(-10.0)
       assert abs(switch_neg - (-1.0)) < 1e-3