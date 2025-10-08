# Example from: docs\reference\analysis\validation_statistical_benchmarks.md
# Index: 6
# Runnable: True
# Hash: a463bacf

from src.benchmarks.statistical_benchmarks_v2 import run_trials
from src.controllers.factory import create_smc_for_pso, SMCType

# Define controller factory
def controller_factory():
    return create_smc_for_pso(
        SMCType.CLASSICAL,
        gains=[10, 8, 15, 12, 50, 5],
        max_force=100.0
    )

# Configure benchmarking
from src.config import load_config
config = load_config("config.yaml")

# Run trials with statistical analysis
metrics_list, ci_results = run_trials(
    controller_factory,
    config,
    n_trials=30,
    confidence_level=0.95
)

# Access results
print(f"Mean ISE: {ci_results['ise']['mean']:.4f}")
print(f"95% CI: [{ci_results['ise']['ci_lower']:.4f}, {ci_results['ise']['ci_upper']:.4f}]")
print(f"Std Dev: {ci_results['ise']['std']:.4f}")