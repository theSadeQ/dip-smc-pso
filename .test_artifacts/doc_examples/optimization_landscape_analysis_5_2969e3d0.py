# Example from: docs\mathematical_foundations\optimization_landscape_analysis.md
# Index: 5
# Runnable: False
# Hash: 2969e3d0

def check_convexity(fitness_func, g1, g2, n_points=20):
    """Test convexity between two points."""
    alphas = np.linspace(0, 1, n_points)
    convex_bound = []
    actual_fitness = []

    for alpha in alphas:
        g_interp = alpha * g1 + (1 - alpha) * g2
        f_interp = fitness_func(g_interp)
        f_bound = alpha * fitness_func(g1) + (1 - alpha) * fitness_func(g2)

        actual_fitness.append(f_interp)
        convex_bound.append(f_bound)

    # If actual < bound everywhere → convex
    is_convex = all(a <= b for a, b in zip(actual_fitness, convex_bound))
    return is_convex, actual_fitness, convex_bound