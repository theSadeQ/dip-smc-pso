# Example from: docs\optimization_simulation\index.md
# Index: 1
# Runnable: True
# Hash: 49fa0afc

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
    seed=42
)

# Run optimization
result = tuner.optimise()

# Extract best gains
best_gains = result['best_pos']
best_cost = result['best_cost']