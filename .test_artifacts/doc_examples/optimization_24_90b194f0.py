# Example from: docs\guides\api\optimization.md
# Index: 24
# Runnable: False
# Hash: 90b194f0

# example-metadata:
# runnable: false

# Iteration count based on convergence needs
tuner_fast = PSOTuner(..., iters=50)    # Quick prototyping
tuner_standard = PSOTuner(..., iters=100)  # Standard optimization
tuner_thorough = PSOTuner(..., iters=200)  # Publication-quality