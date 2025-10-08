# Example from: docs\pso_factory_integration_patterns.md
# Index: 18
# Runnable: True
# Hash: ada2d98d

#!/usr/bin/env python3
"""Basic PSO optimization example."""

from src.controllers.factory import create_pso_controller_factory, SMCType, get_gain_bounds_for_pso
from src.optimization.algorithms.pso_optimizer import PSOTuner
from src.config import load_config

def basic_pso_example():
    """Basic PSO optimization example."""

    # Load configuration
    config = load_config("config.yaml")

    # Create controller factory
    factory = create_pso_controller_factory(
        SMCType.CLASSICAL,
        plant_config=config.physics
    )

    # Define fitness function
    def fitness_function(gains):
        controller = factory(gains)
        metrics = evaluate_controller_performance(controller)
        return metrics['total_cost']

    # Get optimization bounds
    bounds = get_gain_bounds_for_pso(SMCType.CLASSICAL)

    # Run PSO optimization
    tuner = PSOTuner(
        controller_factory=fitness_function,
        config=config
    )

    best_gains, best_fitness = tuner.optimize()

    print(f"Optimization complete!")
    print(f"Best gains: {best_gains}")
    print(f"Best fitness: {best_fitness}")

    return best_gains, best_fitness

if __name__ == "__main__":
    basic_pso_example()