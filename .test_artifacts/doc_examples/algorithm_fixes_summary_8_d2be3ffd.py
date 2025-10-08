# Example from: docs\mathematical_foundations\algorithm_fixes_summary.md
# Index: 8
# Runnable: False
# Hash: d2be3ffd

# example-metadata:
# runnable: false

   def test_boundary_layer_monotonicity_all_methods(self):
       """Test monotonicity for all switching methods."""
       methods = ["tanh", "linear", "sign"]

       for method in methods:
           boundary_layer = BoundaryLayer(thickness=0.1, switch_method=method)

           s_values = np.linspace(-2, 2, 1000)
           switch_values = [boundary_layer.compute_switching_function(s) for s in s_values]

           # Must be monotonically increasing
           for i in range(len(switch_values) - 1):
               assert switch_values[i+1] >= switch_values[i]