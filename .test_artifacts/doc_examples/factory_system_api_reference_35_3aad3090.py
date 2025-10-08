# Example from: docs\api\factory_system_api_reference.md
# Index: 35
# Runnable: False
# Hash: 3aad3090

from src.controllers.factory import SMCType, create_pso_controller_factory
from src.optimization.algorithms.pso_optimizer import PSOTuner
from src.config import load_config
import numpy as np

# Load configuration
config = load_config("config.yaml")

# Step 1: Create PSO-compatible controller factory
controller_factory = create_pso_controller_factory(
    smc_type=SMCType.CLASSICAL,
    max_force=150.0,
    dt=0.001
)

# Step 2: Initialize PSO tuner
tuner = PSOTuner(
    controller_factory=controller_factory,
    config=config,
    seed=42
)

# Step 3: Run PSO optimization
print("Starting PSO optimization...")
result = tuner.optimise(
    n_particles_override=30,
    iters_override=100
)

# Step 4: Extract optimized gains
optimized_gains = result['best_pos']
best_cost = result['best_cost']
print(f"Optimized gains: {optimized_gains}")
print(f"Best cost: {best_cost:.6f}")

# Step 5: Create final controller with optimized gains
from src.controllers.factory import create_controller
optimized_controller = create_controller(
    'classical_smc',
    config,
    gains=optimized_gains
)

# Step 6: Validate optimized controller
validation_cost = evaluate_controller(optimized_controller)
print(f"Validation cost: {validation_cost:.6f}")

# Step 7: Compare with baseline
baseline_controller = create_controller('classical_smc', config)
baseline_cost = evaluate_controller(baseline_controller)
improvement = (baseline_cost - validation_cost) / baseline_cost * 100
print(f"Improvement over baseline: {improvement:.1f}%")