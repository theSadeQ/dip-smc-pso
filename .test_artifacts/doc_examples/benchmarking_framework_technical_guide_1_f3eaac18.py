# Example from: docs\testing\benchmarking_framework_technical_guide.md
# Index: 1
# Runnable: True
# Hash: f3eaac18

# High-level workflow
from src.benchmarks import run_trials, compute_all_metrics
from src.benchmarks.statistics import compute_t_confidence_intervals

# Execute trials
metrics_list, ci_results = run_trials(
    controller_factory=create_controller,
    cfg=config,
    n_trials=30,
    seed=42
)

# Confidence intervals automatically computed
for metric, (mean, ci_width) in ci_results.items():
    print(f"{metric}: {mean:.4f} ± {ci_width:.4f}")