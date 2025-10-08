# Example from: docs\mathematical_foundations\pso_algorithm_theory.md
# Index: 6
# Runnable: True
# Hash: 33c9fd94

def check_convergence(fitness_history, window=10, tolerance=1e-6):
    """Stop if fitness stagnates."""
    if len(fitness_history) < window:
        return False

    recent = fitness_history[-window:]
    stagnation = max(recent) - min(recent)

    return stagnation < tolerance