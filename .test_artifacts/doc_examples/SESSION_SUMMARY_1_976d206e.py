# Example from: docs\SESSION_SUMMARY.md
# Index: 1
# Runnable: False
# Hash: 976d206e

# Original (WRONG):
fitness = tracking_error_rms + chattering_penalty + ...
# chattering_penalty = 0 if chattering < 2.0 ← ALWAYS ZERO!

# Corrected (RIGHT):
fitness = chattering_index  # Direct minimization