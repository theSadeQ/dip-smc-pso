# Example from: docs\issue_12_pso_implementation_summary.md
# Index: 4
# Runnable: True
# Hash: ffb54aa0

chattering_target = 2.0           # Issue #12 target
tracking_target = 0.1             # Tracking constraint (rad)
effort_target = 100.0             # Control effort constraint (N RMS)

# Penalty weights
chattering_penalty_weight = 10.0   # Secondary objective
tracking_penalty_weight = 100.0    # Hard constraint (must not violate)
effort_penalty_weight = 0.1        # Soft constraint