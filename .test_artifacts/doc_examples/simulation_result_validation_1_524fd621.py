# Example from: docs\validation\simulation_result_validation.md
# Index: 1
# Runnable: True
# Hash: 524fd621

from src.analysis.validation.monte_carlo import MonteCarloConfig, MonteCarloAnalyzer

config = MonteCarloConfig(
    n_samples=1000,
    sampling_method="random",
    random_seed=42
)
analyzer = MonteCarloAnalyzer(config)