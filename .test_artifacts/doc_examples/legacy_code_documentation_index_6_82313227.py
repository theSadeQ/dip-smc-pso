# Example from: docs\implementation\legacy_code_documentation_index.md
# Index: 6
# Runnable: True
# Hash: 82313227

"""
Complete DIP-SMC-PSO workflow demonstrating theory-implementation integration.
"""
import numpy as np
from src.config import load_config
from src.controllers.factory import create_controller
from src.core.dynamics_full import DoublePendulumFull
from src.optimizer.pso_optimizer import PSOOptimizer
from src.utils.visualization import plot_results

def main():
    # Load validated configuration
    config = load_config('config.yaml')

    # Create system using complete dynamics {eq}`mass_matrix_form`
    system = DoublePendulumFull(
        m0=config.physics.m0, m1=config.physics.m1, m2=config.physics.m2,
        l1=config.physics.l1, l2=config.physics.l2, g=config.physics.g
    )

    # Optimize controller parameters using PSO theory
    optimizer = PSOOptimizer(config.pso)
    best_params = optimizer.optimize_controller(
        system=system,
        controller_type='hybrid_adaptive_sta_smc',
        objectives={
            'tracking': 1.0,      # {eq}`tracking_objective`
            'effort': 0.1,        # {eq}`control_effort_objective`
            'smoothness': 0.01    # {eq}`smoothness_objective`
        }
    )

    # Create optimized controller
    controller = create_controller('hybrid_adaptive_sta_smc', **best_params)

    # Validate theoretical properties
    assert controller.verify_stability_conditions()  # Theorem 5
    assert controller.verify_convergence_properties()  # Theorem 4

    # Run final simulation
    runner = SimulationRunner(system, controller)
    results = runner.simulate(duration=10.0)

    # Visualize and analyze results
    plot_results(results)
    print(f"Performance metrics: {results.compute_metrics()}")

if __name__ == "__main__":
    main()