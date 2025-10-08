# Example from: docs\validation\simulation_result_validation.md
# Index: 6
# Runnable: True
# Hash: ccc9ba6a

config = MonteCarloConfig(
    convergence_tolerance=0.01,  # 1% relative change
    convergence_window=50,
    min_samples=100,
    max_samples=10000
)