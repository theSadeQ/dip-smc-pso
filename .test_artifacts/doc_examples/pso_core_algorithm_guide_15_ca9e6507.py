# Example from: docs\optimization\pso_core_algorithm_guide.md
# Index: 15
# Runnable: True
# Hash: ca9e6507

from src.optimization.algorithms.swarm import ParticleSwarmOptimizer
from src.optimization.core.interfaces import ParameterSpace

# Define parameter space
param_space = ParameterSpace(
    bounds=[
        (0.1, 50.0),  # k1
        (0.1, 50.0),  # k2
        (0.1, 50.0),  # λ1
        (0.1, 50.0),  # λ2
        (1.0, 200.0), # K
        (0.0, 50.0),  # kd
    ],
    names=['k1', 'k2', 'lambda1', 'lambda2', 'K', 'kd']
)

# Create optimizer
pso = ParticleSwarmOptimizer(
    parameter_space=param_space,
    population_size=30,
    max_iterations=100,
    adaptive_weights=True,
    velocity_clamping=True
)

# Define objective function
def fitness_function(gains):
    controller = create_controller('classical_smc', gains=gains)
    result = simulate(controller, duration=5.0)
    return result.ise + 0.3 * result.chattering

# Run optimization
result = pso.optimize(objective_function)

# Results
print(f"Best gains: {result.best_position}")
print(f"Best fitness: {result.best_fitness}")
print(f"Iterations: {result.iterations}")
print(f"Convergence reason: {result.convergence_status}")