# Example from: docs\optimization_simulation\guide.md
# Index: 22
# Runnable: True
# Hash: e4e8eaa0

from src.optimization.algorithms.pso_optimizer import PSOTuner
from src.config import load_config

config = load_config("config.yaml")

# Configure uncertainty evaluation
config.physics_uncertainty = {
    "n_evals": 10,  # 10 perturbed physics models
    "cart_mass": 0.15,          # ±15% variation
    "pendulum1_mass": 0.15,
    "pendulum2_mass": 0.15,
    "pendulum1_length": 0.05,   # ±5% variation
    "pendulum2_length": 0.05,
    "gravity": 0.01,            # ±1% variation (altitude/latitude)
    "cart_friction": 0.20,      # ±20% variation
    "joint1_friction": 0.20,
    "joint2_friction": 0.20,
}

# Define controller factory
from src.controllers import create_smc_for_pso, SMCType

def controller_factory(gains):
    return create_smc_for_pso(SMCType.ADAPTIVE, gains, max_force=100.0)

# Initialize tuner
tuner = PSOTuner(
    controller_factory=controller_factory,
    config=config,
    seed=42
)

# Run robust optimization
result = tuner.optimise()

print(f"Robust gains optimized under {config.physics_uncertainty.n_evals} uncertainty scenarios")
print(f"Best robust cost: {result['best_cost']:.4f}")
print(f"Optimized gains: {result['best_pos']}")