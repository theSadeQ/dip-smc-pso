# Example from: docs\mathematical_foundations\optimization_landscape_analysis.md
# Index: 9
# Runnable: False
# Hash: 25119f60

def barrier_penalty(gains, mu=0.05):
    """Logarithmic barrier for stability constraints."""
    penalty = 0.0

    # Surface gains must be positive
    for i in range(4):
        if gains[i] <= 0:
            return 1e9  # Hard constraint violation
        penalty -= mu * np.log(gains[i])

    # Switching gain must exceed disturbance
    K_margin = gains[4] - 10.0
    if K_margin <= 0:
        return 1e9
    penalty -= mu * np.log(K_margin)

    return penalty

def fitness_with_barrier(gains):
    return base_fitness(gains) + barrier_penalty(gains)