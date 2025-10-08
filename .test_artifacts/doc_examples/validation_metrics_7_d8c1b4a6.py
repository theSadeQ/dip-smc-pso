# Example from: docs\reference\analysis\validation_metrics.md
# Index: 7
# Runnable: True
# Hash: d8c1b4a6

from src.benchmarks.metrics.control_metrics import compute_ise, compute_itae
from src.benchmarks.metrics.stability_metrics import compute_overshoot, compute_settling_time
from src.benchmarks.metrics.constraint_metrics import count_control_violations

# Control metrics
ise = compute_ise(result.time, result.states)
itae = compute_itae(result.time, result.states)

# Stability metrics
overshoot = compute_overshoot(result.states[:, 0])  # First angle
settling_time = compute_settling_time(result.time, result.states, threshold=0.02)

# Constraint violations
violations, severity, peak = count_control_violations(result.control, max_force=100.0)

print(f"ISE: {ise:.4f}, ITAE: {itae:.4f}")
print(f"Overshoot: {overshoot:.2f}%, Settling: {settling_time:.3f}s")
print(f"Violations: {violations}, Severity: {severity:.4f}, Peak: {peak:.2f}")