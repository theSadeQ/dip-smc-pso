# Example from: docs\testing\guides\coverage_quality_gates_troubleshooting.md
# Index: 10
# Runnable: True
# Hash: b28fb892

def test_pso_convergence_failure():
       # Force non-convergence with difficult fitness landscape
       pso = PSOTuner(max_iterations=5, convergence_threshold=1e-10)
       result, converged = pso.optimize(difficult_fitness_function)
       assert not converged