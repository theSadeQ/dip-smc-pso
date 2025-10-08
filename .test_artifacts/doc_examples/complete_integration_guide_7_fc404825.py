# Example from: docs\workflows\complete_integration_guide.md
# Index: 7
# Runnable: False
# Hash: fc404825

# example-metadata:
# runnable: false

# Adaptive PSO with time-varying parameters
pso_config = {
    'n_particles': 25,
    'iters': 250,
    'options': {
        'c1': lambda t: 2.5 - 1.5 * t / 250,  # Decreasing cognitive
        'c2': lambda t: 0.5 + 2.0 * t / 250,  # Increasing social
        'w': lambda t: 0.9 - 0.5 * t / 250    # Decreasing inertia
    }
}