# Example from: docs\optimization_simulation\guide.md
# Index: 2
# Runnable: True
# Hash: 3ba3ea03

from src.optimization.algorithms.pso_optimizer import PSOTuner
from src.controllers import create_smc_for_pso, SMCType
from src.config import load_config

# Load configuration
config = load_config("config.yaml")

# Define controller factory
def controller_factory(gains):
    return create_smc_for_pso(SMCType.CLASSICAL, gains, max_force=100.0)

# Initialize PSO tuner
tuner = PSOTuner(
    controller_factory=controller_factory,
    config=config,
    seed=42,  # Reproducibility
    instability_penalty_factor=100.0
)

# Run optimization
result = tuner.optimise(
    iters_override=150,      # Override config iterations
    n_particles_override=40   # Override config swarm size
)

# Extract best gains
best_gains = result['best_pos']
best_cost = result['best_cost']
cost_history = result['history']['cost']

print(f"Best gains: {best_gains}")
print(f"Best cost: {best_cost:.4f}")
print(f"Iterations to convergence: {len(cost_history)}")