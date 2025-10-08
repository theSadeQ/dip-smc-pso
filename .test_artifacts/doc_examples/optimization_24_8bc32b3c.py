# Example from: docs\guides\api\optimization.md
# Index: 24
# Runnable: False
# Hash: 8bc32b3c

# Iteration count based on convergence needs
tuner_fast = PSOTuner(..., iters=50)    # Quick prototyping
tuner_standard = PSOTuner(..., iters=100)  # Standard optimization
tuner_thorough = PSOTuner(..., iters=200)  # Publication-quality