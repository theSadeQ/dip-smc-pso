# Example from: docs\issue_12_pso_failure_analysis.md
# Index: 1
# Runnable: True
# Hash: fe550886

# From optimize_chattering_direct.py
fitness = tracking_error + chattering_penalty
chattering_penalty = max(0, chattering - 2.0) * 10.0  # ZERO if chattering < 2.0!

# If tracking good and chattering < 2.0: fitness = 0.0
# Result: No optimization pressure on chattering!