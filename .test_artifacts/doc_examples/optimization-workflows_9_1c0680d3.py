# Example from: docs\guides\how-to\optimization-workflows.md
# Index: 9
# Runnable: True
# Hash: 1c0680d3

import multiprocessing as mp
from functools import partial

def run_pso_trial(seed, controller_type, config):
    """Run single PSO trial."""
    tuner = PSOTuner(
        controller_type=controller_type,
        config=config,
        seed=seed
    )

    gains, cost = tuner.optimize()

    return {
        'seed': seed,
        'gains': gains,
        'cost': cost
    }

# Define seeds
seeds = [42, 123, 456, 789, 1337]

# Run in parallel
with mp.Pool(5) as pool:
    run_func = partial(
        run_pso_trial,
        controller_type='classical_smc',
        config=config
    )
    results = pool.map(run_func, seeds)

# Find best
best_result = min(results, key=lambda x: x['cost'])

print(f"Best cost: {best_result['cost']:.4f}")
print(f"Best seed: {best_result['seed']}")
print(f"Best gains: {best_result['gains']}")