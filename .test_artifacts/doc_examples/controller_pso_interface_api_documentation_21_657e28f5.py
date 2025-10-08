# Example from: docs\controller_pso_interface_api_documentation.md
# Index: 21
# Runnable: False
# Hash: 657e28f5

#!/usr/bin/env python3
"""Example: PSO optimization for Classical SMC."""

import numpy as np
from src.controllers.factory import ControllerFactory
from src.optimization.algorithms.pso_optimizer import PSOTuner
from src.config import load_config

def main():
    """Run PSO optimization example."""

    # Load configuration
    config = load_config('config.yaml')

    # Define controller factory
    def create_classical_smc(gains: np.ndarray):
        return ControllerFactory.create_controller('classical_smc', gains)

    # Initialize PSO tuner
    pso_tuner = PSOTuner(
        controller_factory=create_classical_smc,
        config=config,
        seed=42
    )

    # Set optimization bounds
    lower_bounds = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
    upper_bounds = np.array([20.0, 20.0, 20.0, 20.0, 100.0, 10.0])

    # Run optimization
    print("Starting PSO optimization...")
    results = pso_tuner.optimize(
        bounds=(lower_bounds, upper_bounds),
        n_particles=50,
        n_iterations=100,
        verbose=True
    )

    # Display results
    if results['success']:
        print(f"Optimization successful!")
        print(f"Best gains: {results['best_gains']}")
        print(f"Best cost: {results['best_cost']:.6f}")

        # Test optimized controller
        controller = create_classical_smc(results['best_gains'])
        test_state = np.array([0.1, 0.05, 0.0, 0.0, 0.0, 0.0])
        control = controller.compute_control(test_state)
        print(f"Test control output: {control:.3f} N")
    else:
        print(f"Optimization failed: {results.get('message', 'Unknown error')}")

if __name__ == "__main__":
    main()