# Example from: docs\mathematical_foundations\pso_algorithm_theory.md
# Index: 3
# Runnable: True
# Hash: e57e5131

# Swarm knowledge attraction
social = c2 * random() * (global_best - position)
velocity_new += social