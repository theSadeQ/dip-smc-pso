# Example from: docs\mathematical_foundations\pso_algorithm_theory.md
# Index: 25
# Runnable: True
# Hash: 81785ab9

pso_params = {
    'n_particles': 30,
    'max_iters': 100,
    'inertia': 0.7298,     # Constriction coefficient
    'c1': 2.05,            # Cognitive coefficient
    'c2': 2.05,            # Social coefficient
    'v_max': 0.2 * range,  # Velocity clamping
}