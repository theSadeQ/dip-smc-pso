# Example from: docs\mathematical_foundations\optimization_landscape_analysis.md
# Index: 4
# Runnable: False
# Hash: c5a8e714

# example-metadata:
# runnable: false

def compute_ruggedness(fitness_function, gains, epsilon=0.1, n_samples=100):
    """Estimate landscape ruggedness via random perturbations."""
    f_center = fitness_function(gains)
    variations = []

    for _ in range(n_samples):
        perturbation = np.random.randn(len(gains)) * epsilon
        gains_perturbed = gains + perturbation
        f_perturbed = fitness_function(gains_perturbed)
        variations.append(abs(f_perturbed - f_center))

    ruggedness = np.mean(variations)
    return ruggedness