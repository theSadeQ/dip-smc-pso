# Example from: docs\mathematical_foundations\advanced_algorithms_guide.md
# Index: 14
# Runnable: True
# Hash: b42e9be3

# Set global seed in config
config.global_seed = 42

# PSO tuner uses this seed automatically
tuner = PSOTuner(controller_factory, config, seed=42)

# Results are now fully reproducible