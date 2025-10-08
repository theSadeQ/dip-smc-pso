# Example from: docs\mathematical_foundations\test_validation_methodology.md
# Index: 5
# Runnable: True
# Hash: 9634d87b

def test_boundary_layer_monotonicity():
       """Test that switching function is monotonic."""
       boundary_layer = BoundaryLayer(thickness=0.1, switch_method="tanh")

       s_values = np.linspace(-1, 1, 100)
       switch_values = [boundary_layer.compute_switching_function(s) for s in s_values]

       # Switching function should be strictly increasing
       for i in range(len(switch_values) - 1):
           assert switch_values[i+1] >= switch_values[i]