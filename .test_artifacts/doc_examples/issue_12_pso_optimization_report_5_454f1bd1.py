# Example from: docs\issue_12_pso_optimization_report.md
# Index: 5
# Runnable: True
# Hash: 454f1bd1

chattering_target = 2.0           # Issue #12 target
tracking_target = 0.1             # Max acceptable tracking error (rad)
effort_target = 100.0             # Control effort constraint (N RMS)

chattering_penalty_weight = 10.0  # Secondary objective weight
tracking_penalty_weight = 100.0   # Hard constraint weight
effort_penalty_weight = 0.1       # Soft constraint weight