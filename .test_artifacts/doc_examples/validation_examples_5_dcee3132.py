# Example from: docs\validation\validation_examples.md
# Index: 5
# Runnable: True
# Hash: dcee3132

config = MonteCarloConfig(
    n_samples=1024,  # Power of 2 for Sobol
    sampling_method="sobol",
    sensitivity_analysis=True,
    sensitivity_method="sobol"
)