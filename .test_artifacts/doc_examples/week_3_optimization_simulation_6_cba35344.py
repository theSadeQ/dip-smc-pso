# Example from: docs\plans\documentation\week_3_optimization_simulation.md
# Index: 6
# Runnable: True
# Hash: cba35344

from src.optimization.algorithms.swarm import PSOCore
from src.controllers.factory import SMCFactory

# Define bounds
bounds = [
    (0.1, 50.0),  # k1
    (0.1, 50.0),  # k2
    (0.1, 50.0),  # λ1
    (0.1, 50.0),  # λ2
    (1.0, 200.0), # K
    (0.0, 50.0),  # kd
]

# Create optimizer
optimizer = PSOCore(
    factory=SMCFactory,
    bounds=bounds,
    n_particles=30,
    max_iters=100
)

# Run optimization
result = optimizer.optimize()

print(f"Best gains: {result.best_position}")
print(f"Best fitness: {result.best_fitness}")
print(f"Convergence iteration: {result.convergence_iter}")