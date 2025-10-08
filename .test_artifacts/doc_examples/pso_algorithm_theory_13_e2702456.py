# Example from: docs\mathematical_foundations\pso_algorithm_theory.md
# Index: 13
# Runnable: False
# Hash: e2702456

# example-metadata:
# runnable: false

pso_config = {
    'n_particles': 30,
    'max_iters': 100,
    'inertia': 0.7298,         # Constriction coefficient
    'c1': 2.05,                # Cognitive coefficient
    'c2': 2.05,                # Social coefficient
    'bounds': [
        (0.1, 50.0),  # k1
        (0.1, 50.0),  # k2
        (0.1, 50.0),  # λ1
        (0.1, 50.0),  # λ2
        (1.0, 200.0), # K
        (0.0, 50.0),  # kd
    ],
    'objective_weights': {
        'ise': 0.5,
        'chattering': 0.3,
        'effort': 0.2,
    }
}