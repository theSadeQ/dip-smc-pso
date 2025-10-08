# Example from: docs\mathematical_foundations\pso_algorithm_theory.md
# Index: 12
# Runnable: False
# Hash: 8363ac7b

def penalized_fitness(gains):
    """Add large penalty for invalid gains."""
    base_fitness = evaluate_fitness(gains)
    penalty = 0.0

    # Stability constraint violation
    if any(g <= 0 for g in gains[:5]):
        penalty += 1e6

    # Minimum switching gain
    if gains[4] < 10.0:
        penalty += 1e4 * (10.0 - gains[4])

    return base_fitness + penalty