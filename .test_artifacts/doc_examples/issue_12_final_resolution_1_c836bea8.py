# Example from: docs\issue_12_final_resolution.md
# Index: 1
# Runnable: True
# Hash: c836bea8

# Original fitness (optimize_chattering_direct.py):
fitness = tracking_error_rms + chattering_penalty + tracking_penalty + effort_penalty

# Where:
chattering_penalty = max(0, chattering_index - 2.0) * 10.0