# Example from: docs\reference\analysis\performance_control_metrics.md
# Index: 5
# Runnable: True
# Hash: a29f2215

# Parameter sensitivity analysis
from src.analysis.performance import sensitivity_analysis

sensitivity = sensitivity_analysis(
    system=plant,
    parameters={'mass': (0.8, 1.2), 'length': (0.9, 1.1)},
    metric=compute_stability_margin
)
print(f"Most sensitive: {sensitivity.most_sensitive_param}")