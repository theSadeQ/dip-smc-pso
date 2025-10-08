# Example from: docs\reports\pso_code_quality_optimization_report.md
# Index: 8
# Runnable: True
# Hash: 0a67d3e6

# Cache expensive computations
   @lru_cache(maxsize=128)
   def _compute_normalization_constants(self, baseline_gains):
       # Expensive baseline computation