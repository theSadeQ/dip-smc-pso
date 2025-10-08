# Example from: docs\validation\simulation_result_validation.md
# Index: 24
# Runnable: True
# Hash: e07a0e64

from src.analysis.validation.benchmarking import BenchmarkConfig, BenchmarkSuite

config = BenchmarkConfig(
    metrics_to_compare=["settling_time", "overshoot", "control_effort"],
    primary_metric="settling_time"
)