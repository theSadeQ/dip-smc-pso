# Example from: docs\testing\reports\2025-09-30\pso_convergence_analysis.md
# Index: 3
# Runnable: True
# Hash: d8038c89

# Potential issue in cost function
   cost = performance_metric + 1e6 * constraint_violation
   # If constraint is always zero, cost = performance only
   # If performance is normalized poorly, could yield 0