# Example from: docs\mathematical_foundations\pso_algorithm_theory.md
# Index: 7
# Runnable: False
# Hash: eec52556

max_iter = 200
stagnation_limit = 20

for iter in range(max_iter):
    # ... PSO iteration ...

    if no_improvement_count >= stagnation_limit:
        print(f"Converged at iteration {iter}")
        break