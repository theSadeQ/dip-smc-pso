# Example from: docs\benchmarks_methodology.md
# Index: 4
# Runnable: True
# Hash: bd8ec234

from src.benchmarks.statistical_benchmarks_v2 import run_trials
from src.controllers.factory import create_controller_factory
from src.config import load_config

# Load configuration
config = load_config('config.yaml')

# Create controller factory
factory = create_controller_factory('classical_smc', config.controllers.classical_smc)

# Run benchmark
metrics_per_trial, ci_results = run_trials(
    controller_factory=factory,
    cfg=config,
    n_trials=30,
    seed=1234
)

# Display results with confidence intervals
for metric, (mean, ci_width) in ci_results.items():
    print(f"{metric}: {mean:.4f} ± {ci_width:.4f}")