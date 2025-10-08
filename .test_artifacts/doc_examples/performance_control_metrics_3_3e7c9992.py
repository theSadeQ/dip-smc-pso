# Example from: docs\reference\analysis\performance_control_metrics.md
# Index: 3
# Runnable: True
# Hash: 3e7c9992

# Compute comprehensive metrics
from src.analysis.performance import compute_all_metrics

metrics = compute_all_metrics(
    time=t,
    state=x,
    control=u,
    reference=r
)
print(f"ISE: {metrics.ise:.2f}, ITAE: {metrics.itae:.2f}")