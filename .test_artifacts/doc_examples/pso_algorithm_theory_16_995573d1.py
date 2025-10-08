# Example from: docs\mathematical_foundations\pso_algorithm_theory.md
# Index: 16
# Runnable: False
# Hash: 995573d1

# example-metadata:
# runnable: false

best_fitness_history = []
no_improvement_count = 0
tolerance = 1e-6

for iter in range(max_iter):
    # ... PSO iteration ...

    if len(best_fitness_history) > 0:
        improvement = abs(current_best - best_fitness_history[-1])
        if improvement < tolerance:
            no_improvement_count += 1
        else:
            no_improvement_count = 0

    if no_improvement_count >= 20:
        print(f"Stagnation detected at iteration {iter}")
        # Restart or perturb swarm
        break