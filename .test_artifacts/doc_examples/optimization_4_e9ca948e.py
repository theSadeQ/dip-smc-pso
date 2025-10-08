# Example from: docs\guides\api\optimization.md
# Index: 4
# Runnable: True
# Hash: e9ca948e

import json

# Save optimized gains
results = {
    'controller_type': 'classical_smc',
    'gains': best_gains.tolist(),
    'cost': float(best_cost),
    'optimization_params': {
        'n_particles': 30,
        'iters': 100,
        'bounds': bounds
    }
}

with open('optimized_gains.json', 'w') as f:
    json.dump(results, f, indent=2)

# Load and use
with open('optimized_gains.json', 'r') as f:
    loaded = json.load(f)

controller = create_smc_for_pso(
    SMCType.CLASSICAL,
    gains=loaded['gains'],
    max_force=100.0
)