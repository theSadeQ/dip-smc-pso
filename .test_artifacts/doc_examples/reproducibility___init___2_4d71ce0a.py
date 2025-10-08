# Example from: docs\reference\utils\reproducibility___init__.md
# Index: 2
# Runnable: True
# Hash: 4d71ce0a

from src.utils.reproducibility import set_seed
import numpy as np

def monte_carlo_simulation(n_trials: int, seed: int):
    # Set seed for reproducible Monte Carlo
    set_seed(seed)

    results = []
    for i in range(n_trials):
        # Simulate with random initial conditions
        x0 = np.random.randn(6) * 0.1
        result = run_simulation(x0)
        results.append(result)

    return np.mean(results), np.std(results)

# Run twice with same seed - get identical results
mean1, std1 = monte_carlo_simulation(1000, seed=42)
mean2, std2 = monte_carlo_simulation(1000, seed=42)

assert mean1 == mean2 and std1 == std2
print("✓ Monte Carlo reproducibility confirmed")