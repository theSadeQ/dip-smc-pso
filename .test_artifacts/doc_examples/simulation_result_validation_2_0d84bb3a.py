# Example from: docs\validation\simulation_result_validation.md
# Index: 2
# Runnable: True
# Hash: 0d84bb3a

config = MonteCarloConfig(
    n_samples=500,  # Can use fewer samples than random
    sampling_method="latin_hypercube",
    random_seed=42
)
analyzer = MonteCarloAnalyzer(config)