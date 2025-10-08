# Example from: docs\implementation\legacy_code_documentation_index.md
# Index: 5
# Runnable: True
# Hash: bbbe3aa6

from src.optimizer.pso_optimizer import PSOOptimizer
from src.core.simulation_context import SimulationContext

# Set up optimization problem from theory
optimizer = PSOOptimizer(
    n_particles=30,        # From {eq}`swarm_size_rule`
    bounds=[[0.1, 20]] * 3 + [[0.1, 10], [0.001, 0.5]],  # Physical constraints
    objectives=['tracking', 'control_effort', 'smoothness']  # {eq}`multiobjective_problem`
)

# Run optimization with theoretical convergence monitoring
context = SimulationContext('classical_smc')
best_params = optimizer.optimize(context, max_generations=50)