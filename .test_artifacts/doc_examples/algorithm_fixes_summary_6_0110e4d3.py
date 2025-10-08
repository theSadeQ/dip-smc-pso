# Example from: docs\mathematical_foundations\algorithm_fixes_summary.md
# Index: 6
# Runnable: True
# Hash: 0110e4d3

def get_effective_controllability_threshold(self) -> float:
       """Auto-compute threshold based on system parameters."""
       if self.controllability_threshold is not None:
           return self.controllability_threshold

       # Scale with surface gains for adaptive behavior
       base_threshold = 0.05 * (self.k1 + self.k2)

       # Bound within reasonable limits
       return np.clip(base_threshold, 0.01, 1.0)