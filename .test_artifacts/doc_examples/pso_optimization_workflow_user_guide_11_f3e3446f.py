# Example from: docs\pso_optimization_workflow_user_guide.md
# Index: 11
# Runnable: True
# Hash: f3e3446f

from src.optimization.multi_objective import ParetoFrontPSO

# Define multiple objectives
objectives = {
    'performance': {'weight': 1.0, 'minimize': True},
    'energy': {'weight': 0.01, 'minimize': True},
    'robustness': {'weight': 10.0, 'minimize': True}
}

# Multi-objective PSO
mo_pso = ParetoFrontPSO(
    controller_factory=create_controller,
    objectives=objectives,
    config=config
)

# Get Pareto front
pareto_solutions = mo_pso.optimize(
    bounds=bounds,
    n_particles=100,
    n_iterations=200
)

# Select solution based on preferences
selected_solution = mo_pso.select_solution(
    pareto_solutions,
    preferences={'performance': 0.6, 'energy': 0.2, 'robustness': 0.2}
)