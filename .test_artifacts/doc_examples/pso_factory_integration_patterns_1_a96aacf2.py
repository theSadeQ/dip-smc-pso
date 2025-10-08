# Example from: docs\pso_factory_integration_patterns.md
# Index: 1
# Runnable: True
# Hash: a96aacf2

from src.controllers.factory import create_smc_for_pso, SMCType
import numpy as np

def simple_fitness_function(gains_array: np.ndarray) -> float:
    """Simple PSO fitness evaluation using direct controller creation."""

    # Create controller directly from gains
    controller = create_smc_for_pso(
        SMCType.CLASSICAL,
        gains=gains_array,
        max_force=150.0,
        dt=0.001
    )

    # Evaluate controller performance
    performance_metrics = evaluate_controller_performance(controller)

    # Return fitness value (minimize)
    return performance_metrics['total_cost']

# PSO optimization setup
from src.optimization.algorithms.pso_optimizer import PSOTuner

bounds = get_gain_bounds_for_pso(SMCType.CLASSICAL)
tuner = PSOTuner(
    controller_factory=simple_fitness_function,
    config=config
)
best_gains, best_fitness = tuner.optimize()