# Example from: docs\api\optimization_module_api_reference.md
# Index: 3
# Runnable: True
# Hash: 86acf37b

from src.optimization.algorithms.pso_optimizer import PSOTuner
from src.controllers.factory import create_controller
from src.config import load_config
from functools import partial

# Load configuration
config = load_config("config.yaml")

# Create controller factory (partial application)
controller_factory = partial(
    create_controller,
    controller_type='classical_smc',
    config=config
)

# Initialize PSO tuner
tuner = PSOTuner(
    controller_factory=controller_factory,
    config=config,
    seed=42,
    instability_penalty_factor=100.0
)

# Run optimization
result = tuner.optimise()

print(f"Best gains: {result['best_pos']}")
print(f"Best cost: {result['best_cost']:.4f}")