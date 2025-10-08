# Example from: docs\api\factory_system_api_reference.md
# Index: 66
# Runnable: False
# Hash: 5d318ea8

# example-metadata:
# runnable: false

"""
Example 2: PSO-Optimized Controller Creation
Demonstrates complete PSO workflow for gain optimization.
"""

from src.controllers.factory import SMCType, create_pso_controller_factory, create_controller
from src.optimization.algorithms.pso_optimizer import PSOTuner
from src.config import load_config
import numpy as np

def evaluate_controller(controller, test_states):
    """Evaluate controller performance on test trajectories."""
    total_cost = 0.0
    for state in test_states:
        result = controller.compute_control(state, 0.0, {})
        if hasattr(result, 'u'):
            u = result.u
        else:
            u = result['u'] if isinstance(result, dict) else result

        # Compute cost: state regulation + control effort
        cost = np.sum(state[:3]**2) + 0.1 * u**2
        total_cost += cost

    return total_cost / len(test_states)

def main():
    # Load configuration
    config = load_config("config.yaml")

    # Step 1: Create PSO-compatible controller factory
    print("Creating PSO controller factory...")
    controller_factory = create_pso_controller_factory(
        smc_type=SMCType.CLASSICAL,
        max_force=150.0,
        dt=0.001
    )
    print(f"Factory configured for {controller_factory.n_gains} gains")

    # Step 2: Initialize PSO tuner
    print("\nInitializing PSO tuner...")
    tuner = PSOTuner(
        controller_factory=controller_factory,
        config=config,
        seed=42
    )

    # Step 3: Run PSO optimization
    print("Running PSO optimization (30 particles, 100 iterations)...")
    result = tuner.optimise(
        n_particles_override=30,
        iters_override=100
    )

    # Step 4: Extract results
    optimized_gains = result['best_pos']
    best_cost = result['best_cost']
    print(f"\nOptimization complete!")
    print(f"  Best cost: {best_cost:.6f}")
    print(f"  Optimized gains: {[f'{g:.2f}' for g in optimized_gains]}")

    # Step 5: Create final controller
    print("\nCreating optimized controller...")
    optimized_controller = create_controller('classical_smc', config, gains=optimized_gains)

    # Step 6: Compare with baseline
    print("\nComparing with baseline...")
    baseline_controller = create_controller('classical_smc', config)

    # Generate test states
    np.random.seed(42)
    test_states = [
        np.array([0.0, 0.1, 0.05, 0.0, 0.0, 0.0]),
        np.array([0.0, 0.2, 0.1, 0.0, 0.5, 0.3]),
        np.array([0.0, -0.1, -0.05, 0.0, -0.3, -0.2])
    ]

    baseline_cost = evaluate_controller(baseline_controller, test_states)
    optimized_cost = evaluate_controller(optimized_controller, test_states)

    improvement = (baseline_cost - optimized_cost) / baseline_cost * 100
    print(f"  Baseline cost: {baseline_cost:.3f}")
    print(f"  Optimized cost: {optimized_cost:.3f}")
    print(f"  Improvement: {improvement:.1f}%")

if __name__ == '__main__':
    main()