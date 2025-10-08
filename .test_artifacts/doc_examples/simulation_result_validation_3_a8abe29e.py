# Example from: docs\validation\simulation_result_validation.md
# Index: 3
# Runnable: True
# Hash: a8abe29e

config = MonteCarloConfig(
    n_samples=1024,  # Typically use powers of 2
    sampling_method="sobol",
    sensitivity_analysis=True,
    sensitivity_method="sobol"
)
analyzer = MonteCarloAnalyzer(config)