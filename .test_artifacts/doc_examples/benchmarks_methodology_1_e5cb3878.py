# Example from: docs\benchmarks_methodology.md
# Index: 1
# Runnable: True
# Hash: e5cb3878

# Base seed for reproducibility
base_seed = 1234

# Each trial gets independent seed
trial_seeds = rng.integers(0, 2**32-1, size=n_trials)