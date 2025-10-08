# Example from: docs\issue_12_pso_implementation_summary.md
# Index: 3
# Runnable: True
# Hash: deed636f

n_particles: 50          # Increased for better exploration
iters: 300               # Longer convergence for multi-objective
w: 0.7                   # Inertia weight (exploration vs exploitation)
c1: 2.0                  # Cognitive coefficient (personal best)
c2: 2.0                  # Social coefficient (global best)
seed: 42                 # Reproducibility