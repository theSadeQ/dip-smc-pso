# Example from: docs\pso_optimization_workflow_user_guide.md
# Index: 17
# Runnable: False
# Hash: 295cba06

# example-metadata:
# runnable: false

# Systematic bounds exploration
bounds_sets = [
    ([0.1, 0.1, 0.1, 0.1, 0.1, 0.1], [10, 10, 10, 10, 50, 5]),    # Conservative
    ([0.5, 0.5, 0.5, 0.5, 1.0, 0.5], [20, 20, 20, 20, 100, 10]),  # Standard
    ([1.0, 1.0, 1.0, 1.0, 5.0, 1.0], [30, 30, 30, 30, 150, 15])   # Aggressive
]

best_overall = None
best_cost = float('inf')

for i, (lower, upper) in enumerate(bounds_sets):
    print(f"Testing bounds set {i+1}/3...")

    results = pso_tuner.optimize(
        bounds=(np.array(lower), np.array(upper)),
        n_particles=50,
        n_iterations=100
    )

    if results['best_cost'] < best_cost:
        best_cost = results['best_cost']
        best_overall = results

    print(f"Bounds set {i+1}: Best cost = {results['best_cost']:.3f}")

print(f"Overall best cost: {best_cost:.3f}")