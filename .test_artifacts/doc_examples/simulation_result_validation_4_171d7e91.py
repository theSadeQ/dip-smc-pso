# Example from: docs\validation\simulation_result_validation.md
# Index: 4
# Runnable: True
# Hash: 171d7e91

config = MonteCarloConfig(
    n_samples=1000,
    sampling_method="halton"
)
analyzer = MonteCarloAnalyzer(config)