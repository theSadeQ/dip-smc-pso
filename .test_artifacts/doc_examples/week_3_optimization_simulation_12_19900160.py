# Example from: docs\plans\documentation\week_3_optimization_simulation.md
# Index: 12
# Runnable: False
# Hash: 19900160

def penalized_fitness(gains, base_fitness):
    """Add penalty for constraint violations."""
    penalty = 0.0

    # Stability constraint: positive gains
    if any(g <= 0 for g in gains[:5]):
        penalty += 1e6

    # Switching gain constraint: K > disturbance
    if gains[4] < 10.0:  # Minimum K
        penalty += 1e4 * (10.0 - gains[4])

    return base_fitness + penalty