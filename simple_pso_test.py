#==========================================================================================\\\
#================================ simple_pso_test.py =================================\\\
#==========================================================================================\\\

"""
Simple PSO test to validate Issue #2 optimization.
"""

import numpy as np
from src.config import load_config
from src.controllers.factory import create_controller
from src.optimizer.pso_optimizer import PSOTuner

def test_pso_optimization():
    """Run a simple PSO optimization test."""
    print("Loading configuration...")
    config = load_config("config.yaml")

    # Create corrected bounds for Issue #2
    config.pso.bounds.min = [1.0, 1.0, 5.0, 3.0, 0.5, 0.5]  # lambda bounds corrected
    config.pso.bounds.max = [20.0, 15.0, 20.0, 15.0, 2.0, 2.0]  # lambda bounds corrected
    config.pso.n_particles = 15
    config.pso.iters = 50

    print("Creating controller factory...")

    def controller_factory(gains):
        """Create STA-SMC controller with given gains."""
        controller = create_controller("sta_smc", config, gains=gains)
        return controller

    # Check n_gains
    test_controller = controller_factory([8.0, 5.0, 12.0, 6.0, 1.2, 0.8])
    print(f"Controller type: {type(test_controller)}")
    print(f"Controller n_gains: {getattr(test_controller, 'n_gains', 'Not found')}")

    # Add n_gains to factory function if missing
    if not hasattr(controller_factory, 'n_gains'):
        controller_factory.n_gains = 6

    print("Initializing PSO tuner...")
    tuner = PSOTuner(
        controller_factory=controller_factory,
        config=config,
        seed=42
    )

    print("Running PSO optimization...")
    result = tuner.optimise()

    print(f"Optimization complete!")
    print(f"Best cost: {result['best_cost']:.6f}")
    print(f"Best gains: {result['best_pos']}")

    # Compare with original problematic gains
    original_gains = [15.0, 8.0, 12.0, 6.0, 20.0, 4.0]
    optimized_gains = result['best_pos']

    print(f"\nComparison:")
    print(f"Original lambda1: {original_gains[4]:.3f} -> Optimized: {optimized_gains[4]:.3f}")
    print(f"Original lambda2: {original_gains[5]:.3f} -> Optimized: {optimized_gains[5]:.3f}")

    return result

if __name__ == "__main__":
    result = test_pso_optimization()