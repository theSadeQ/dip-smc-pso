# Example from: docs\guides\tutorials\tutorial-01-validation-report.md
# Index: 1
# Runnable: True
# Hash: dd554ce6

from scripts.analysis.compute_performance_metrics import compute_all_metrics

# After simulation
metrics = compute_all_metrics(t, x, u)
print(metrics)

# Output:
# Performance Metrics:
#   Settling Time:       2.45 s
#   Max Overshoot:       3.2 %
#   Steady-State Error:  0.008 rad (0.46°)
#   RMS Control Effort:  12.4 N
#   Peak Control:        45.3 N
#   Control Saturation:  0.0%