# Example from: docs\mathematical_foundations\optimization_landscape_analysis.md
# Index: 18
# Runnable: False
# Hash: 1c921c24

# example-metadata:
# runnable: false

def diagnose_convergence(fitness_history, diversity_history):
    """Identify convergence issues."""
    if len(fitness_history) < 20:
        return "Insufficient data"

    # Check stagnation
    recent_improvement = fitness_history[-1] - fitness_history[-20]
    if abs(recent_improvement) < 1e-3:
        return "Stagnation detected"

    # Check premature convergence
    if diversity_history[-1] < 0.01 * diversity_history[0]:
        if fitness_history[-1] > 10.0:  # Poor fitness
            return "Premature convergence"

    # Check oscillation
    recent_std = np.std(fitness_history[-10:])
    if recent_std > 5.0:
        return "Unstable oscillation"

    return "Healthy convergence"