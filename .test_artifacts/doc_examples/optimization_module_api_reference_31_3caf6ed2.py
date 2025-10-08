# Example from: docs\api\optimization_module_api_reference.md
# Index: 31
# Runnable: False
# Hash: 3caf6ed2

#!/usr/bin/env python3
"""
Example 1: Basic PSO Optimization for Classical SMC

Demonstrates:
- Configuration loading
- Controller factory creation
- PSO tuner initialization
- Optimization execution
- Result visualization
"""

import matplotlib.pyplot as plt
import numpy as np
from functools import partial

from src.optimization.algorithms.pso_optimizer import PSOTuner
from src.controllers.factory import create_controller
from src.config import load_config

# ============================================================================
# Configuration
# ============================================================================

CONFIG_PATH = "config.yaml"
CONTROLLER_TYPE = 'classical_smc'
SEED = 42

# ============================================================================
# Main Optimization
# ============================================================================

def main():
    # Load configuration
    print("Loading configuration...")
    config = load_config(CONFIG_PATH)

    # Create controller factory (partial application for PSO)
    print("Creating controller factory...")
    controller_factory = partial(
        create_controller,
        controller_type=CONTROLLER_TYPE,
        config=config
    )

    # Initialize PSO tuner
    print("Initializing PSO tuner...")
    tuner = PSOTuner(
        controller_factory=controller_factory,
        config=config,
        seed=SEED,
        instability_penalty_factor=100.0
    )

    # Run optimization
    print(f"Running PSO optimization with {config.pso.n_particles} particles for {config.pso.n_iterations} iterations...")
    result = tuner.optimise()

    # Extract results
    best_gains = result['best_pos']
    best_cost = result['best_cost']
    cost_history = result['cost_history']

    print(f"\n{'='*80}")
    print("OPTIMIZATION RESULTS")
    print(f"{'='*80}")
    print(f"Best Cost: {best_cost:.6f}")
    print(f"Best Gains: {best_gains}")
    print(f"Convergence: {len(cost_history)} iterations")
    print(f"{'='*80}\n")

    # Plot convergence
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(cost_history, linewidth=2)
    ax.set_xlabel('Iteration', fontsize=12)
    ax.set_ylabel('Best Cost', fontsize=12)
    ax.set_title('PSO Convergence History - Classical SMC', fontsize=14, fontweight='bold')
    ax.set_yscale('log')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('pso_convergence_basic.png', dpi=300)
    print("Convergence plot saved: pso_convergence_basic.png")

    # Save optimized gains
    np.save('optimized_gains_classical_smc.npy', best_gains)
    print("Optimized gains saved: optimized_gains_classical_smc.npy")

if __name__ == "__main__":
    main()