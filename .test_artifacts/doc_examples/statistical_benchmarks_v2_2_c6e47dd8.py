# Example from: docs\reference\benchmarks\statistical_benchmarks_v2.md
# Index: 2
# Runnable: True
# Hash: c6e47dd8

from src.benchmarks.statistical_benchmarks_v2 import run_trials_with_advanced_statistics

# Run with bootstrap CI (non-parametric, no normality assumption)
metrics_list, analysis = run_trials_with_advanced_statistics(
    controller_factory,
    config,
    n_trials=50,
    confidence_level=0.99,
    use_bootstrap=True,
    n_bootstrap=10000
)

# Bootstrap results more robust for non-normal distributions
print(f"Bootstrap 99% CI for settling time:")
print(f"  [{analysis['settling_time']['bootstrap_ci'][0]:.3f}, "
      f"{analysis['settling_time']['bootstrap_ci'][1]:.3f}]")