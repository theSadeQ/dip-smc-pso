# Example from: docs\guides\api\optimization.md
# Index: 2
# Runnable: True
# Hash: 6c36d362

# Run optimization
best_gains, best_cost = tuner.optimize()

print(f"Optimized gains: {best_gains}")
print(f"Best cost: {best_cost:.4f}")

# Create optimized controller
from src.controllers import create_smc_for_pso

optimized_controller = create_smc_for_pso(
    SMCType.CLASSICAL,
    gains=best_gains,
    max_force=100.0
)