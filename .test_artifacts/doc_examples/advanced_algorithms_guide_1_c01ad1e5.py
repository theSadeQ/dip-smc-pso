# Example from: docs\mathematical_foundations\advanced_algorithms_guide.md
# Index: 1
# Runnable: True
# Hash: c01ad1e5

from src.optimization.algorithms.pso_optimizer import PSOTuner
from src.controllers.factory import create_controller
from src.config import load_config

# Load configuration
config = load_config("config.yaml")

# Define controller factory
def controller_factory(gains):
    return create_controller(
        'classical_smc',
        config=config,
        gains=gains
    )

# Initialize PSO tuner
tuner = PSOTuner(
    controller_factory=controller_factory,
    config=config,
    seed=42,  # Reproducible results
    instability_penalty_factor=100.0
)

# Run optimization
result = tuner.optimise(
    iters_override=100,           # 100 PSO iterations
    n_particles_override=30,      # 30 particles
    options_override={
        'w': 0.7,                 # Constant inertia
        'c1': 2.05,               # Cognitive coefficient
        'c2': 2.05                # Social coefficient
    }
)

# Extract results
best_gains = result['best_pos']
best_cost = result['best_cost']
convergence_history = result['history']['cost']

print(f"Optimal gains: {best_gains}")
print(f"Final cost: {best_cost:.6f}")