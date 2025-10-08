# Example from: docs\issue_12_pso_failure_analysis.md
# Index: 2
# Runnable: True
# Hash: 98a3fcb1

# From optimize_chattering_focused.py (CORRECT)
fitness = chattering_index + tracking_constraint_penalty

# Direct chattering minimization
if tracking_error_rms > 0.1:
    tracking_constraint_penalty = (tracking_error_rms - 0.1) * 1000.0
else:
    tracking_constraint_penalty = 0.0

# Chattering is PRIMARY objective, tracking is CONSTRAINT