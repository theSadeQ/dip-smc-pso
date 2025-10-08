# Example from: docs\mathematical_foundations\pso_algorithm_theory.md
# Index: 9
# Runnable: True
# Hash: e3eb2c13

def select_learning_exemplar(particle_i, dimension_d):
    """Choose particle to learn from for dimension d."""
    if random() < learning_probability:
        return best_particle_except_i  # Learn from best
    else:
        return random_particle()  # Learn from random (diversity)