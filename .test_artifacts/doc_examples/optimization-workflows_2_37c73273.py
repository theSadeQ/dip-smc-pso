# Example from: docs\guides\how-to\optimization-workflows.md
# Index: 2
# Runnable: True
# Hash: 37c73273

from src.optimizer.pso_optimizer import PSOTuner
from custom_cost import minimal_settling_time_cost
from src.config import load_config

# Load configuration
config = load_config('config.yaml')

# Create PSO tuner with custom cost
tuner = PSOTuner(
    controller_type='classical_smc',
    config=config,
    cost_function=minimal_settling_time_cost  # Custom!
)

# Run optimization
best_gains, best_cost = tuner.optimize()

print(f"Optimized gains: {best_gains}")
print(f"Final cost: {best_cost:.4f}")