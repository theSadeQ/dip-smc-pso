# Example from: docs\testing\guides\coverage_quality_gates_troubleshooting.md
# Index: 9
# Runnable: True
# Hash: c7af2424

# Uncovered: Convergence failure scenarios
   if iteration > max_iterations:  # ← Max iteration limit not tested
       logger.warning("PSO failed to converge")
       return best_solution, False