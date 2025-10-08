# Example from: docs\reference\utils\reproducibility___init__.md
# Index: 3
# Runnable: True
# Hash: c303be88

from src.utils.reproducibility import set_seed
from src.optimizer import PSOTuner

def reproducible_pso_tuning(seed: int):
    # Set seed before PSO initialization
    set_seed(seed)

    # Create PSO tuner
    tuner = PSOTuner(
        n_particles=30,
        iters=100,
        bounds=[(0.1, 50.0)] * 6
    )

    # Optimize (deterministic with fixed seed)
    best_gains, best_fitness = tuner.optimize(fitness_function)

    return best_gains

# Verify PSO reproducibility
gains_run1 = reproducible_pso_tuning(seed=123)
gains_run2 = reproducible_pso_tuning(seed=123)

assert np.allclose(gains_run1, gains_run2)
print("✓ PSO optimization is reproducible")