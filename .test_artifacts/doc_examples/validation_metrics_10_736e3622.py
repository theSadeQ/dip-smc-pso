# Example from: docs\reference\analysis\validation_metrics.md
# Index: 10
# Runnable: True
# Hash: 736e3622

from src.benchmarks.metrics import compute_all_metrics

# Compute metrics for multiple trials
trials_results = []  # List of simulation results from multiple runs

metrics_collection = []
for result in trials_results:
    metrics = compute_all_metrics(result.time, result.states, result.control, 100.0)
    metrics_collection.append(metrics)

# Aggregate statistics
import pandas as pd
df = pd.DataFrame(metrics_collection)

print("Metric Statistics Across Trials:")
print(df[['ise', 'settling_time', 'overshoot', 'rms_control']].describe())