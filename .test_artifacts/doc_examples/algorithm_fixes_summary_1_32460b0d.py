# Example from: docs\mathematical_foundations\algorithm_fixes_summary.md
# Index: 1
# Runnable: False
# Hash: 32460b0d

def compute_switching_function(self, surface_value: float) -> float:
       """Compute continuous switching function with adaptive boundary layer."""

       # Adaptive boundary layer thickness
       surface_derivative = self._get_surface_derivative()
       effective_thickness = self.base_thickness + self.slope * abs(surface_derivative)

       # Continuous switching approximation
       if self.switch_method == "tanh":
           return np.tanh(surface_value / effective_thickness)
       elif self.switch_method == "linear":
           return np.clip(surface_value / effective_thickness, -1.0, 1.0)
       else:  # "sign"
           return np.sign(surface_value)