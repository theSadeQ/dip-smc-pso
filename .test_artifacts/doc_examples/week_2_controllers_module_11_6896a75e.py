# Example from: docs\plans\documentation\week_2_controllers_module.md
# Index: 11
# Runnable: True
# Hash: 6896a75e

from src.benchmarks.statistical_benchmarks_v2 import run_trials

metrics_list, ci_results = run_trials(
    controller_factory, config, n_trials=30
)