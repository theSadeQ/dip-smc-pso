# Example from: docs\guides\api\optimization.md
# Index: 16
# Runnable: True
# Hash: 9e0c9b27

from concurrent.futures import ProcessPoolExecutor
import numpy as np

def optimize_controller(controller_type):
    """Optimize a single controller type."""
    bounds = get_gain_bounds_for_pso(controller_type)
    tuner = PSOTuner(controller_type, bounds, n_particles=30, iters=100)
    best_gains, best_cost = tuner.optimize()
    return controller_type, best_gains, best_cost

# Optimize all controllers in parallel
controller_types = [
    SMCType.CLASSICAL,
    SMCType.ADAPTIVE,
    SMCType.SUPER_TWISTING,
    SMCType.HYBRID
]

with ProcessPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(optimize_controller, ct) for ct in controller_types]
    results = [future.result() for future in futures]

for ctrl_type, gains, cost in results:
    print(f"{ctrl_type}: Cost={cost:.4f}, Gains={gains}")