# Example from: docs\guides\api\optimization.md
# Index: 20
# Runnable: True
# Hash: 0ec01594

from src.config import load_config
from src.optimizer import PSOTuner
from src.controllers import SMCType, get_gain_bounds_for_pso, create_smc_for_pso
from src.core import SimulationRunner

# Setup
config = load_config('config.yaml')
bounds = get_gain_bounds_for_pso(SMCType.CLASSICAL)

# Optimize
tuner = PSOTuner(SMCType.CLASSICAL, bounds, n_particles=30, iters=100, config=config)
best_gains, best_cost = tuner.optimize()

# Validate
controller = create_smc_for_pso(SMCType.CLASSICAL, best_gains)
runner = SimulationRunner(config)
result = runner.run(controller)

print(f"Optimized Cost: {best_cost:.4f}")
print(f"Validation ISE: {result['metrics']['ise']:.4f}")